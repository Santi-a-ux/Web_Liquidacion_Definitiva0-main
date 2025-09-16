import sys
import os

sys.path.append("src")  # Agrega la ruta "src" al sistema para buscar módulos
from controller.controlador import BaseDeDatos  # Importa la clase BaseDeDatos del controlador
from datetime import datetime  # Importa la clase datetime para trabajar con fechas
import random  # Importa el módulo random para generar valores aleatorios

# Función para asignar un ID de liquidación único
def asignar_id_liquidacion():
    """
    Genera un ID único para liquidación dentro del rango de INT (2,147,483,647)
    usando timestamp + número aleatorio pequeño
    """
    import time
    import random
    
    # Usar los últimos 4 dígitos del timestamp + 3 dígitos aleatorios = 7 dígitos max
    timestamp = int(time.time()) % 10000  # Últimos 4 dígitos del timestamp
    random_part = random.randint(100, 999)  # 3 dígitos aleatorios
    
    # Combinar: máximo 7 dígitos (dentro del rango de INT)
    unique_id = int(f"{timestamp}{random_part}")
    
    # Asegurar que esté en rango válido (1-2,000,000,000)
    if unique_id > 2000000000:
        unique_id = unique_id % 2000000000
        
    # Asegurar que no sea 0
    if unique_id == 0:
        unique_id = random.randint(100000, 999999)
    
    return unique_id

# Funciones para calcular diferentes aspectos de la liquidación
def calcular_indemnizacion(salario_mensual, anios_trabajados):
    return salario_mensual * anios_trabajados

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
ID_USUARIO_INVALIDO_MSG = "ID de usuario inválido. Por favor, ingresa un valor numérico."

def agregar_usuario():
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
        return
    BaseDeDatos.agregar_usuario(nombre, apellido, documento_identidad, correo_electronico, telefono, fecha_ingreso, fecha_salida, salario, id_usuario)

def agregar_liquidacion():
    try:
        salario = float(input("Ingresa el salario mensual del usuario: "))
    except ValueError:
        print("Salario inválido. Por favor, ingresa un valor numérico.")
        return
    fecha_ingreso = input("Ingresa la fecha de ingreso del usuario (AAAA-MM-DD): ")
    fecha_salida = input("Ingresa la fecha de salida del usuario (AAAA-MM-DD): ")
    try:
        id_usuario = int(input("Ingresa el ID del usuario: "))
    except ValueError:
        print(ID_USUARIO_INVALIDO_MSG)
        return
    dias_trabajados_total = dias_trabajados(fecha_ingreso, fecha_salida)
    anios_trabajados = dias_trabajados_total // 360
    salario_anual = salario * 12
    salario_semestral = salario * 6
    tasa_retencion = 0.1  # Suponiendo una tasa de retención del 10%
    id_liquidacion = asignar_id_liquidacion()
    print("El ID de tu liquidación es: ", id_liquidacion)
    indemnizacion = calcular_indemnizacion(salario, anios_trabajados)
    valor_vacaciones = calcular_valor_vacaciones(dias_trabajados_total, salario_anual)
    cesantias = calcular_cesantias(dias_trabajados_total, salario)
    intereses_sobre_cesantias = calcular_intereses_sobre_cesantias(cesantias)
    prima_servicios = calcular_prima_servicios(salario_semestral)
    retencion_fuente = calcular_retencion_fuente(salario_anual, tasa_retencion)
    total_a_pagar = indemnizacion + valor_vacaciones + cesantias + intereses_sobre_cesantias + prima_servicios - retencion_fuente
    BaseDeDatos.agregar_liquidacion(id_liquidacion, indemnizacion, valor_vacaciones, cesantias, intereses_sobre_cesantias, prima_servicios, retencion_fuente, total_a_pagar, id_usuario)
    print(f"Liquidación agregada exitosamente. Total a pagar: {total_a_pagar}")

def consultar_usuario():
    try:
        id_usuario = int(input("Ingresa el ID del usuario a consultar: "))
    except ValueError:
        print(ID_USUARIO_INVALIDO_MSG)
        return
    BaseDeDatos.consultar_usuario(id_usuario)

def eliminar_usuario():
    try:
        id_usuario = int(input("Ingresa el ID del usuario a eliminar: "))
    except ValueError:
        print(ID_USUARIO_INVALIDO_MSG)
        return
    try:
        BaseDeDatos.eliminar_usuario(id_usuario)
        print("Usuario eliminado exitosamente.")
    except ValueError:
        print("Error al eliminar el usuario. Por favor, verifica el ID.")

def eliminar_liquidacion():
    try:
        id_liquidacion = int(input("Ingresa el ID de la liquidación a eliminar: "))
    except ValueError:
        print("ID de liquidación inválido. Por favor, ingresa un valor numérico.")
        return
    try:
        BaseDeDatos.eliminar_liquidacion(id_liquidacion)
        print("Liquidación eliminada exitosamente.")
    except ValueError:
        print("Error al eliminar la liquidación. Por favor, verifica el ID.")

def mostrar_menu():
    print("Selecciona una opción:")
    print("1. Agregar usuario")
    print("2. Agregar liquidación")
    print("3. Consultar usuario")
    print("4. Eliminar usuario")
    print("5. Salir")
    print("6. Eliminar Liquidación")

def main_menu():
    while True:
        mostrar_menu()
        try:
            opcion = int(input("Ingresa el número de la opción: "))
        except ValueError:
            print("Opción inválida. Por favor, selecciona una opción válida.")
            continue

        if opcion == 1:
            agregar_usuario()
        elif opcion == 2:
            agregar_liquidacion()
        elif opcion == 3:
            consultar_usuario()
        elif opcion == 4:
            eliminar_usuario()
        elif opcion == 5:
            print("Saliendo del menú...")
            sys.exit()
        elif opcion == 6:
            eliminar_liquidacion()
        else:
            print("Opción inválida. Por favor, selecciona una opción válida.")

if __name__ == "__main__":
    main_menu()  # Ejecuta la función principal del menú
