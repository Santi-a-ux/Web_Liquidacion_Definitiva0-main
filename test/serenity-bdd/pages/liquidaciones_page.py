"""
Page Object para la página de gestión de liquidaciones
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import allure


class LiquidacionesPage:
    """Representa la página de gestión de liquidaciones"""
    
    def __init__(self, driver, base_url="http://127.0.0.1:8080"):
        self.driver = driver
        self.base_url = base_url
        self.url_crear = f"{base_url}/crear_liquidacion"
        self.url_listar = f"{base_url}/listar_liquidaciones"
        self.url_consultar = f"{base_url}/consultar_liquidacion"
        
        # Localizadores de formulario
        self.documento_input = (By.NAME, "documento")
        self.tipo_retiro_select = (By.NAME, "tipo_retiro")
        self.fecha_retiro_input = (By.NAME, "fecha_retiro")
        self.dias_trabajados_input = (By.NAME, "dias_trabajados")
        self.auxilio_transporte_checkbox = (By.NAME, "auxilio_transporte")
        self.calcular_button = (By.ID, "calcular")
        self.submit_button = (By.CSS_SELECTOR, "button[type='submit']")
        
        # Localizadores de resultados
        self.resumen_liquidacion = (By.CLASS_NAME, "liquidacion-resumen")
        self.cesantias = (By.ID, "cesantias")
        self.intereses_cesantias = (By.ID, "intereses_cesantias")
        self.prima_servicios = (By.ID, "prima_servicios")
        self.vacaciones = (By.ID, "vacaciones")
        self.indemnizacion = (By.ID, "indemnizacion")
        self.total_liquidacion = (By.ID, "total_liquidacion")
        
        # Localizadores de mensajes
        self.success_message = (By.CLASS_NAME, "alert-success")
        self.error_message = (By.CLASS_NAME, "alert-danger")
        
        # Localizadores de lista
        self.liquidacion_table = (By.TAG_NAME, "table")
        self.liquidacion_rows = (By.CSS_SELECTOR, "table tbody tr")
    
    @allure.step("Navegar a crear liquidación")
    def navegar_a_crear(self):
        """Navega a la página de crear liquidación"""
        self.driver.get(self.url_crear)
        self._esperar_formulario()
    
    @allure.step("Navegar a lista de liquidaciones")
    def navegar_a_listar(self):
        """Navega a la lista de liquidaciones"""
        self.driver.get(self.url_listar)
    
    @allure.step("Llenar formulario de liquidación")
    def llenar_formulario(self, datos):
        """
        Llena el formulario con los datos de la liquidación
        
        Args:
            datos: Diccionario con los datos de la liquidación
        """
        if 'documento' in datos:
            doc_field = self.driver.find_element(*self.documento_input)
            doc_field.clear()
            doc_field.send_keys(datos['documento'])
        
        if 'tipo_retiro' in datos:
            tipo_select = Select(self.driver.find_element(*self.tipo_retiro_select))
            tipo_select.select_by_visible_text(datos['tipo_retiro'])
        
        if 'fecha_retiro' in datos:
            fecha_field = self.driver.find_element(*self.fecha_retiro_input)
            fecha_field.clear()
            fecha_field.send_keys(datos['fecha_retiro'])
        
        if 'dias_trabajados' in datos:
            dias_field = self.driver.find_element(*self.dias_trabajados_input)
            dias_field.clear()
            dias_field.send_keys(datos['dias_trabajados'])
        
        if 'auxilio_transporte' in datos and datos['auxilio_transporte'].lower() == 'si':
            checkbox = self.driver.find_element(*self.auxilio_transporte_checkbox)
            if not checkbox.is_selected():
                checkbox.click()
    
    @allure.step("Calcular liquidación")
    def calcular_liquidacion(self):
        """Hace clic en el botón de calcular"""
        button = self.driver.find_element(*self.calcular_button)
        button.click()
        self._esperar_resultados()
    
    @allure.step("Generar liquidación")
    def generar_liquidacion(self):
        """Genera/guarda la liquidación"""
        button = self.driver.find_element(*self.submit_button)
        button.click()
    
    @allure.step("Crear liquidación completa")
    def crear_liquidacion(self, datos):
        """Proceso completo de crear una liquidación"""
        self.navegar_a_crear()
        self.llenar_formulario(datos)
        self.calcular_liquidacion()
        self.generar_liquidacion()
    
    @allure.step("Obtener resumen de liquidación")
    def obtener_resumen(self):
        """Obtiene el resumen de la liquidación calculada"""
        try:
            resumen = {}
            resumen['cesantias'] = self._obtener_valor_campo(self.cesantias)
            resumen['intereses_cesantias'] = self._obtener_valor_campo(self.intereses_cesantias)
            resumen['prima_servicios'] = self._obtener_valor_campo(self.prima_servicios)
            resumen['vacaciones'] = self._obtener_valor_campo(self.vacaciones)
            resumen['indemnizacion'] = self._obtener_valor_campo(self.indemnizacion)
            resumen['total'] = self._obtener_valor_campo(self.total_liquidacion)
            return resumen
        except:
            return None
    
    @allure.step("Verificar si se muestra el resumen")
    def hay_resumen_visible(self):
        """Verifica si se muestra el resumen de liquidación"""
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.resumen_liquidacion)
            )
            return True
        except:
            return False
    
    @allure.step("Verificar concepto en liquidación: {concepto}")
    def concepto_esta_incluido(self, concepto):
        """Verifica si un concepto específico está incluido en la liquidación"""
        localizadores = {
            'cesantías': self.cesantias,
            'cesantias': self.cesantias,
            'intereses sobre cesantías': self.intereses_cesantias,
            'intereses': self.intereses_cesantias,
            'prima de servicios': self.prima_servicios,
            'prima': self.prima_servicios,
            'vacaciones': self.vacaciones,
            'indemnización': self.indemnizacion,
            'indemnizacion': self.indemnizacion
        }
        
        concepto_lower = concepto.lower()
        if concepto_lower in localizadores:
            try:
                element = self.driver.find_element(*localizadores[concepto_lower])
                return element.is_displayed()
            except:
                return False
        return False
    
    @allure.step("Obtener total de liquidación")
    def obtener_total(self):
        """Obtiene el valor total de la liquidación"""
        return self._obtener_valor_campo(self.total_liquidacion)
    
    @allure.step("Buscar liquidación por ID: {liquidacion_id}")
    def buscar_liquidacion(self, liquidacion_id):
        """Busca una liquidación por su ID"""
        self.driver.get(f"{self.url_consultar}?id={liquidacion_id}")
    
    @allure.step("Contar liquidaciones en la lista")
    def contar_liquidaciones(self):
        """Cuenta el número de liquidaciones en la lista"""
        try:
            rows = self.driver.find_elements(*self.liquidacion_rows)
            return len(rows)
        except:
            return 0
    
    @allure.step("Obtener mensaje de éxito")
    def obtener_mensaje_exito(self):
        """Obtiene el mensaje de éxito"""
        try:
            success = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.success_message)
            )
            return success.text
        except:
            return None
    
    @allure.step("Obtener mensaje de error")
    def obtener_mensaje_error(self):
        """Obtiene el mensaje de error"""
        try:
            error = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.error_message)
            )
            return error.text
        except:
            return None
    
    def _obtener_valor_campo(self, locator):
        """Obtiene el valor de un campo de la liquidación"""
        try:
            element = self.driver.find_element(*locator)
            return element.text or element.get_attribute('value')
        except:
            return None
    
    def _esperar_formulario(self):
        """Espera a que el formulario cargue"""
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.documento_input)
        )
    
    def _esperar_resultados(self):
        """Espera a que los resultados se muestren"""
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.resumen_liquidacion)
        )
