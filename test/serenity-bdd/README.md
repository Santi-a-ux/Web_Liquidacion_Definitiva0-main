# Integración de Pruebas con Patrón SerenityBDD

## Descripción General

Este directorio contiene la implementación del **patrón de pruebas SerenityBDD** para el proyecto Web Liquidación Definitiva. SerenityBDD es un framework de automatización de pruebas que combina BDD (Behavior-Driven Development) con reportes detallados y documentación viva.

### Características Principales

- ✅ **BDD (Behavior-Driven Development)**: Escribe pruebas en lenguaje natural usando Gherkin
- ✅ **Reportes Detallados**: Genera reportes HTML ricos con capturas de pantalla y detalles de ejecución
- ✅ **Documentación Viva**: Las pruebas sirven como documentación ejecutable del sistema
- ✅ **Integración con pytest**: Compatible con el ecosistema de pruebas existente
- ✅ **Trazabilidad**: Vincula pruebas con requisitos de negocio

## Arquitectura de la Solución

En Python, implementamos el patrón SerenityBDD usando:

1. **pytest-bdd**: Para escribir pruebas en estilo BDD con archivos `.feature`
2. **Allure**: Para generar reportes detallados similares a SerenityBDD
3. **Patrón Screenplay**: Para organizar el código de prueba de manera mantenible

```
test/serenity-bdd/
├── features/              # Archivos .feature en Gherkin
│   ├── login.feature
│   ├── empleados.feature
│   └── liquidaciones.feature
├── step_defs/            # Definiciones de pasos (step definitions)
│   ├── __init__.py
│   ├── test_login_steps.py
│   ├── test_empleados_steps.py
│   └── test_liquidaciones_steps.py
├── pages/                # Page Objects (patrón Page Object Model)
│   ├── __init__.py
│   ├── login_page.py
│   ├── empleados_page.py
│   └── liquidaciones_page.py
├── tasks/                # Tareas de alto nivel (patrón Screenplay)
│   ├── __init__.py
│   ├── login_task.py
│   └── empleados_task.py
├── conftest.py           # Configuración de pytest y fixtures
├── pytest.ini            # Configuración de pytest-bdd
├── requirements.txt      # Dependencias Python
└── README.md            # Este archivo
```

## Instalación

### 1. Instalar Dependencias

```bash
cd test/serenity-bdd
pip install -r requirements.txt
```

### 2. Instalar Allure (para reportes)

**En Ubuntu/Debian:**
```bash
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure
```

**En macOS:**
```bash
brew install allure
```

**En Windows:**
```bash
scoop install allure
```

O descarga desde: https://github.com/allure-framework/allure2/releases

## Estructura de Archivos Feature

Los archivos `.feature` definen las pruebas en lenguaje natural usando Gherkin:

```gherkin
# Idioma: español
Característica: Inicio de Sesión
  Como usuario del sistema
  Quiero poder iniciar sesión
  Para acceder a las funcionalidades del sistema

  Escenario: Login exitoso como administrador
    Dado que estoy en la página de inicio de sesión
    Cuando ingreso el usuario "admin" y contraseña "admin123"
    Y hago clic en el botón de iniciar sesión
    Entonces debería ver el panel de administración
    Y debería ver un mensaje de bienvenida

  Escenario: Login fallido con credenciales incorrectas
    Dado que estoy en la página de inicio de sesión
    Cuando ingreso el usuario "admin" y contraseña "incorrecta"
    Y hago clic en el botón de iniciar sesión
    Entonces debería ver un mensaje de error
    Y debería permanecer en la página de inicio de sesión
```

## Definiciones de Pasos (Step Definitions)

Las definiciones de pasos conectan el lenguaje Gherkin con el código Python:

```python
from pytest_bdd import scenarios, given, when, then, parsers
from pages.login_page import LoginPage

scenarios('../features/login.feature')

@given('que estoy en la página de inicio de sesión')
def navegar_a_login(browser):
    login_page = LoginPage(browser)
    login_page.navegar()

@when(parsers.parse('ingreso el usuario "{username}" y contraseña "{password}"'))
def ingresar_credenciales(browser, username, password):
    login_page = LoginPage(browser)
    login_page.ingresar_credenciales(username, password)

@when('hago clic en el botón de iniciar sesión')
def hacer_clic_login(browser):
    login_page = LoginPage(browser)
    login_page.hacer_clic_login()

@then('debería ver el panel de administración')
def verificar_panel_admin(browser):
    assert '/admin' in browser.current_url
```

