import sys
import os
# Agrega el directorio padre al path del sistema para poder importar módulos desde allí
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Importa la clase BaseDeDatos desde el controlador
from controller.controlador import BaseDeDatos

# Importa funciones auxiliares para cálculos desde el controlador de consola
from view.console.consolacontrolador import asignar_id_liquidacion, calcular_indemnizacion, calcular_valor_vacaciones, calcular_cesantias, calcular_intereses_sobre_cesantias, calcular_prima_servicios, calcular_retencion_fuente, dias_trabajados

# Importa módulos de Flask para crear la aplicación web
from flask import Flask, render_template, request, redirect, url_for, flash, session

# Clase principal de la aplicación
class Run:
    app = Flask(__name__, template_folder='templates')
    app.secret_key = "supersecretkey"  # Llave secreta para manejar sesiones y mensajes flash

    # Decorador para verificar si está logueado
    @staticmethod
    def login_required(f):
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash("Debes iniciar sesión para acceder", "error")
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        decorated_function.__name__ = f.__name__
        return decorated_function

    # Decorador para verificar si es administrador (RRHH)
    @staticmethod
    def admin_required(f):
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash("Debes iniciar sesión para acceder", "error")
                return redirect(url_for('login'))
            if session.get('rol') != 'administrador':
                flash("Acceso denegado. Solo personal de Recursos Humanos", "error")
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        decorated_function.__name__ = f.__name__
        return decorated_function

    @app.route('/login', methods=['GET', 'POST'])
    @staticmethod
    def login():
        if request.method == 'POST':
            id_usuario = request.form['id_usuario']
            password = request.form['password']
            
            # Autenticar usuario
            resultado = BaseDeDatos.autenticar_usuario(id_usuario, password)
            
            if resultado['autenticado']:
                session['user_id'] = resultado['id']
                session['nombre'] = resultado['nombre']
                session['apellido'] = resultado['apellido']
                session['rol'] = resultado['rol']
                
                # Registrar inicio de sesión en auditoría
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
    @staticmethod
    def logout():
        session.clear()
        flash("Sesión cerrada exitosamente", "success")
        return redirect(url_for('login'))

    @app.route('/')
    @staticmethod
    def index():
        # Verificar si está logueado
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        return render_template('index.html', 
                             usuario_nombre=session.get('nombre'),
                             usuario_rol=session.get('rol'))

    @app.route('/test')
    @staticmethod
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
    @staticmethod
    def agregar_usuario():
        # Verificar sesión
        if 'user_id' not in session:
            flash("Debes iniciar sesión para acceder", "error")
            return redirect(url_for('login'))
            
        if request.method == 'POST':
            # Obtiene los datos del formulario
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
                # Intenta agregar el empleado a la base de datos
                print(f"DEBUG: Intentando agregar empleado ID: {id_usuario}, Nombre: {nombre}")
                BaseDeDatos.agregar_usuario(nombre, apellido, documento_identidad, correo_electronico, telefono, fecha_ingreso, fecha_salida, salario, id_usuario, usuario_sistema=session.get('user_id'))
                flash("Empleado agregado exitosamente", "success")
                print(f"DEBUG: Empleado {id_usuario} agregado exitosamente")
                return redirect(url_for('index'))
            except Exception as e:
                # Si hay un error, muestra un mensaje flash detallado
                error_msg = f"Error al agregar el empleado: {str(e)}"
                print(f"DEBUG: {error_msg}")
                flash(error_msg, "error")
                return redirect(url_for('agregar_usuario'))
        # Renderiza la plantilla para agregar usuario
        return render_template('agregar_usuario.html')

    @app.route('/agregar_liquidacion', methods=['GET', 'POST'])
    @staticmethod
    def agregar_liquidacion():
        # Verificar sesión
        if 'user_id' not in session:
            flash("Debes iniciar sesión para acceder", "error")
            return redirect(url_for('login'))
            
        if request.method == 'POST':
            try:
                id_usuario = int(request.form['id_usuario'])
            except ValueError:
                flash("ID de empleado inválido. Por favor, ingresa un valor numérico.", "error")
                return render_template('agregar_liquidacion.html')

            # Obtener TODA la información del empleado desde la base de datos
            try:
                empleado_data = BaseDeDatos.consultar_usuario(id_usuario)
                if not empleado_data[0]:  # Si no existe el empleado
                    flash(f"No se encontró un empleado con ID: {id_usuario}", "error")
                    return render_template('agregar_liquidacion.html')
                
                # Extraer TODOS los datos del empleado automáticamente
                empleado = empleado_data[0]
                salario = float(empleado[8])  # Salario
                fecha_ingreso = str(empleado[6])  # Fecha de ingreso
                fecha_salida = str(empleado[7])   # Fecha de salida
                
                print(f"DEBUG: Empleado {id_usuario} - Salario: {salario}, Ingreso: {fecha_ingreso}, Salida: {fecha_salida}")
                
            except Exception as e:
                flash(f"Error al obtener información del empleado: {str(e)}", "error")
                return render_template('agregar_liquidacion.html')

            # Calcula varios valores necesarios para la liquidación
            dias_trabajados_total = dias_trabajados(fecha_ingreso, fecha_salida)
            años_trabajados = dias_trabajados_total // 360
            salario_anual = salario * 12
            salario_semestral = salario * 6
            tasa_retencion = 0.1  # Suponiendo una tasa de retención del 10%

            # Asigna un ID para la liquidación y calcula los valores de la liquidación
            id_liquidacion = asignar_id_liquidacion()
            indemnizacion = calcular_indemnizacion(salario, años_trabajados)
            valor_vacaciones = calcular_valor_vacaciones(dias_trabajados_total, salario_anual)
            cesantias = calcular_cesantias(dias_trabajados_total, salario)
            intereses_sobre_cesantias = calcular_intereses_sobre_cesantias(cesantias)
            prima_servicios = calcular_prima_servicios(salario_semestral)
            retencion_fuente = calcular_retencion_fuente(salario_anual, tasa_retencion)
            total_a_pagar = (indemnizacion + valor_vacaciones + cesantias + 
                            intereses_sobre_cesantias + prima_servicios - retencion_fuente)
            
            # Agrega la liquidación a la base de datos
            resultado_guardado = BaseDeDatos.agregar_liquidacion(id_liquidacion, indemnizacion, valor_vacaciones, cesantias, 
                                    intereses_sobre_cesantias, prima_servicios, retencion_fuente, 
                                    total_a_pagar, id_usuario)
            
            if resultado_guardado:
                flash(f"✅ Liquidación creada exitosamente para el empleado {id_usuario}. Total a pagar: ${total_a_pagar:,.2f}", "success")
            else:
                flash("❌ Error al guardar la liquidación en la base de datos", "error")
                
            return redirect(url_for('index'))
        # Renderiza la plantilla para agregar liquidación
        return render_template('agregar_liquidacion.html')
    
    @app.route('/consultar_usuario', methods=['GET', 'POST'])
    @staticmethod
    def consultar_usuario():
        # Verificar sesión
        if 'user_id' not in session:
            flash("Debes iniciar sesión para acceder", "error")
            return redirect(url_for('login'))
            
        if request.method == 'POST':
            # Obtiene el ID del usuario del formulario
            id_usuario = int(request.form['id_usuario'])  # Convertir a entero
            print(f"DEBUG: Consultando usuario con ID: {id_usuario}")
            # Consulta el usuario y su liquidación en la base de datos
            usuario, Liquidacion = BaseDeDatos.consultar_usuario(id_usuario)
            print(f"DEBUG: Resultado consulta - Usuario: {usuario}, Liquidacion: {Liquidacion}")
            if usuario:
                # Si el usuario existe, renderiza la plantilla con los datos del usuario y la liquidación
                print("DEBUG: Usuario encontrado, renderizando template")
                return render_template('consultar_usuario.html', usuario=usuario, liquidacion=Liquidacion)
            else:
                # Si el usuario no se encuentra, muestra un mensaje flash
                print("DEBUG: Usuario no encontrado")
                flash("Usuario no encontrado")
                return redirect(url_for('consultar_usuario'))
        # Renderiza la plantilla para consultar usuario
        return render_template('consultar_usuario.html')

    @app.route('/eliminar_usuario', methods=['GET', 'POST'])
    @staticmethod
    def eliminar_usuario():
        # Verificar sesión y rol de administrador
        if 'user_id' not in session:
            flash("Debes iniciar sesión para acceder", "error")
            return redirect(url_for('login'))
        
        if session.get('rol') != 'administrador':
            flash("Acceso denegado. Solo personal de Recursos Humanos puede eliminar empleados", "error")
            return redirect(url_for('index'))
            
        if request.method == 'POST':
            # Obtiene el ID del usuario del formulario
            id_usuario = request.form['id_usuario']
            # Elimina el usuario de la base de datos
            resultado = BaseDeDatos.eliminar_usuario(id_usuario, usuario_sistema=session.get('user_id'))
            
            if resultado:
                flash("Empleado eliminado exitosamente", "success")
            else:
                flash("Error: No se pudo eliminar el empleado. Verifica que no tenga liquidaciones pendientes.", "error")
            
            return redirect(url_for('index'))
        # Renderiza la plantilla para eliminar empleado
        return render_template('eliminar_usuario.html')

    @app.route('/eliminar_liquidacion', methods=['GET', 'POST'])
    @staticmethod
    def eliminar_liquidacion():
        # Verificar sesión y rol de administrador
        if 'user_id' not in session:
            flash("Debes iniciar sesión para acceder", "error")
            return redirect(url_for('login'))
        
        if session.get('rol') != 'administrador':
            flash("Acceso denegado. Solo administradores pueden eliminar liquidaciones", "error")
            return redirect(url_for('index'))
            
        if request.method == 'POST':
            # Obtiene el ID de la liquidación del formulario
            id_liquidacion = request.form['id_liquidacion']
            # Elimina la liquidación de la base de datos
            resultado = BaseDeDatos.eliminar_liquidacion(id_liquidacion)
            
            if resultado:
                flash("Liquidación eliminada exitosamente", "success")
            else:
                flash("Error: No se encontró la liquidación con ese ID.", "error")
            
            return redirect(url_for('index'))
        # Renderiza la plantilla para eliminar liquidación
        return render_template('eliminar_liquidacion.html')


    @app.route('/admin')
    @staticmethod
    def admin_panel_redirect():
        return redirect(url_for('admin_panel'))

    @app.route('/admin_panel')
    @staticmethod
    def admin_panel():
        # Verificar sesión y rol de administrador
        if 'user_id' not in session:
            flash("Debes iniciar sesión para acceder", "error")
            return redirect(url_for('login'))
        
        if session.get('rol') != 'administrador':
            flash("Acceso denegado. Solo administradores", "error")
            return redirect(url_for('index'))
            
        """Panel de administración para ver todos los datos"""
        try:
            usuarios = BaseDeDatos.obtener_todos_usuarios()
            liquidaciones = BaseDeDatos.obtener_todas_liquidaciones()
            stats = BaseDeDatos.obtener_estadisticas()
            return render_template('admin_panel.html', 
                                 usuarios=usuarios, 
                                 liquidaciones=liquidaciones,
                                 stats=stats)
        except Exception as e:
            flash(f"Error al cargar el panel de administración: {str(e)}", "error")
            return redirect(url_for('index'))




    @app.route('/admin/usuarios')
    @staticmethod
    def admin_usuarios():
        """Ver solo la lista de usuarios"""
        try:
            usuarios = BaseDeDatos.obtener_todos_usuarios()
            return render_template('admin_usuarios.html', usuarios=usuarios)
        except Exception as e:
            flash(f"Error al cargar usuarios: {str(e)}", "error")
            return redirect(url_for('admin_panel'))



    @app.route('/simple')
    @staticmethod
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

    @app.route('/modificar_usuario', methods=['GET', 'POST'])
    @staticmethod
    def modificar_usuario():
        # Verificar sesión
        if 'user_id' not in session:
            flash("Debes iniciar sesión para acceder", "error")
            return redirect(url_for('login'))
        
        if request.method == 'GET':
            # Mostrar formulario de búsqueda/edición
            id_usuario = request.args.get('id')
            usuario_data = None
            
            if id_usuario:
                # Buscar datos del usuario para prellenar el formulario
                usuario, _ = BaseDeDatos.consultar_usuario(id_usuario)
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
        
        elif request.method == 'POST':
            # Procesar modificación
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
                
                # Llamar función de modificación
                exito, mensaje = BaseDeDatos.modificar_usuario(
                    id_usuario, nombre, apellido, documento, correo, 
                    telefono, fecha_ingreso, fecha_salida, salario, usuario_sistema=session.get('user_id')
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

    # =============== RUTAS DE AUDITORÍA ===============
    
    @app.route('/auditoria')
    @admin_required
    def auditoria():
        """Página principal de auditoría - solo para administradores RRHH"""
        try:
            # Obtener parámetros de filtro
            usuario_filtro = request.args.get('usuario_filtro')
            accion_filtro = request.args.get('accion_filtro')
            tabla_filtro = request.args.get('tabla_filtro')
            limite = int(request.args.get('limite', 50))
            
            # Obtener registros de auditoría
            registros = BaseDeDatos.obtener_auditoria(
                limite=limite,
                usuario_filtro=usuario_filtro,
                accion_filtro=accion_filtro,
                tabla_filtro=tabla_filtro
            )
            
            # Obtener estadísticas
            estadisticas = BaseDeDatos.obtener_estadisticas_auditoria()
            
            return render_template('auditoria.html', 
                                 registros=registros, 
                                 estadisticas=estadisticas,
                                 filtros={
                                     'usuario_filtro': usuario_filtro,
                                     'accion_filtro': accion_filtro,
                                     'tabla_filtro': tabla_filtro,
                                     'limite': limite
                                 })
        except Exception as e:
            flash(f"Error al cargar auditoría: {str(e)}", "error")
            return redirect(url_for('admin_panel'))

    # =============== RUTA DE REPORTES AVANZADOS ===============
    
    @app.route('/reportes')
    @staticmethod
    @admin_required
    def reportes():
        """Página dedicada de reportes avanzados - solo para administradores RRHH"""
        try:
            from datetime import datetime
            
            # Obtener estadísticas generales
            stats = BaseDeDatos.obtener_estadisticas()
            
            # Obtener todos los empleados para análisis
            empleados = BaseDeDatos.obtener_todos_usuarios()
            
            # Obtener todas las liquidaciones para análisis
            liquidaciones = BaseDeDatos.obtener_todas_liquidaciones()
            
            # Análisis por mes (últimos 6 meses)
            empleados_por_mes = {}
            
            if empleados:
                for emp in empleados:
                    fecha_ingreso = emp[6]  # fecha_ingreso
                    if fecha_ingreso:
                        mes = f"{fecha_ingreso.year}-{fecha_ingreso.month:02d}"
                        empleados_por_mes[mes] = empleados_por_mes.get(mes, 0) + 1
            
            # Análisis de rangos salariales
            rangos_salariales = {
                'Menos de 2M': 0,
                '2M - 5M': 0,
                '5M - 10M': 0,
                'Más de 10M': 0
            }
            
            if empleados:
                for emp in empleados:
                    salario = float(emp[8]) if emp[8] else 0
                    if salario < 2000000:
                        rangos_salariales['Menos de 2M'] += 1
                    elif salario < 5000000:
                        rangos_salariales['2M - 5M'] += 1
                    elif salario < 10000000:
                        rangos_salariales['5M - 10M'] += 1
                    else:
                        rangos_salariales['Más de 10M'] += 1
            
            # Top empleados por salario
            top_empleados = []
            if empleados:
                empleados_ordenados = sorted(empleados, key=lambda x: float(x[8]) if x[8] else 0, reverse=True)
                top_empleados = empleados_ordenados[:10]
            
            # Análisis de liquidaciones
            total_por_componente = {
                'indemnizacion': 0,
                'vacaciones': 0,
                'cesantias': 0,
                'intereses': 0,
                'prima': 0,
                'retencion': 0
            }
            
            if liquidaciones:
                for liq in liquidaciones:
                    total_por_componente['indemnizacion'] += float(liq[1]) if liq[1] else 0
                    total_por_componente['vacaciones'] += float(liq[2]) if liq[2] else 0
                    total_por_componente['cesantias'] += float(liq[3]) if liq[3] else 0
                    total_por_componente['intereses'] += float(liq[4]) if liq[4] else 0
                    total_por_componente['prima'] += float(liq[5]) if liq[5] else 0
                    total_por_componente['retencion'] += float(liq[6]) if liq[6] else 0
            
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
    @staticmethod
    @admin_required
    def exportar_datos():
        """Exportar datos en formato CSV"""
        try:
            import csv
            import io
            from datetime import datetime
            from flask import make_response
            
            # Crear archivo CSV en memoria
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Obtener datos
            empleados = BaseDeDatos.obtener_todos_usuarios()
            liquidaciones = BaseDeDatos.obtener_todas_liquidaciones()
            
            # Escribir encabezados
            writer.writerow(['REPORTE COMPLETO DEL SISTEMA - GENERADO:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
            writer.writerow([])  # Línea vacía
            
            # Datos de empleados
            writer.writerow(['=== EMPLEADOS ==='])
            writer.writerow(['ID', 'Nombre', 'Apellido', 'Documento', 'Correo', 'Teléfono', 'Fecha Ingreso', 'Fecha Salida', 'Salario', 'Rol'])
            
            if empleados:
                for emp in empleados:
                    writer.writerow(emp)
            
            writer.writerow([])  # Línea vacía
            
            # Datos de liquidaciones
            writer.writerow(['=== LIQUIDACIONES ==='])
            writer.writerow(['ID Liquidación', 'Indemnización', 'Vacaciones', 'Cesantías', 'Intereses', 'Prima', 'Retención', 'Total', 'ID Empleado'])
            
            if liquidaciones:
                for liq in liquidaciones:
                    writer.writerow(liq)
            
            # Preparar respuesta
            output.seek(0)
            response = make_response(output.getvalue())
            response.headers['Content-Type'] = 'text/csv'
            response.headers['Content-Disposition'] = f'attachment; filename=reporte_liquidaciones_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            
            return response
            
        except Exception as e:
            flash(f"Error al exportar datos: {str(e)}", "error")
            return redirect(url_for('reportes'))

# Inicia la aplicación Flask en modo depuración
if __name__ == "__main__":
    Run.app.run(debug=True)
