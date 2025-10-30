"""
Configuración de pytest para pruebas SerenityBDD
Proporciona fixtures y configuración global para las pruebas
"""

import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope='function')
def browser():
    """
    Fixture que proporciona una instancia del navegador para cada prueba.
    Se cierra automáticamente después de cada prueba.
    """
    # Configurar opciones de Chrome
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Ejecutar sin interfaz gráfica
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    
    # Inicializar el driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    
    yield driver
    
    # Tomar captura de pantalla si la prueba falla
    if hasattr(pytest, 'last_test_failed') and pytest.last_test_failed:
        allure.attach(
            driver.get_screenshot_as_png(),
            name='screenshot_on_failure',
            attachment_type=allure.attachment_type.PNG
        )
    
    # Cerrar el navegador
    driver.quit()


@pytest.fixture(scope='session')
def base_url():
    """
    Fixture que proporciona la URL base de la aplicación.
    """
    return "http://127.0.0.1:8080"


@pytest.fixture(scope='function')
def admin_credentials():
    """
    Fixture que proporciona las credenciales del administrador.
    """
    return {
        'username': 'admin',
        'password': 'admin123'
    }


@pytest.fixture(scope='function')
def assistant_credentials():
    """
    Fixture que proporciona las credenciales del asistente.
    """
    return {
        'username': 'asistente',
        'password': 'asistente123'
    }


@pytest.fixture(scope='function')
def empleado_valido():
    """
    Fixture que proporciona datos de un empleado válido para pruebas.
    """
    import time
    timestamp = int(time.time())
    
    return {
        'nombre': 'Juan',
        'apellido': 'Pérez',
        'documento': f'{timestamp}',
        'correo': f'juan.perez.{timestamp}@example.com',
        'telefono': '3001234567',
        'direccion': 'Calle 123 #45-67',
        'cargo': 'Desarrollador',
        'salario': '3000000',
        'fecha_ingreso': '2024-01-01'
    }


# Hook para capturar información de la prueba
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook para capturar el resultado de la prueba.
    Usado para tomar capturas de pantalla en caso de fallo.
    """
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == 'call' and rep.failed:
        pytest.last_test_failed = True
    else:
        pytest.last_test_failed = False


def pytest_configure(config):
    """
    Hook de configuración que se ejecuta antes de todas las pruebas.
    """
    # Configurar Allure
    config.addinivalue_line(
        "markers", "feature: Marca para features de Allure"
    )
    config.addinivalue_line(
        "markers", "story: Marca para stories de Allure"
    )
    config.addinivalue_line(
        "markers", "severity: Marca para severity de Allure"
    )


def pytest_bdd_after_scenario(request, feature, scenario):
    """
    Hook que se ejecuta después de cada escenario BDD.
    """
    # Agregar información del escenario a Allure
    allure.dynamic.feature(feature.name)
    allure.dynamic.story(scenario.name)


def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    """
    Hook que se ejecuta cuando un paso BDD falla.
    """
    # Adjuntar información del error a Allure
    allure.attach(
        str(exception),
        name='Error Details',
        attachment_type=allure.attachment_type.TEXT
    )