## Page Objects

Los Page Objects encapsulan la interacción con las páginas web:

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "http://127.0.0.1:8080/login"
        self.username_input = (By.NAME, "usuario")
        self.password_input = (By.NAME, "clave")
        self.login_button = (By.CSS_SELECTOR, "button[type='submit']")
    
    def navegar(self):
        self.driver.get(self.url)
    
    def ingresar_credenciales(self, username, password):
        self.driver.find_element(*self.username_input).send_keys(username)
        self.driver.find_element(*self.password_input).send_keys(password)
    
    def hacer_clic_login(self):
        self.driver.find_element(*self.login_button).click()
```

## Ejecutar Pruebas

### Ejecutar Todas las Pruebas

```bash
cd test/serenity-bdd
pytest
```

### Ejecutar Pruebas con Reportes Allure

```bash
# Ejecutar pruebas y generar datos de Allure
pytest --alluredir=allure-results

# Generar y abrir el reporte HTML
allure serve allure-results
```

### Ejecutar un Feature Específico

```bash
pytest --feature features/login.feature
```

### Ejecutar con Diferentes Niveles de Detalle

```bash
# Verbose (detallado)
pytest -v

# Muy verbose (muy detallado)
pytest -vv

# Con salida de print
pytest -s
```

## Reportes Allure

Los reportes Allure proporcionan:

- **Vista General**: Resumen de ejecución con gráficos
- **Suites**: Organización por features y escenarios
- **Gráficos**: Tendencias, distribución de estados, duración
- **Timeline**: Línea de tiempo de ejecución
- **Categorías**: Clasificación de fallos
- **Capturas de Pantalla**: Evidencia visual de las pruebas
- **Logs**: Detalles de ejecución paso a paso

### Ejemplo de Anotaciones Allure

```python
import allure

@allure.feature('Gestión de Empleados')
@allure.story('Agregar Empleado')
@allure.severity(allure.severity_level.CRITICAL)
@allure.title('Agregar empleado con datos válidos')
def test_agregar_empleado_valido():
    with allure.step('Navegar a la página de empleados'):
        # código...
    
    with allure.step('Llenar formulario con datos válidos'):
        # código...
    
    with allure.step('Enviar formulario'):
        # código...
    
    with allure.step('Verificar empleado creado'):
        # código...
```

## Integración con Patrón Screenplay

El patrón Screenplay se puede integrar con BDD:

```python
from pytest_bdd import scenarios, given, when, then
from test.screenplay.actors import AdminUser
from test.screenplay.abilities import BrowseTheWeb
from test.screenplay.tasks import Login

scenarios('../features/login.feature')

@given('que soy un usuario administrador')
def crear_admin(browser):
    admin = AdminUser()
    admin.who_can(BrowseTheWeb.using(browser))
    return admin

@when('intento iniciar sesión con mis credenciales')
def login_como_admin(admin):
    admin.attempts_to(
        Login.with_credentials(admin.username, admin.password)
    )

@then('debería acceder al sistema exitosamente')
def verificar_acceso_exitoso(admin):
    admin.should_see(
        TheUrl.current().contains('/dashboard')
    )
```

## Mejores Prácticas

### 1. Escribir Escenarios Claros

```gherkin
# ✅ BUENO: Específico y claro
Escenario: Agregar empleado con salario mensual
  Dado que estoy autenticado como administrador
  Cuando agrego un empleado con nombre "Juan Pérez" y salario "3000000"
  Entonces el empleado debería aparecer en la lista
  Y el salario debería mostrarse como "$3.000.000"

# ❌ MALO: Vago y confuso
Escenario: Prueba de empleado
  Dado que estoy en el sistema
  Cuando hago algo con empleados
  Entonces debería funcionar
```

### 2. Reutilizar Definiciones de Pasos

```python
# Usar parsers para parámetros
@when(parsers.parse('ingreso el {campo} con valor "{valor}"'))
def ingresar_campo(browser, campo, valor):
    # Implementación genérica
    pass

# En lugar de:
@when('ingreso el nombre')
@when('ingreso el apellido')
@when('ingreso el documento')
# ... uno para cada campo
```

### 3. Usar Background para Precondiciones Comunes

```gherkin
Característica: Gestión de Empleados

  Antecedentes:
    Dado que estoy autenticado como administrador
    Y estoy en la página de empleados

  Escenario: Agregar empleado
    Cuando completo el formulario de nuevo empleado
    # ...

  Escenario: Consultar empleado
    Cuando busco un empleado por documento
    # ...
