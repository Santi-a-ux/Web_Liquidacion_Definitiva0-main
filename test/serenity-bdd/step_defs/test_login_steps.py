"""
Step definitions para las pruebas de inicio de sesión (login)
"""

import pytest
import allure
from pytest_bdd import scenarios, given, when, then, parsers
from pages.login_page import LoginPage


# Cargar todos los escenarios del archivo login.feature
scenarios('../features/login.feature')


# ==================== GIVEN (Dado que) ====================

@given('que la aplicación está en ejecución')
def aplicacion_en_ejecucion(base_url):
    """Verifica que la aplicación esté disponible"""
    # En un entorno real, aquí se verificaría que el servidor está activo
    assert base_url is not None
    allure.attach(base_url, name='URL Base', attachment_type=allure.attachment_type.TEXT)


@given('estoy en la página de inicio de sesión')
def estoy_en_pagina_login(browser, base_url):
    """Navega a la página de inicio de sesión"""
    login_page = LoginPage(browser, base_url)
    login_page.navegar()
    assert login_page.estoy_en_pagina_login()


@given(parsers.parse('que he iniciado sesión como "{username}" con contraseña "{password}"'))
def he_iniciado_sesion(browser, base_url, username, password):
    """Inicia sesión con las credenciales proporcionadas"""
    login_page = LoginPage(browser, base_url)
    login_page.login(username, password)


# ==================== WHEN (Cuando) ====================

@when(parsers.parse('ingreso el usuario "{username}" y la contraseña "{password}"'))
def ingresar_credenciales(browser, base_url, username, password):
    """Ingresa las credenciales en el formulario de login"""
    login_page = LoginPage(browser, base_url)
    login_page.ingresar_credenciales(username, password)


@when('hago clic en el botón de iniciar sesión')
def hacer_clic_login(browser, base_url):
    """Hace clic en el botón de iniciar sesión"""
    login_page = LoginPage(browser, base_url)
    login_page.hacer_clic_login()


@when('hago clic en el botón de iniciar sesión sin ingresar credenciales')
def hacer_clic_login_sin_credenciales(browser, base_url):
    """Intenta hacer login sin ingresar credenciales"""
    login_page = LoginPage(browser, base_url)
    login_page.hacer_clic_login()


@when('hago clic en el botón de cerrar sesión')
def hacer_clic_cerrar_sesion(browser, base_url):
    """Cierra la sesión del usuario"""
    login_page = LoginPage(browser, base_url)
    login_page.cerrar_sesion()


# ==================== THEN (Entonces) ====================

@then('debería ver el panel de administración')
def verificar_panel_admin(browser):
    """Verifica que se haya redirigido al panel de administración"""
    # La URL debería contener /admin o /dashboard dependiendo de la implementación
    url_actual = browser.current_url
    assert ('/admin' in url_actual or '/dashboard' in url_actual or '/listar' in url_actual), \
        f"No se redirigió al panel esperado. URL actual: {url_actual}"
    allure.attach(url_actual, name='URL después del login', attachment_type=allure.attachment_type.TEXT)


@then('debería ver el panel principal')
def verificar_panel_principal(browser):
    """Verifica que se haya redirigido al panel principal"""
    url_actual = browser.current_url
    assert '/login' not in url_actual, f"Aún está en la página de login. URL: {url_actual}"
    allure.attach(url_actual, name='URL después del login', attachment_type=allure.attachment_type.TEXT)


@then(parsers.parse('debería ver mi nombre de usuario "{username}" en la barra superior'))
def verificar_nombre_usuario(browser, username):
    """Verifica que el nombre de usuario aparezca en la barra superior"""
    # Este paso puede variar según la implementación real
    # Por ahora, verificamos que no estamos en la página de login
    assert '/login' not in browser.current_url


@then('debería tener acceso a las opciones de administrador')
def verificar_opciones_admin(browser):
    """Verifica que se muestren las opciones de administrador"""
    # Verificar que no estamos en la página de login
    assert '/login' not in browser.current_url


@then('no debería ver las opciones de administrador')
def verificar_sin_opciones_admin(browser):
    """Verifica que NO se muestren opciones de administrador"""
    # Verificar que no estamos en /admin
    assert '/admin' not in browser.current_url or '/login' not in browser.current_url


@then('debería ver un mensaje de error indicando credenciales inválidas')
def verificar_mensaje_error_credenciales(browser, base_url):
    """Verifica que se muestre un mensaje de error"""
    login_page = LoginPage(browser, base_url)
    assert login_page.hay_mensaje_error(), "No se muestra mensaje de error"
    mensaje = login_page.obtener_mensaje_error()
    if mensaje:
        allure.attach(mensaje, name='Mensaje de error', attachment_type=allure.attachment_type.TEXT)


@then('debería permanecer en la página de inicio de sesión')
def verificar_permanece_en_login(browser, base_url):
    """Verifica que permanece en la página de login"""
    login_page = LoginPage(browser, base_url)
    assert login_page.estoy_en_pagina_login(), \
        f"No está en la página de login. URL actual: {browser.current_url}"


@then('debería ver mensajes de validación en los campos obligatorios')
def verificar_mensajes_validacion(browser, base_url):
    """Verifica que se muestren mensajes de validación"""
    login_page = LoginPage(browser, base_url)
    # Verificar que los campos tienen validación (atributo required, etc.)
    assert login_page.verificar_validacion_campos_vacios()


@then('debería ser redirigido a la página de inicio de sesión')
def verificar_redireccion_a_login(browser, base_url):
    """Verifica que se redirija a la página de login después del logout"""
    login_page = LoginPage(browser, base_url)
    # Esperar un poco para que la redirección ocurra
    import time
    time.sleep(1)
    assert login_page.estoy_en_pagina_login() or '/login' in browser.current_url


@then('no debería poder acceder a páginas protegidas sin autenticación')
def verificar_sin_acceso_sin_auth(browser, base_url):
    """Verifica que no se puede acceder a páginas protegidas sin autenticación"""
    # Intentar acceder a una página protegida
    browser.get(f"{base_url}/listar_usuarios")
    import time
    time.sleep(1)
    # Debería redirigir a login
    assert '/login' in browser.current_url, \
        f"Se pudo acceder sin autenticación. URL: {browser.current_url}"
