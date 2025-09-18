import sys
import os
import secrets  # Para generar una clave aleatoria segura
import logging
from datetime import date  # Para manejar fecha_salida None

# Carga opcional de variables desde .env en desarrollo (no requerido para CI)
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# Permite importar desde src/
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from controller.controlador import BaseDeDatos

# Funciones auxiliares de consola usadas en las vistas
from view.console.consolacontrolador import (
    asignar_id_liquidacion,
    calcular_indemnizacion,
    calcular_valor_vacaciones,
    calcular_cesantias,
    calcular_intereses_sobre_cesantias,
    calcular_prima_servicios,
    calcular_retencion_fuente,
    dias_trabajados,
)

from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response

# NUEVO: Protección CSRF
from flask_wtf import CSRFProtect

# Constantes
LOGIN_REQUIRED_MSG = "Debes iniciar sesión para acceder"
TEMPLATE_AGREGAR_LIQUIDACION = 'agregar_liquidacion.html'  # Evita duplicar el literal

logger = logging.getLogger(__name__)

# Instancia global de Flask
app = Flask(__name__, template_folder='templates')

# Secret key NO hardcodeada
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or secrets.token_hex(32)

# Configuración CSRF (opcionalmente ajustable)
app.config.setdefault("WTF_CSRF_ENABLED", True)
app.config.setdefault("WTF_CSRF_TIME_LIMIT", None)

# Inicializa CSRF global
csrf = CSRFProtect(app)


