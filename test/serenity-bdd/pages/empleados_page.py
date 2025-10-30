"""
Page Object para la página de gestión de empleados
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class EmpleadosPage:
    """Representa la página de gestión de empleados"""
    
    def __init__(self, driver, base_url="http://127.0.0.1:8080"):
        self.driver = driver
        self.base_url = base_url
        self.url_agregar = f"{base_url}/agregar_usuario"
        self.url_listar = f"{base_url}/listar_usuarios"
        self.url_consultar = f"{base_url}/consultar"
        
        # Localizadores de formulario
        self.nombre_input = (By.NAME, "nombre")
        self.apellido_input = (By.NAME, "apellido")
        self.documento_input = (By.NAME, "documento")
        self.correo_input = (By.NAME, "correo")
        self.telefono_input = (By.NAME, "telefono")
        self.direccion_input = (By.NAME, "direccion")
        self.cargo_input = (By.NAME, "cargo")
        self.salario_input = (By.NAME, "salario")
        self.fecha_ingreso_input = (By.NAME, "fecha_ingreso")
        self.submit_button = (By.CSS_SELECTOR, "button[type='submit']")
        
        # Localizadores de mensajes
        self.success_message = (By.CLASS_NAME, "alert-success")
        self.error_message = (By.CLASS_NAME, "alert-danger")
        
        # Localizadores de lista
        self.employee_table = (By.TAG_NAME, "table")
        self.employee_rows = (By.CSS_SELECTOR, "table tbody tr")
    
    @allure.step("Navegar a la página de agregar empleado")
    def navegar_a_agregar(self):
        """Navega a la página de agregar empleado"""
        self.driver.get(self.url_agregar)
        self._esperar_formulario()
    
    @allure.step("Navegar a la lista de empleados")
    def navegar_a_listar(self):
        """Navega a la página de lista de empleados"""
        self.driver.get(self.url_listar)
    
    @allure.step("Llenar formulario de empleado con datos: {datos}")
    def llenar_formulario(self, datos):
        """
        Llena el formulario con los datos del empleado
        
        Args:
            datos: Diccionario con los datos del empleado
        """
        campos = {
            'nombre': self.nombre_input,
            'apellido': self.apellido_input,
            'documento': self.documento_input,
            'correo': self.correo_input,
            'telefono': self.telefono_input,
            'direccion': self.direccion_input,
            'cargo': self.cargo_input,
            'salario': self.salario_input,
            'fecha_ingreso': self.fecha_ingreso_input
        }
        
        for campo, locator in campos.items():
            if campo in datos:
                element = self.driver.find_element(*locator)
                element.clear()
                element.send_keys(datos[campo])
    
    @allure.step("Enviar formulario")
    def enviar_formulario(self):
        """Envía el formulario"""
        button = self.driver.find_element(*self.submit_button)
        button.click()
    
    @allure.step("Agregar empleado completo")
    def agregar_empleado(self, datos):
        """Proceso completo de agregar un empleado"""
        self.navegar_a_agregar()
        self.llenar_formulario(datos)
        self.enviar_formulario()
    
    @allure.step("Obtener mensaje de éxito")
    def obtener_mensaje_exito(self):
        """Obtiene el mensaje de éxito mostrado"""
        try:
            success = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.success_message)
            )
            return success.text
        except:
            return None
    
    @allure.step("Obtener mensaje de error")
    def obtener_mensaje_error(self):
        """Obtiene el mensaje de error mostrado"""
        try:
            error = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.error_message)
            )
            return error.text
        except:
            return None
    
    @allure.step("Verificar si empleado está en la lista")
    def empleado_esta_en_lista(self, documento):
        """Verifica si un empleado aparece en la lista"""
        self.navegar_a_listar()
        try:
            rows = self.driver.find_elements(*self.employee_rows)
            for row in rows:
                if documento in row.text:
                    return True
            return False
        except:
            return False
    
    @allure.step("Buscar empleado por documento: {documento}")
    def buscar_empleado(self, documento):
        """Busca un empleado por número de documento"""
        # Navegar a consultar con el documento
        self.driver.get(f"{self.url_consultar}?documento={documento}")
    
    @allure.step("Obtener datos del empleado mostrado")
    def obtener_datos_empleado(self):
        """Obtiene los datos del empleado mostrado en pantalla"""
        # Implementación básica - puede ser personalizada según la UI real
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "employee-info"))
            )
            return True
        except:
            return False
    
    @allure.step("Contar empleados en la lista")
    def contar_empleados(self):
        """Cuenta el número de empleados en la lista"""
        try:
            rows = self.driver.find_elements(*self.employee_rows)
            return len(rows)
        except:
            return 0
    
    def _esperar_formulario(self):
        """Espera a que el formulario cargue"""
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.nombre_input)
        )
