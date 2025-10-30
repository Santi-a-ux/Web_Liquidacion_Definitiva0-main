"""
Ejemplo de prueba simple usando SerenityBDD con pytest-bdd
Este archivo demuestra cómo usar el patrón sin archivos .feature
"""

import pytest
import allure
from pages.login_page import LoginPage
from tasks.login_task import LoginTask


@allure.feature('Inicio de Sesión')
@allure.story('Login de Usuario')
@allure.severity(allure.severity_level.CRITICAL)
class TestLoginSimple:
    """Pruebas simples de login sin usar archivos .feature"""
    
    @allure.title('Login exitoso con credenciales de administrador')
    @allure.description('Verifica que un administrador puede iniciar sesión correctamente')
    @pytest.mark.humo
    @pytest.mark.critico
    def test_login_admin_exitoso(self, browser, base_url, admin_credentials):
        """Prueba login exitoso como administrador"""
        
        with allure.step('Paso 1: Crear tarea de login'):
            login_task = LoginTask(browser, base_url)
        
        with allure.step('Paso 2: Realizar login como administrador'):
            login_task.realizar_login(
                admin_credentials['username'],
                admin_credentials['password']
            )
        
        with allure.step('Paso 3: Verificar que el login fue exitoso'):
            assert login_task.verificar_login_exitoso()
        
        with allure.step('Paso 4: Verificar URL contiene dashboard o listar'):
            url = browser.current_url
            assert ('/dashboard' in url or '/listar' in url or '/admin' in url), \
                f"URL inesperada después del login: {url}"
    
    @allure.title('Login con credenciales incorrectas')
    @allure.description('Verifica que se muestra error con credenciales incorrectas')
    @pytest.mark.login
    def test_login_credenciales_incorrectas(self, browser, base_url):
        """Prueba login con credenciales incorrectas"""
        
        with allure.step('Paso 1: Crear página de login'):
            login_page = LoginPage(browser, base_url)
        
        with allure.step('Paso 2: Navegar a la página de login'):
            login_page.navegar()
        
        with allure.step('Paso 3: Ingresar credenciales incorrectas'):
            login_page.ingresar_credenciales('admin', 'password_incorrecto')
        
        with allure.step('Paso 4: Hacer clic en botón de login'):
            login_page.hacer_clic_login()
        
        with allure.step('Paso 5: Verificar que se muestra mensaje de error'):
            # Esperar un poco para que el error aparezca
            import time
            time.sleep(1)
            # Verificar que seguimos en la página de login
            assert login_page.estoy_en_pagina_login(), \
                "No permanece en la página de login después del error"


@allure.feature('Inicio de Sesión')
@allure.story('Logout de Usuario')
@allure.severity(allure.severity_level.NORMAL)
class TestLogout:
    """Pruebas de cierre de sesión"""
    
    @allure.title('Cerrar sesión exitosamente')
    @allure.description('Verifica que un usuario puede cerrar sesión correctamente')
    @pytest.mark.login
    def test_logout_exitoso(self, browser, base_url, admin_credentials):
        """Prueba logout exitoso"""
        
        with allure.step('Paso 1: Iniciar sesión'):
            login_task = LoginTask(browser, base_url)
            login_task.realizar_login(
                admin_credentials['username'],
                admin_credentials['password']
            )
        
        with allure.step('Paso 2: Verificar login exitoso'):
            assert login_task.verificar_login_exitoso()
        
        with allure.step('Paso 3: Cerrar sesión'):
            login_page = LoginPage(browser, base_url)
            login_page.cerrar_sesion()
        
        with allure.step('Paso 4: Verificar redirección a página de login'):
            import time
            time.sleep(1)
            assert '/login' in browser.current_url, \
                f"No redirigió a login después del logout. URL: {browser.current_url}"
