"""
Tarea de alto nivel para realizar login
"""

import allure
from pages.login_page import LoginPage


class LoginTask:
    """Tarea para realizar el proceso de inicio de sesión"""
    
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.login_page = LoginPage(driver, base_url)
    
    @allure.step("Realizar login como {username}")
    def realizar_login(self, username, password):
        """
        Realiza el proceso completo de inicio de sesión
        
        Args:
            username: Nombre de usuario
            password: Contraseña
        """
        with allure.step(f"Navegar a la página de login"):
            self.login_page.navegar()
        
        with allure.step(f"Ingresar credenciales para {username}"):
            self.login_page.ingresar_credenciales(username, password)
        
        with allure.step("Hacer clic en el botón de login"):
            self.login_page.hacer_clic_login()
        
        return self
    
    @allure.step("Verificar que el login fue exitoso")
    def verificar_login_exitoso(self):
        """Verifica que el login haya sido exitoso"""
        url_actual = self.driver.current_url
        assert '/login' not in url_actual, f"El login falló, aún en página de login: {url_actual}"
        return True
