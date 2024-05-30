import unittest
from datetime import datetime
import os
import sys
directorio_actual = os.path.dirname(os.path.abspath(__file__))
ruta_src = os.path.join(directorio_actual, '..', 'src')
sys.path.insert(0, ruta_src)
from model.calculadora import CalculadoraLiquidacion

class TestCalculadoraLiquidacion(unittest.TestCase):
    def setUp(self):
        self.calculadora = CalculadoraLiquidacion()

    def test_calculo_liquidacion(self):
        salario = 1500000
        fecha_inicio = "01/01/2022"
        fecha_fin = "01/01/2023"
        fecha_inicio_dt = datetime.strptime(fecha_inicio, "%d/%m/%Y")
        fecha_fin_dt = datetime.strptime(fecha_fin, "%d/%m/%Y")
        dias_trabajados = (fecha_fin_dt - fecha_inicio_dt).days
        tiempo_trabajado_anos = dias_trabajados / 365
        indemnizacion, _, _, _, _, _, _ = self.calculadora.calcular_resultados_prueba(
            salario_basico=salario,
            fecha_inicio_labores=fecha_inicio,
            fecha_ultimas_vacaciones=fecha_fin,
            dias_acumulados_vacaciones=0
    )
        meses_maximos = 12
        dias_por_anio = 20
        dias_maximos = meses_maximos * dias_por_anio
        dias_indemnizacion = min(tiempo_trabajado_anos * dias_por_anio, dias_maximos)
        liquidacion_esperada = round((salario * dias_indemnizacion) / 30, 2)
        self.assertEqual(indemnizacion, liquidacion_esperada)

    def test_calculo_indemnizacion(self):
        salario = 2500000
        meses_trabajados = 6
        tiempo_trabajado_anos = meses_trabajados / 12  
        valor_indemnizacion = self.calculadora.calcular_indemnizacion(salario, tiempo_trabajado_anos)
        valor_esperado = round(salario * tiempo_trabajado_anos * 20 / 30, 2)
        self.assertEqual(valor_indemnizacion, valor_esperado)

    def test_calculo_vacaciones(self):
        salario = 1500000
        dias_trabajados = 10
        result = self.calculadora.calcular_vacaciones(salario, dias_trabajados)
        self.assertAlmostEqual(result, 20833.33, places=2)

    def test_calculo_cesantias(self):
        salario_mensual = 3000000
        dias_trabajados = 15
        result = self.calculadora.calcular_cesantias(salario_mensual, dias_trabajados)
        self.assertEqual(result, 125000)

    def calcular_prima(self, salario_mensual, dias_trabajados):
        prima = salario_mensual * (dias_trabajados / 180)  
        return round(prima, 2)

    def test_calculo_retencion(self):
        ingreso_laboral = 5000000
        result = self.calculadora.calcular_retencion(ingreso_laboral)
        self.assertEqual(result, 242349.75)

    def test_formato_fecha_invalido_calculo_liquidacion(self):
        salario = 2000000
        fecha_inicio = "01-01-2022"
        fecha_fin = "15-01-2022"
        with self.assertRaises(ValueError):
            self.calculadora.calcular_resultados_prueba(salario, fecha_inicio, fecha_fin, 0)

    def test_calculo_intereses_cesantias_valor_negativo(self):
        calc = CalculadoraLiquidacion()
        cesantias = -10000
        vacaciones = 20000
        with self.assertRaises(ValueError):
            calc.calcular_intereses_cesantias(cesantias, vacaciones)

    def test_calculo_liquidacion_fecha_invalida(self):
        calc = CalculadoraLiquidacion()
        salario_basico = 500000
        fecha_inicio_labores = "01/01/2023"
        fecha_ultimas_vacaciones = "30/02/2023" 
        dias_acumulados_vacaciones = 10
        with self.assertRaises(ValueError):
            calc.calcular_resultados_prueba(salario_basico, fecha_inicio_labores, fecha_ultimas_vacaciones, dias_acumulados_vacaciones)

    class TestCalculadoraLiquidacion(unittest.TestCase):
        def test_motivo_invalido_calculo_indemnizacion(self):
            salario = 2000000
            meses_trabajados = 6
            tiempo_trabajado_anos = meses_trabajados / 12
            self.calculadora.calcular_indemnizacion(salario, tiempo_trabajado_anos)

    def test_dias_trabajados_negativos_calculo_vacaciones(self):
        salario_mensual = 2000000
        dias_trabajados = -5
        with self.assertRaises(ValueError):
            self.calculadora.calcular_vacaciones(salario_mensual, dias_trabajados)

    def test_dias_trabajados_negativos_calculo_cesantias(self):
        salario_mensual = 2000000
        dias_trabajados = -10
        with self.assertRaises(ValueError):
            self.calculadora.calcular_cesantias(salario_mensual, dias_trabajados)

    def test_formato_ingreso_laboral_invalido_calculo_retencion(self):
        ingreso_laboral = "5000000"
        with self.assertRaises(ValueError):
            self.calculadora.calcular_retencion(ingreso_laboral)

    def test_total_pagar_negativo_imprimir_resultados(self):
        pass

    def test_formato_fecha_inicio_invalido(self):
        with self.assertRaises(ValueError):
            self.calculadora.calcular_resultados_prueba(2000000, "01-01-2022", "01/01/2023", 0)

    def test_formato_fecha_ultimas_vacaciones_invalido(self):
        with self.assertRaises(ValueError):
            self.calculadora.calcular_resultados_prueba(2000000, "01/01/2022", "2023/01/01", 0)

    def test_calculo_indemnizacion_maximo_dias(self):
        salario = 2000000
        meses_trabajados = 20  
        tiempo_trabajado_anos = meses_trabajados / 12
        indemnizacion = self.calculadora.calcular_indemnizacion(salario, tiempo_trabajado_anos)
        meses_maximos = 12
        dias_por_anio = 20
        dias_maximos = meses_maximos * dias_por_anio
        dias_indemnizacion = min(tiempo_trabajado_anos * dias_por_anio, dias_maximos)
        indemnizacion_esperada = round((salario * dias_indemnizacion) / 30, 2)
        self.assertEqual(indemnizacion, indemnizacion_esperada)

    def test_salario_basico_negativo(self):
        with self.assertRaises(ValueError):
            self.calculadora.calcular_resultados_prueba(-2000000, "01/01/2022", "01/01/2023", 0)

    def test_dias_acumulados_vacaciones_negativos(self):
        with self.assertRaises(ValueError):
            self.calculadora.calcular_vacaciones(2000000, -10)

    def test_tipo_ingreso_laboral_invalido(self):
        with self.assertRaises(ValueError):
            self.calculadora.calcular_retencion("five million")

    def test_calculo_prima_dias_negativos(self):
        salario_mensual = 2000000
        dias_trabajados = -15
        with self.assertRaises(ValueError):
            self.calculadora.calcular_prima(salario_mensual, dias_trabajados)

    def test_calculo_retencion_maximo_rango(self):
        ingreso_laboral = 5000000000  
        valor_uvt = 39205 
        self.calculadora.valor_uvt = valor_uvt
        retencion = self.calculadora.calcular_retencion(ingreso_laboral)
        ingreso_uvt = ingreso_laboral / valor_uvt
        base_uvt = ingreso_uvt - 2300
        retencion_esperada = round(base_uvt * 0.39 * valor_uvt + 770 * valor_uvt, 2)
        self.assertEqual(retencion, retencion_esperada)

if __name__ == '__main__':
    unittest.main(verbosity=2)