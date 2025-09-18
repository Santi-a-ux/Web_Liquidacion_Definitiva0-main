from __future__ import annotations

from datetime import datetime
from typing import Tuple

# Constantes para evitar números mágicos y mejorar legibilidad (SonarQube)
DAYS_PER_YEAR: float = 365.0
DAYS_PER_MONTH: float = 30.0
# Reglas esperadas por los tests
INDEMN_DAYS_PER_YEAR: float = 20.0
MAX_INDEMN_DAYS: float = 240.0
DATE_FORMAT_UI: str = "%d/%m/%Y"

# Mensajes de error reutilizables
NEGATIVE_DAYS_ERROR: str = "Los días trabajados no pueden ser negativos"
SALARY_POSITIVE_ERROR: str = "El salario debe ser positivo"
NEGATIVE_TIME_ERROR: str = "El tiempo trabajado no puede ser negativo"


class CalculadoraLiquidacion:
    """
    Cálculos de liquidación con tipado, validaciones y sin números mágicos.
    Cumple reglas comunes de SonarQube (nombres claros, constantes, validaciones).
    """

    def __init__(self, valor_uvt: float = 39205) -> None:
        self.valor_uvt: float = float(valor_uvt)

    def calcular_resultados_prueba(
        self,
        salario_basico: float,
        fecha_inicio_labores: str,
        fecha_ultimas_vacaciones: str,
        dias_acumulados_vacaciones: int,
    ) -> Tuple[float, float, float, float, float, float, float]:
        """
        Método de apoyo usado en tests. Devuelve una tupla de 7 elementos en el orden:
        (indemnizacion, vacaciones, cesantias, intereses_cesantias, primas, retencion_fuente, total_pagar)
        """
        if salario_basico <= 0:
            raise ValueError(SALARY_POSITIVE_ERROR)

        fecha_inicio = datetime.strptime(fecha_inicio_labores, DATE_FORMAT_UI)
        fecha_ult = datetime.strptime(fecha_ultimas_vacaciones, DATE_FORMAT_UI)
        dias_trabajados = (fecha_ult - fecha_inicio).days
        if dias_trabajados < 0:
            raise ValueError(NEGATIVE_DAYS_ERROR)

        tiempo_trabajado_anos = dias_trabajados / DAYS_PER_YEAR

        indemnizacion = self.calcular_indemnizacion(salario_basico, tiempo_trabajado_anos)
        vacaciones = self.calcular_vacaciones(salario_basico, dias_trabajados)
        cesantias = self.calcular_cesantias(salario_basico, dias_trabajados)
        intereses_cesantias = self.calcular_intereses_cesantias(cesantias, dias_acumulados_vacaciones)
        primas = self.calcular_prima(salario_basico, dias_trabajados)
        retencion_fuente = self.calcular_retencion(
            indemnizacion + vacaciones + cesantias + intereses_cesantias + primas
        )
        total_pagar = indemnizacion + vacaciones + cesantias + intereses_cesantias + primas - retencion_fuente
        return (
            indemnizacion,
            vacaciones,
            cesantias,
            intereses_cesantias,
            primas,
            retencion_fuente,
            round(total_pagar, 2),
        )

    def calcular_indemnizacion(self, salario_mensual: float, tiempo_trabajado_anos: float) -> float:
        """
        Calcula la indemnización:
        - 20 días por año trabajado (prorrateado)
        - Tope máximo de 240 días en total
        Fórmula: (salario_mensual / 30) * min(20 * años, 240)
        """
        if salario_mensual <= 0:
            raise ValueError(SALARY_POSITIVE_ERROR)
        if tiempo_trabajado_anos < 0:
            raise ValueError(NEGATIVE_TIME_ERROR)

        salario_diario = salario_mensual / DAYS_PER_MONTH
        dias_indemnizacion = INDEMN_DAYS_PER_YEAR * tiempo_trabajado_anos
        dias_indemnizacion = min(dias_indemnizacion, MAX_INDEMN_DAYS)
        valor = salario_diario * dias_indemnizacion
        return round(valor, 2)

    def calcular_vacaciones(self, salario_mensual: float, dias_trabajados: int) -> float:
        if dias_trabajados < 0:
            raise ValueError(NEGATIVE_DAYS_ERROR)
        valor_vacaciones = (salario_mensual * dias_trabajados) / 720.0
        return round(valor_vacaciones, 2)

    def calcular_cesantias(self, salario_mensual: float, dias_trabajados: int) -> float:
        if dias_trabajados < 0:
            raise ValueError(NEGATIVE_DAYS_ERROR)
        cesantias = (salario_mensual * dias_trabajados) / 360.0
        return round(cesantias, 2)

    def calcular_intereses_cesantias(self, cesantias: float, dias_trabajados: int) -> float:
        if cesantias < 0:
            raise ValueError("El valor de las cesantías no puede ser negativo")
        if dias_trabajados < 0:
            raise ValueError(NEGATIVE_DAYS_ERROR)
        intereses_cesantias = (cesantias * dias_trabajados * 0.12) / 360.0
        return round(intereses_cesantias, 2)

    def calcular_prima(self, salario_mensual: float, dias_trabajados: int) -> float:
        if dias_trabajados < 0:
            raise ValueError(NEGATIVE_DAYS_ERROR)
        prima = salario_mensual * (dias_trabajados / 360.0)
        return round(prima, 2)

    def calcular_retencion(self, salario_basico: float) -> float:
        if not isinstance(salario_basico, (int, float)):
            raise ValueError("El salario básico debe ser un número")

        ingreso_uvt = float(salario_basico) / self.valor_uvt
        retencion = 0.0

        if ingreso_uvt <= 95:
            retencion = 0.0
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