```

### 4. Usar Tags para Organizar Pruebas

```gherkin
@humo @critico
Escenario: Login exitoso

@regresion @empleados
Escenario: Agregar empleado

# Ejecutar solo pruebas de humo:
# pytest -m humo
```

### 5. Mantener Escenarios Independientes

Cada escenario debe:
- Configurar su propio estado inicial
- No depender de otros escenarios
- Limpiar datos después de ejecutarse

## Comparación con Otros Frameworks

| Característica | SerenityBDD (Java) | pytest-bdd + Allure (Python) |
|---------------|-------------------|----------------------------|
| **Lenguaje** | Java | Python |
| **BDD** | ✅ Nativo | ✅ Via pytest-bdd |
| **Reportes** | ✅ SerenityBDD | ✅ Allure |
| **Screenplay** | ✅ Nativo | ✅ Implementación custom |
| **Page Objects** | ✅ Soportado | ✅ Soportado |
| **Integración CI/CD** | ✅ Buena | ✅ Excelente |
| **Curva de Aprendizaje** | Media-Alta | Media |

## Integración con CI/CD

### GitHub Actions

```yaml
name: Pruebas SerenityBDD

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Instalar Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    
    - name: Instalar dependencias
      run: |
        cd test/serenity-bdd
        pip install -r requirements.txt
    
    - name: Ejecutar pruebas
      run: |
        cd test/serenity-bdd
        pytest --alluredir=allure-results
    
    - name: Generar reporte Allure
      if: always()
      uses: simple-elf/allure-report-action@master
      with:
        allure_results: test/serenity-bdd/allure-results
        allure_history: allure-history
    
    - name: Publicar reporte
      if: always()
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: allure-history
```

## Solución de Problemas

### Error: "No se encuentran los archivos .feature"

**Solución:**
```bash
# Verificar que pytest.ini tiene:
[pytest]
python_files = test_*.py
python_classes = Test*
python_functions = test_*
bdd_features_base_dir = features/
```

### Error: "Step definition not found"

**Solución:**
- Verificar que el texto del step en Gherkin coincide exactamente con el decorador
- Usar `parsers.parse()` para parámetros dinámicos
- Asegurar que el archivo de step_defs se está importando correctamente

### Error: "Browser not found"

**Solución:**
```bash
# Instalar ChromeDriver
sudo apt-get install chromium-chromedriver

# O usar webdriver-manager
pip install webdriver-manager
```

### Reportes Allure no se generan

**Solución:**
```bash
# Verificar instalación de Allure
allure --version

# Reinstalar si es necesario
# Ver instrucciones de instalación arriba
```

## Recursos Adicionales

### Documentación Oficial
- [pytest-bdd Documentation](https://pytest-bdd.readthedocs.io/)
- [Allure Framework](https://docs.qameta.io/allure/)
- [Gherkin Syntax](https://cucumber.io/docs/gherkin/)
- [SerenityBDD (Java)](https://serenity-bdd.github.io/)

### Tutoriales
- [BDD con Python](https://automationpanda.com/bdd/)
- [Page Object Model](https://selenium-python.readthedocs.io/page-objects.html)
- [Allure Report Examples](https://demo.qameta.io/allure/)

### Comunidad
- [pytest-bdd GitHub](https://github.com/pytest-dev/pytest-bdd)
- [Allure GitHub](https://github.com/allure-framework)

## Próximos Pasos

1. **Explorar los Ejemplos**: Revisar los archivos .feature y step_defs de ejemplo
2. **Ejecutar las Pruebas**: Correr `pytest` y generar reportes Allure
3. **Crear Nuevos Escenarios**: Agregar tus propios archivos .feature
4. **Personalizar Reportes**: Configurar categorías y decoradores de Allure
5. **Integrar con CI/CD**: Configurar pipeline para ejecución automática

## Contribuir

Al agregar nuevas pruebas:

1. Escribe el escenario en Gherkin (archivo .feature)
2. Implementa las definiciones de pasos
3. Usa Page Objects para interacciones con UI
4. Agrega anotaciones Allure apropiadas
5. Documenta pasos complejos
6. Asegura que las pruebas sean independientes

---

**¡Feliz Testing con SerenityBDD! 🎉**
