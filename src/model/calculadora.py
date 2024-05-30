from datetime import datetime

class CalculadoraLiquidacion:
    def __init__(self, valor_uvt=39205):
        self.valor_uvt = valor_uvt

    def calcular_resultados_prueba(self, salario_basico, fecha_inicio_labores, fecha_ultimas_vacaciones, dias_acumulados_vacaciones):
        # Calcula los días trabajados y el tiempo trabajado en años
        fecha_inicio = datetime.strptime(fecha_inicio_labores, "%d/%m/%Y")
        fecha_ultimas_vacaciones = datetime.strptime(fecha_ultimas_vacaciones, "%d/%m/%Y")
        dias_trabajados = (fecha_ultimas_vacaciones - fecha_inicio).days
        tiempo_trabajado_anos = dias_trabajados / 365
        indemnizacion = self.calcular_indemnizacion(salario_basico, tiempo_trabajado_anos)
        vacaciones = self.calcular_vacaciones(salario_basico, dias_trabajados)
        cesantias = self.calcular_cesantias(salario_basico, dias_trabajados)
        intereses_cesantias = self.calcular_intereses_cesantias(cesantias, dias_acumulados_vacaciones)
        primas = self.calcular_prima(salario_basico, dias_trabajados)
        retencion_fuente = self.calcular_retencion(indemnizacion + vacaciones + cesantias + intereses_cesantias + primas)
        total_pagar = indemnizacion + vacaciones + cesantias + intereses_cesantias + primas - retencion_fuente
        return indemnizacion, vacaciones, cesantias, intereses_cesantias, primas, retencion_fuente, total_pagar

    def calcular_indemnizacion(self, salario_basico, tiempo_trabajado_anos):
        meses_maximos = 12
        dias_por_anio = 20
        dias_maximos = meses_maximos * dias_por_anio
        dias_indemnizacion = min(tiempo_trabajado_anos * dias_por_anio, dias_maximos)
        indemnizacion = (salario_basico * dias_indemnizacion) / 30 
        return round(indemnizacion, 2)

    def calcular_vacaciones(self, salario_mensual, dias_trabajados):
        if dias_trabajados < 0:
            raise ValueError("Los días trabajados no pueden ser negativos")
        valor_vacaciones = (salario_mensual * dias_trabajados) / 720
        return round(valor_vacaciones, 2)

    def calcular_cesantias(self, salario_mensual, dias_trabajados):
        if dias_trabajados < 0:
            raise ValueError("Los días trabajados no pueden ser negativos")
        cesantias = (salario_mensual * dias_trabajados) / 360
        return round(cesantias, 2)

    def calcular_intereses_cesantias(self, cesantias, dias_trabajados):
        if cesantias < 0:
            raise ValueError("El valor de las cesantías no puede ser negativo")
        if dias_trabajados < 0:
            raise ValueError("Los días trabajados no pueden ser negativos")
        intereses_cesantias = (cesantias * dias_trabajados * 0.12) / 360
        return round(intereses_cesantias, 2)

    def calcular_prima(self, salario_mensual, dias_trabajados):
        if dias_trabajados < 0:
            raise ValueError("Los días trabajados no pueden ser negativos")
        prima = salario_mensual * (dias_trabajados / 360)
        return round(prima, 2)

    def calcular_retencion(self, salario_basico):
        if not isinstance(salario_basico, (int, float)):
            raise ValueError("El salario básico debe ser un número")
        retencion = 0
        salario_basico = float(salario_basico)
        ingreso_uvt = salario_basico / self.valor_uvt

        if ingreso_uvt <= 95:
            pass
        elif ingreso_uvt <= 150:
            base_uvt = ingreso_uvt - 95
            retencion = base_uvt * 0.19 * self.valor_uvt
        elif ingreso_uvt <= 360:
            base_uvt = ingreso_uvt - 150
            retencion = base_uvt * 0.28 * self.valor_uvt + 10 * self.valor_uvt
        elif ingreso_uvt <= 640:
            base_uvt = ingreso_uvt - 360
            retencion = base_uvt * 0.33 * self.valor_uvt + 69 * self.valor_uvt
        elif ingreso_uvt <= 945:
            base_uvt = ingreso_uvt - 640
            retencion = base_uvt * 0.35 * self.valor_uvt + 162 * self.valor_uvt
        elif ingreso_uvt <= 2300:
            base_uvt = ingreso_uvt - 945
            retencion = base_uvt * 0.37 * self.valor_uvt + 268 * self.valor_uvt
        else:
            base_uvt = ingreso_uvt - 2300
            retencion = base_uvt * 0.39 * self.valor_uvt + 770 * self.valor_uvt
        return round(retencion, 2)
    
    
    
