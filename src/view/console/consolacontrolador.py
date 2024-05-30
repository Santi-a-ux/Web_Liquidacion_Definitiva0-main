import sys
import os

sys.path.append("src")  # Agrega la ruta "src" al sistema para buscar módulos
from controller.controlador import BaseDeDatos  # Importa la clase BaseDeDatos del controlador
from datetime import datetime  # Importa la clase datetime para trabajar con fechas
import random  # Importa el módulo random para generar valores aleatorios

# Función para asignar un ID de liquidación aleatorio
def asignar_id_liquidacion():
    return random.randint(0, 9)

# Funciones para calcular diferentes aspectos de la liquidación
def calcular_indemnizacion(salario_mensual, años_trabajados):
    return salario_mensual * años_trabajados

def calcular_valor_vacaciones(dias_trabajados, salario_anual):
    return (dias_trabajados / 365) * salario_anual * (15 / 365)

def calcular_cesantias(dias_trabajados, salario):
    return (dias_trabajados / 360) * salario

def calcular_intereses_sobre_cesantias(cesantias):
    return cesantias * 0.12

def calcular_prima_servicios(salario_semestral):
    return salario_semestral / 12

def calcular_retencion_fuente(total_a_pagar, tasa_retencion):
    return (total_a_pagar / 12) * tasa_retencion

def dias_trabajados(fecha_ingreso, fecha_salida):
    fecha_ingreso = datetime.strptime(fecha_ingreso, '%Y-%m-%d')  # Convierte la fecha de ingreso a formato datetime
    fecha_salida = datetime.strptime(fecha_salida, '%Y-%m-%d')    # Convierte la fecha de salida a formato datetime
    delta = fecha_salida - fecha_ingreso  # Calcula la diferencia entre las fechas
    return delta.days  # Retorna el número de días de diferencia

# Función principal del menú
def main_menu():
    while True:
        print("Selecciona una opción:")
        print("1. Agregar usuario")
        print("2. Agregar liquidación")
        print("3. Consultar usuario")
        print("4. Eliminar usuario")
        print("5. Salir")
        print("6. Eliminar Liquidación")

        try:
            opcion = int(input("Ingresa el número de la opción: "))
        except ValueError:
            print("Opción inválida. Por favor, selecciona una opción válida.")
            continue

        if opcion == 1:
            # Solicita información del usuario y la agrega a la base de datos
            nombre = input("Ingresa el nombre del usuario: ")
            apellido = input("Ingresa el apellido del usuario: ")
            documento_identidad = input("Ingresa el documento de identidad del usuario: ")
            correo_electronico = input("Ingresa el correo electrónico del usuario: ")
            telefono = input("Ingresa el teléfono del usuario: ")
            fecha_ingreso = input("Ingresa la fecha de ingreso del usuario (AAAA-MM-DD): ")
            fecha_salida = input("Ingresa la fecha de salida del usuario (AAAA-MM-DD): ")
            id_usuario = input("Ingresa el ID de su nuevo usuario: ")
            try:
                salario = float(input("Ingresa el salario del usuario: "))
            except ValueError:
                print("Salario inválido. Por favor, ingresa un valor numérico.")
                continue
            BaseDeDatos.agregar_usuario(nombre, apellido, documento_identidad, correo_electronico, telefono, fecha_ingreso, fecha_salida, salario, id_usuario)

        elif opcion == 2:
            # Solicita información para calcular la liquidación y la agrega a la base de datos
            try:
                salario = float(input("Ingresa el salario mensual del usuario: "))
            except ValueError:
                print("Salario inválido. Por favor, ingresa un valor numérico.")
                continue
            
            fecha_ingreso = input("Ingresa la fecha de ingreso del usuario (AAAA-MM-DD): ")
            fecha_salida = input("Ingresa la fecha de salida del usuario (AAAA-MM-DD): ")
            try:
                id_usuario = int(input("Ingresa el ID del usuario: "))
            except ValueError:
                print("ID de usuario inválido. Por favor, ingresa un valor numérico.")
                continue
            
            dias_trabajados_total = dias_trabajados(fecha_ingreso, fecha_salida)
            años_trabajados = dias_trabajados_total // 360
            salario_anual = salario * 12
            salario_semestral = salario * 6
            tasa_retencion = 0.1  # Suponiendo una tasa de retención del 10%

            id_liquidacion = asignar_id_liquidacion()
            print("El ID de tu liquidación es: ", id_liquidacion)
            indemnizacion = calcular_indemnizacion(salario, años_trabajados)
            valor_vacaciones = calcular_valor_vacaciones(dias_trabajados_total, salario_anual)
            cesantias = calcular_cesantias(dias_trabajados_total, salario)
            intereses_sobre_cesantias = calcular_intereses_sobre_cesantias(cesantias)
            prima_servicios = calcular_prima_servicios(salario_semestral)
            retencion_fuente = calcular_retencion_fuente(salario_anual, tasa_retencion)
            total_a_pagar = indemnizacion + valor_vacaciones + cesantias + intereses_sobre_cesantias + prima_servicios - retencion_fuente

            BaseDeDatos.agregar_liquidacion(id_liquidacion, indemnizacion, valor_vacaciones, cesantias, intereses_sobre_cesantias, prima_servicios, retencion_fuente, total_a_pagar, id_usuario)
            print(f"Liquidación agregada exitosamente. Total a pagar: {total_a_pagar}")

        elif opcion == 3:
            # Consulta un usuario en la base de datos
            try:
                id_usuario = int(input("Ingresa el ID del usuario a consultar: "))
            except ValueError:
                print("ID de usuario inválido. Por favor, ingresa un valor numérico.")
                continue
            BaseDeDatos.consultar_usuario(id_usuario)

        elif opcion == 4:
            # Elimina un usuario de la base de datos
            try:
                id_usuario = int(input("Ingresa el ID del usuario a eliminar: "))
            except ValueError:
                print("ID de usuario inválido. Por favor, ingresa un valor numérico.")
                continue
            try:
                BaseDeDatos.eliminar_usuario(id_usuario)
                print("Usuario eliminado exitosamente.")
            except ValueError:
                print("Error al eliminar el usuario. Por favor, verifica el ID.")

        elif opcion == 5:
            # Sale del menú
            print("Saliendo del menú...")
            sys.exit()

        elif opcion == 6:
            # Elimina una liquidación de la base de datos
            try:
                id_liquidacion = int(input("Ingresa el ID de la liquidación a eliminar: "))
            except ValueError:
                print("ID de liquidación inválido. Por favor, ingresa un valor numérico.")
                continue
            try:
                BaseDeDatos.eliminar_liquidacion(id_liquidacion)
                print("Liquidación eliminada exitosamente.")
            except ValueError:
                print("Error al eliminar la liquidación. Por favor, verifica el ID.")

        else:
            print("Opción inválida. Por favor, selecciona una opción válida.")

if __name__ == "__main__":
    main_menu()  # Ejecuta la función principal del menú
