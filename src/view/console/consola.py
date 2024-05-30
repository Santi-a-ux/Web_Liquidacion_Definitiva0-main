import sys
sys.path.append("src")
from model.calculadora import CalculadoraLiquidacion 
from controller.controlador import conectar_db, agregar_usuario, agregar_liquidacion, consultar_usuario, eliminar_usuario

calculadora = CalculadoraLiquidacion()

salario_basico = float(input("Ingrese el salario básico en pesos colombianos: "))
fecha_inicio_labores = input("Ingrese la fecha de inicio de labores (dd/mm/yyyy): ")
fecha_ultimas_vacaciones = input("Ingrese la fecha de las últimas vacaciones (dd/mm/yyyy): ")
dias_acumulados_vacaciones = int(input("Ingrese los días acumulados de vacaciones: "))

try:
    indemnizacion, vacaciones, cesantias, intereses_cesantias, primas, retencion_fuente, total_pagar = calculadora.calcular_resultados_prueba(
        salario_basico=salario_basico,
        fecha_inicio_labores=fecha_inicio_labores,
        fecha_ultimas_vacaciones=fecha_ultimas_vacaciones,
        dias_acumulados_vacaciones=dias_acumulados_vacaciones
    )
    
    print(f"Indemnización: COP {indemnizacion:,.2f}")
    print(f"Vacaciones: COP {vacaciones:,.2f}")
    print(f"Cesantías: COP {cesantias:,.2f}")
    print(f"Intereses sobre cesantías: COP {intereses_cesantias:,.2f}")
    print(f"Prima de servicios: COP {primas:,.2f}")
    print(f"Retención en la fuente: COP {retencion_fuente:,.2f}")
    print(f"Total a pagar: COP {total_pagar:,.2f}")

except ValueError as e:
    print("Error:", e)
