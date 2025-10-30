"""
Page Object para la página de inicio de sesión
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class LoginPage:
    """Representa la página de inicio de sesión del sistema"""
    
    def __init__(self, driver, base_url="http://127.0.0.1:8080"):
        self.driver = driver
        self.base_url = base_url
        self.url = f"{base_url}/login"
        
        # Localizadores de elementos
        self.username_input = (By.NAME, "usuario")
        self.password_input = (By.NAME, "clave")
        self.login_button = (By.CSS_SELECTOR, "button[type='submit']")
        self.error_message = (By.CLASS_NAME, "alert-danger")
        self.logout_button = (By.LINK_TEXT, "Cerrar Sesión")
    
    @allure.step("Navegar a la página de inicio de sesión")
    def navegar(self):
        """Navega a la página de login"""
        self.driver.get(self.url)
        self._esperar_carga_pagina()
    
    @allure.step("Ingresar credenciales: usuario='{username}'")
    def ingresar_credenciales(self, username, password):
        """Ingresa el nombre de usuario y contraseña"""
        username_field = self.driver.find_element(*self.username_input)
        password_field = self.driver.find_element(*self.password_input)
        
        username_field.clear()
        username_field.send_keys(username)
        
        password_field.clear()
        password_field.send_keys(password)
    
    @allure.step("Hacer clic en el botón de iniciar sesión")
    def hacer_clic_login(self):
        """Hace clic en el botón de login"""
        button = self.driver.find_element(*self.login_button)
        button.click()
    
    @allure.step("Iniciar sesión con usuario='{username}'")
    def login(self, username, password):
        """Realiza el proceso completo de login"""
        self.navegar()
        self.ingresar_credenciales(username, password)
        self.hacer_clic_login()
    
    @allure.step("Verificar si estoy en la página de login")
    def estoy_en_pagina_login(self):
        """Verifica si estamos en la página de login"""
        return "/login" in self.driver.current_url
    
    @allure.step("Obtener mensaje de error")
    def obtener_mensaje_error(self):
        """Obtiene el mensaje de error mostrado"""
        try:
            error_element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.error_message)
            )
            return error_element.text
        except:
            return None
    
    @allure.step("Verificar si hay mensaje de error")
    def hay_mensaje_error(self):
        """Verifica si se muestra un mensaje de error"""
        return self.obtener_mensaje_error() is not None
    
    @allure.step("Cerrar sesión")
    def cerrar_sesion(self):
        """Cierra la sesión del usuario"""
        try:
            logout = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.logout_button)
            )
            logout.click()
        except:
            # Si no hay botón de logout, ir directamente a /logout
            self.driver.get(f"{self.base_url}/logout")
    
    @allure.step("Obtener URL actual")
    def obtener_url_actual(self):
        """Obtiene la URL actual del navegador"""
        return self.driver.current_url
    
    @allure.step("Verificar campos vacíos")
    def verificar_validacion_campos_vacios(self):
        """Verifica si hay validación de campos vacíos"""
        username_field = self.driver.find_element(*self.username_input)
        password_field = self.driver.find_element(*self.password_input)
        
        # Verificar atributo 'required'
        return (username_field.get_attribute('required') is not None or
                password_field.get_attribute('required') is not None)
    
    def _esperar_carga_pagina(self):
        """Espera a que la página cargue completamente"""
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.username_input)
        )
