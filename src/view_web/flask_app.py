import sys
# Agrega el directorio 'src' al path del sistema para poder importar módulos desde allí
sys.path.append("src")

# Importa la clase BaseDeDatos desde el controlador
from controller.controlador import BaseDeDatos

# Importa funciones auxiliares para cálculos desde el controlador de consola
from view.console.consolacontrolador import asignar_id_liquidacion, calcular_indemnizacion, calcular_valor_vacaciones, calcular_cesantias, calcular_intereses_sobre_cesantias, calcular_prima_servicios, calcular_retencion_fuente, dias_trabajados

# Importa módulos de Flask para crear la aplicación web
from flask import Flask, render_template, request, redirect, url_for, flash

# Clase principal de la aplicación
class Run:
    app = Flask(__name__, template_folder='templates')
    app.secret_key = "supersecretkey"  # Llave secreta para manejar sesiones y mensajes flash


    @app.route('/')
    @staticmethod
    def index():
        return render_template('index.html')

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
                # Intenta agregar el usuario a la base de datos
                print(f"DEBUG: Intentando agregar usuario ID: {id_usuario}, Nombre: {nombre}")
                BaseDeDatos.agregar_usuario(nombre, apellido, documento_identidad, correo_electronico, telefono, fecha_ingreso, fecha_salida, salario, id_usuario)
                flash("Usuario agregado exitosamente", "success")
                print(f"DEBUG: Usuario {id_usuario} agregado exitosamente")
                return redirect(url_for('index'))
            except Exception as e:
                # Si hay un error, muestra un mensaje flash detallado
                error_msg = f"Error al agregar el usuario: {str(e)}"
                print(f"DEBUG: {error_msg}")
                flash(error_msg, "error")
                return redirect(url_for('agregar_usuario'))
        # Renderiza la plantilla para agregar usuario
        return render_template('agregar_usuario.html')

    @app.route('/agregar_liquidacion', methods=['GET', 'POST'])
    @staticmethod
    def agregar_liquidacion():
        if request.method == 'POST':
            try:
                # Obtiene y convierte el salario del formulario
                salario = float(request.form['salario'])
            except ValueError:
                # Si hay un error en el salario, retorna un mensaje de error
                return "Salario inválido. Por favor, ingresa un valor numérico."

            # Obtiene las fechas y el ID del usuario del formulario
            fecha_ingreso = request.form['fecha_ingreso']
            fecha_salida = request.form['fecha_salida']
            try:
                id_usuario = int(request.form['id_usuario'])
                
            except ValueError:
                return "ID de usuario inválido. Por favor, ingresa un valor numérico."

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
            BaseDeDatos.agregar_liquidacion(id_liquidacion, indemnizacion, valor_vacaciones, cesantias, 
                                    intereses_sobre_cesantias, prima_servicios, retencion_fuente, 
                                    total_a_pagar, id_usuario)
            
            flash("Liquidación agregada exitosamente. El total a pagar es: {:.2f}".format(total_a_pagar))
            return redirect(url_for('index'))
        # Renderiza la plantilla para agregar liquidación
        return render_template('agregar_liquidacion.html')
    
    @app.route('/consultar_usuario', methods=['GET', 'POST'])
    @staticmethod
    def consultar_usuario():
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
        if request.method == 'POST':
            # Obtiene el ID del usuario del formulario
            id_usuario = request.form['id_usuario']
            # Elimina el usuario de la base de datos
            BaseDeDatos.eliminar_usuario(id_usuario)
            flash("Usuario eliminado exitosamente")
            return redirect(url_for('index'))
        # Renderiza la plantilla para eliminar usuario
        return render_template('eliminar_usuario.html')

    @app.route('/eliminar_liquidacion', methods=['GET', 'POST'])
    @staticmethod
    def eliminar_liquidacion():
        if request.method == 'POST':
            # Obtiene el ID de la liquidación del formulario
            id_liquidacion = request.form['id_liquidacion']
            # Elimina la liquidación de la base de datos
            BaseDeDatos.eliminar_liquidacion(id_liquidacion)
            flash("Liquidación eliminada exitosamente")
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

# Inicia la aplicación Flask en modo depuración
if __name__ == "__main__":
    Run.app.run(debug=True)
