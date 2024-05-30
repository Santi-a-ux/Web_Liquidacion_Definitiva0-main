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
    def index():
        # Renderiza la plantilla del índice
        return render_template('index.html')

    @app.route('/agregar_usuario', methods=['GET', 'POST'])
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
                BaseDeDatos.agregar_usuario(nombre, apellido, documento_identidad, correo_electronico, telefono, fecha_ingreso, fecha_salida, salario, id_usuario)
                flash("Usuario agregado exitosamente")
                return redirect(url_for('index'))
            except Exception as e:
                # Si hay un error, muestra un mensaje flash
                flash(f"Error al agregar el usuario: {str(e)}")
                return redirect(url_for('agregar_usuario'))
        # Renderiza la plantilla para agregar usuario
        return render_template('agregar_usuario.html')

    @app.route('/agregar_liquidacion', methods=['GET', 'POST'])
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
    def consultar_usuario():
        if request.method == 'POST':
            # Obtiene el ID del usuario del formulario
            id_usuario = request.form['id_usuario']
            # Consulta el usuario y su liquidación en la base de datos
            usuario, Liquidacion = BaseDeDatos.consultar_usuario(id_usuario)
            if usuario:
                # Si el usuario existe, renderiza la plantilla con los datos del usuario y la liquidación
                return render_template('consultar_usuario.html', usuario=usuario, liquidacion=Liquidacion)
            else:
                # Si el usuario no se encuentra, muestra un mensaje flash
                flash("Usuario no encontrado")
                return redirect(url_for('consultar_usuario'))
        # Renderiza la plantilla para consultar usuario
        return render_template('consultar_usuario.html')

    @app.route('/eliminar_usuario', methods=['GET', 'POST'])
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

# Inicia la aplicación Flask en modo depuración
if __name__ == "__main__":
    Run.app.run(debug=True)