# Decoradores a nivel de módulo
def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash(LOGIN_REQUIRED_MSG, "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function


def admin_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash(LOGIN_REQUIRED_MSG, "error")
            return redirect(url_for('login'))
        if session.get('rol') != 'administrador':
            flash("Acceso denegado. Solo personal de Recursos Humanos", "error")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function


# =============== RUTAS ===============

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        id_usuario = request.form['id_usuario']
        password = request.form['password']

        bd = BaseDeDatos()
        resultado = bd.autenticar_usuario(id_usuario, password)

        if resultado.get('autenticado'):
            session['user_id'] = resultado['id']
            session['nombre'] = resultado['nombre']
            session['apellido'] = resultado['apellido']
            session['rol'] = resultado['rol']

            # Registrar auditoría de login (mejor esfuerzo)
            try:
                BaseDeDatos.registrar_auditoria(
                    usuario_sistema=resultado['id'],
                    accion='LOGIN',
                    tabla_afectada='usuarios',
                    id_registro=resultado['id'],
                    ip_address=request.remote_addr,
                    descripcion=f'Inicio de sesión exitoso: {resultado["nombre"]} {resultado["apellido"]} ({resultado["rol"]})'
                )
            except Exception as e:
                print(f"Error al registrar auditoría de login: {e}")

            flash(f"Bienvenido {resultado['nombre']} ({resultado['rol']})", "success")
            return redirect(url_for('index'))
        else:
            flash("Credenciales incorrectas", "error")

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada exitosamente", "success")
    return redirect(url_for('login'))


@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    return render_template('index.html',
                           usuario_nombre=session.get('nombre'),
                           usuario_rol=session.get('rol'))


@app.route('/test')
def test():
    return """
    <!DOCTYPE html>
    <html lang='es'>
    <head><meta charset='UTF-8'><title>Test Flask</title></head>
    <body style='background:#222;color:#0f0;font-size:2rem;'>
    <h1>¡Ruta /test funciona!</h1>
    <p>Esto es HTML plano desde Flask.</p>
    </body></html>
    """


@app.route('/agregar_usuario', methods=['GET', 'POST'])
@login_required
def agregar_usuario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        documento_identidad = request.form['documento_identidad']
        correo_electronico = request.form['correo_electronico']
        telefono = request.form['telefono']
        fecha_ingreso = request.form['fecha_ingreso']
        fecha_salida = request.form['fecha_salida']
        salario = request.form['salario']
        id_usuario = request.form['id_usuario']

        try:
            print(f"DEBUG: Intentando agregar empleado ID: {id_usuario}, Nombre: {nombre}")
            bd = BaseDeDatos()
            bd.agregar_usuario(
                nombre, apellido, documento_identidad, correo_electronico, telefono,
                fecha_ingreso, fecha_salida, salario, id_usuario,
                usuario_sistema=session.get('user_id')
            )
            flash("Empleado agregado exitosamente", "success")
            print(f"DEBUG: Empleado {id_usuario} agregado exitosamente")
            return redirect(url_for('index'))
        except Exception as e:
            error_msg = f"Error al agregar el empleado: {str(e)}"
            print(f"DEBUG: {error_msg}")
            flash(error_msg, "error")
            return redirect(url_for('agregar_usuario'))

    return render_template('agregar_usuario.html')


@app.route('/agregar_liquidacion', methods=['GET', 'POST'])
@login_required
def agregar_liquidacion():
    if request.method == 'POST':
        try:
            id_usuario = int(request.form['id_usuario'])
        except ValueError:
            flash("ID de empleado inválido. Por favor, ingresa un valor numérico.", "error")
            return render_template(TEMPLATE_AGREGAR_LIQUIDACION)

        # Obtener datos del empleado
        try:
            bd = BaseDeDatos()
            empleado_data = bd.consultar_usuario(id_usuario)
            if not empleado_data or not empleado_data[0]:
                flash(f"No se encontró un empleado con ID: {id_usuario}", "error")
                return render_template(TEMPLATE_AGREGAR_LIQUIDACION)

            empleado = empleado_data[0]
            salario = float(empleado[8])
            fecha_ingreso = str(empleado[6])  # YYYY-MM-DD
            # USAR fecha actual si no tiene fecha de salida para evitar fallo en dias_trabajados
            fecha_salida = str(empleado[7]) if empleado[7] else date.today().strftime('%Y-%m-%d')
            print(f"DEBUG: Empleado {id_usuario} - Salario: {salario}, Ingreso: {fecha_ingreso}, Salida: {fecha_salida}")
        except Exception as e:
            flash(f"Error al obtener información del empleado: {str(e)}", "error")
            return render_template(TEMPLATE_AGREGAR_LIQUIDACION)

        # Cálculos
        dias_trabajados_total = dias_trabajados(fecha_ingreso, fecha_salida)
        anios_trabajados = dias_trabajados_total // 360
        salario_anual = salario * 12
        salario_semestral = salario * 6
        tasa_retencion = 0.1

        id_liquidacion = asignar_id_liquidacion()
        indemnizacion = calcular_indemnizacion(salario, anios_trabajados)
        valor_vacaciones = calcular_valor_vacaciones(dias_trabajados_total, salario_anual)
        cesantias = calcular_cesantias(dias_trabajados_total, salario)
        intereses_sobre_cesantias = calcular_intereses_sobre_cesantias(cesantias)
        prima_servicios = calcular_prima_servicios(salario_semestral)
        retencion_fuente = calcular_retencion_fuente(salario_anual, tasa_retencion)
        total_a_pagar = (
            indemnizacion + valor_vacaciones + cesantias +
            intereses_sobre_cesantias + prima_servicios - retencion_fuente
        )

        resultado_guardado = bd.agregar_liquidacion(
            id_liquidacion, indemnizacion, valor_vacaciones, cesantias,
            intereses_sobre_cesantias, prima_servicios, retencion_fuente,
            total_a_pagar, id_usuario
        )

        if resultado_guardado:
            flash(f"OK Liquidación creada exitosamente para el empleado {id_usuario}. Total a pagar: ${total_a_pagar:,.2f}", "success")
        else:
            flash("ERROR Error al guardar la liquidación en la base de datos", "error")

        return redirect(url_for('index'))

    return render_template(TEMPLATE_AGREGAR_LIQUIDACION)


@app.route('/consultar_usuario', methods=['GET', 'POST'])
@login_required
def consultar_usuario():
    if request.method == 'POST':
        id_usuario = int(request.form['id_usuario'])
        print(f"DEBUG: Consultando usuario con ID: {id_usuario}")
        bd = BaseDeDatos()
        usuario, liquidacion = bd.consultar_usuario(id_usuario)  # nombre en minúscula
        print(f"DEBUG: Resultado consulta - Usuario: {usuario}, Liquidacion: {liquidacion}")
        if usuario:
            print("DEBUG: Usuario encontrado, renderizando template")
            return render_template('consultar_usuario.html', usuario=usuario, liquidacion=liquidacion)
        else:
            print("DEBUG: Usuario no encontrado")
            flash("Usuario no encontrado")
            return redirect(url_for('consultar_usuario'))

    return render_template('consultar_usuario.html')


@app.route('/eliminar_usuario', methods=['GET', 'POST'])
@admin_required
def eliminar_usuario():
    if request.method == 'POST':
        id_usuario = request.form['id_usuario']
        bd = BaseDeDatos()
        resultado = bd.eliminar_usuario(id_usuario, usuario_sistema=session.get('user_id'))

        if resultado:
            flash("Empleado eliminado exitosamente", "success")
        else:
            flash("Error: No se pudo eliminar el empleado. Verifica que no tenga liquidaciones pendientes.", "error")

        return redirect(url_for('index'))
    return render_template('eliminar_usuario.html')


@app.route('/eliminar_liquidacion', methods=['GET', 'POST'])
@admin_required
def eliminar_liquidacion():
    if request.method == 'POST':
        id_liquidacion = request.form['id_liquidacion']
        bd = BaseDeDatos()
        resultado = bd.eliminar_liquidacion(id_liquidacion)

        if resultado:
            flash("Liquidación eliminada exitosamente", "success")
        else:
            flash("Error: No se encontró la liquidación con ese ID.", "error")

        return redirect(url_for('index'))
    return render_template('eliminar_liquidacion.html')


@app.route('/admin')
def admin_panel_redirect():
    return redirect(url_for('admin_panel'))


@app.route('/admin_panel')
@admin_required
def admin_panel():
    """Panel de administración para ver todos los datos"""
    try:
        bd = BaseDeDatos()
        usuarios = bd.obtener_todos_usuarios()
        liquidaciones = bd.obtener_todas_liquidaciones()
        stats = bd.obtener_estadisticas()
        return render_template('admin_panel.html',
                               usuarios=usuarios,
                               liquidaciones=liquidaciones,
                               stats=stats)
    except Exception as e:
        flash(f"Error al cargar el panel de administración: {str(e)}", "error")
        return redirect(url_for('index'))


@app.route('/admin/usuarios')
@admin_required
def admin_usuarios():
    """Ver solo la lista de usuarios"""
    try:
        bd = BaseDeDatos()
        usuarios = bd.obtener_todos_usuarios()
        return render_template('admin_usuarios.html', usuarios=usuarios)
    except Exception as e:
        flash(f"Error al cargar usuarios: {str(e)}", "error")
        return redirect(url_for('admin_panel'))


@app.route('/simple')
def simple():
    """Página de prueba simple"""
    return """
    <!DOCTYPE html>
    <html lang='es'>
    <head><meta charset='UTF-8'><title>Prueba Flask</title></head>
    <body style='background:#111;color:#0ff;font-size:2rem;'>
    <h1>¡Flask responde correctamente!</h1>
    <p>Si ves esto, el backend y el navegador funcionan.</p>
    </body></html>
    """


# Nueva ruta: Auditoría (requerida por tests)
@app.route('/auditoria', methods=['GET'])
@admin_required
def auditoria():
    try:
        limite_str = request.args.get('limite', '100')
        try:
            limite = int(limite_str)
        except ValueError:
            limite = 100

        usuario_filtro = request.args.get('usuario_filtro')
        accion_filtro = request.args.get('accion_filtro')
        tabla_filtro = request.args.get('tabla_filtro')

        registros = BaseDeDatos.obtener_auditoria(
            limite=limite,
            usuario_filtro=int(usuario_filtro) if usuario_filtro else None,
            accion_filtro=accion_filtro,
            tabla_filtro=tabla_filtro
        )
        stats = BaseDeDatos.obtener_estadisticas_auditoria()
        return render_template('auditoria.html', registros=registros, stats=stats)
    except Exception as exc:
        flash(f"Error al cargar auditoría: {exc}", "error")
        return redirect(url_for('admin_panel'))


# ===== Helpers para reportes (reducen complejidad cognitiva de la vista) =====

def _empleados_por_mes(empleados):
    """Dict {YYYY-MM: count} a partir de la fecha de ingreso (emp[6])"""
    conteo = {}
    if not empleados:
        return conteo
    for emp in empleados:
        fecha_ingreso = emp[6]
        if fecha_ingreso:
            mes = f"{fecha_ingreso.year}-{fecha_ingreso.month:02d}"
            conteo[mes] = conteo.get(mes, 0) + 1
    return conteo


def _rangos_salariales(empleados):
    """Distribución por rangos definidos"""
    rangos = {
        'Menos de 2M': 0,
        '2M - 5M': 0,
        '5M - 10M': 0,
        'Más de 10M': 0
    }
    if not empleados:
        return rangos
    for emp in empleados:
        salario = float(emp[8]) if emp[8] else 0
        if salario < 2_000_000:
            rangos['Menos de 2M'] += 1
        elif salario < 5_000_000:
            rangos['2M - 5M'] += 1
        elif salario < 10_000_000:
            rangos['5M - 10M'] += 1
        else:
            rangos['Más de 10M'] += 1
    return rangos


def _top_empleados(empleados, n=10):
    """Top N por salario (emp[8])"""
    if not empleados:
        return []
    empleados_ordenados = sorted(empleados, key=lambda x: float(x[8]) if x[8] else 0, reverse=True)
    return empleados_ordenados[:n]


def _total_por_componente(liquidaciones):
    """Suma por componente a partir de filas de liquidación"""
    totales = {
        'indemnizacion': 0,
        'vacaciones': 0,
        'cesantias': 0,
        'intereses': 0,
        'prima': 0,
        'retencion': 0
    }
    if not liquidaciones:
        return totales
    for liq in liquidaciones:
        totales['indemnizacion'] += float(liq[1]) if liq[1] else 0
        totales['vacaciones'] += float(liq[2]) if liq[2] else 0
        totales['cesantias'] += float(liq[3]) if liq[3] else 0
        totales['intereses'] += float(liq[4]) if liq[4] else 0
        totales['prima'] += float(liq[5]) if liq[5] else 0
        totales['retencion'] += float(liq[6]) if liq[6] else 0
    return totales


@app.route('/modificar_usuario', methods=['GET', 'POST'])
@login_required
def modificar_usuario():
    if request.method == 'GET':
        id_usuario = request.args.get('id')
        usuario_data = None

        if id_usuario:
            bd = BaseDeDatos()
            usuario, _ = bd.consultar_usuario(id_usuario)
            if usuario:
                usuario_data = {
                    'id': usuario[0],
                    'nombre': usuario[1],
                    'apellido': usuario[2],
                    'documento': usuario[3],
                    'correo': usuario[4],
                    'telefono': usuario[5],
                    'fecha_ingreso': usuario[6],
                    'fecha_salida': usuario[7],
                    'salario': usuario[8]
                }
            else:
                flash("Usuario no encontrado", "error")
        return render_template('modificar_usuario.html', usuario=usuario_data)

    try:
        id_usuario = request.form['id_usuario']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        documento = request.form['documento']
        correo = request.form['correo']
        telefono = request.form['telefono']
        fecha_ingreso = request.form['fecha_ingreso']
        fecha_salida = request.form['fecha_salida'] if request.form['fecha_salida'] else None
        salario = float(request.form['salario'])

        bd = BaseDeDatos()
        exito, mensaje = bd.modificar_usuario(
            id_usuario, nombre, apellido, documento, correo,
            telefono, fecha_ingreso, fecha_salida, salario,
            usuario_sistema=session.get('user_id')
        )

        if exito:
            flash(mensaje, "success")
            return redirect(url_for('index'))
        else:
            flash(mensaje, "error")
            return redirect(url_for('modificar_usuario', id=id_usuario))

    except Exception as e:
        flash(f"Error al procesar modificación: {str(e)}", "error")
        return redirect(url_for('modificar_usuario'))


# =============== REPORTES Y EXPORTACIÓN ===============

@app.route('/reportes')
@admin_required
def reportes():
    """Página dedicada de reportes avanzados - solo para administradores RRHH"""
    try:
        bd = BaseDeDatos()
        stats = bd.obtener_estadisticas()
        empleados = bd.obtener_todos_usuarios()
        liquidaciones = bd.obtener_todas_liquidaciones()

        empleados_por_mes = _empleados_por_mes(empleados)
        rangos_salariales = _rangos_salariales(empleados)
        top_empleados = _top_empleados(empleados, n=10)
        total_por_componente = _total_por_componente(liquidaciones)

        return render_template('reportes.html',
                               stats=stats,
                               empleados=empleados,
                               liquidaciones=liquidaciones,
                               empleados_por_mes=empleados_por_mes,
                               rangos_salariales=rangos_salariales,
                               top_empleados=top_empleados,
                               total_por_componente=total_por_componente)
    except Exception as e:
        flash(f"Error al cargar reportes: {str(e)}", "error")
        return redirect(url_for('admin_panel'))


@app.route('/exportar_datos')
@admin_required
def exportar_datos():
    """Exportar datos en formato CSV"""
    try:
        import csv
        import io
        from datetime import datetime

        output = io.StringIO()
        writer = csv.writer(output)

        bd = BaseDeDatos()
        empleados = bd.obtener_todos_usuarios()
        liquidaciones = bd.obtener_todas_liquidaciones()

        writer.writerow(['REPORTE COMPLETO DEL SISTEMA - GENERADO:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        writer.writerow([])

        writer.writerow(['=== EMPLEADOS ==='])
        writer.writerow(['ID', 'Nombre', 'Apellido', 'Documento', 'Correo', 'Teléfono', 'Fecha Ingreso', 'Fecha Salida', 'Salario', 'Rol'])
        if empleados:
            for emp in empleados:
                writer.writerow(emp)

        writer.writerow([])
        writer.writerow(['=== LIQUIDACIONES ==='])
        writer.writerow(['ID Liquidación', 'Indemnización', 'Vacaciones', 'Cesantías', 'Intereses', 'Prima', 'Retención', 'Total', 'ID Empleado'])
        if liquidaciones:
            for liq in liquidaciones:
                writer.writerow(liq)

        output.seek(0)
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = f'attachment; filename=reporte_liquidaciones_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        return response

    except Exception as e:
        flash(f"Error al exportar datos: {str(e)}", "error")
        return redirect(url_for('reportes'))


# Compatibilidad con tests que utilizan flask_app.Run.app
class Run:
    app = app


if __name__ == "__main__":  # pragma: no cover
    Run.app.run(debug=True)
