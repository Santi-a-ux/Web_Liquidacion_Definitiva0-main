# Organización de la Suite de Pruebas

> **Nota**: Este documento está completamente en español. For English version, see the commit history or contact the maintainers.
> 
> **Spanish Quick Guide**: Ver también [GUIA_RAPIDA_ESPAÑOL.md](GUIA_RAPIDA_ESPAÑOL.md) para una guía rápida consolidada.

Este documento describe la organización y estructura de la suite de pruebas para el proyecto Web Liquidación Definitiva.

## 🆕 NUEVOS Frameworks de Pruebas Agregados

Además de la suite existente de pytest, se han implementado cuatro nuevos frameworks de pruebas:

1. **Patrón Screenplay** (`test/screenplay/`) - Patrón de diseño orientado al comportamiento para pruebas mantenibles
2. **Selenium IDE** (`test/selenium-ide/`) - Automatización de navegador con grabaciones y pruebas en Python
3. **Cypress** (`test/cypress/`) - Framework moderno de pruebas E2E con excelente experiencia de desarrollo
4. **SerenityBDD** (`test/serenity-bdd/`) - Integración BDD con reportes detallados estilo Serenity

📖 **Ver [TESTING_FRAMEWORKS_OVERVIEW.md](TESTING_FRAMEWORKS_OVERVIEW.md) para documentación completa**

## Estado de las Pruebas
✅ **Pruebas pytest aprobadas**: 208 aprobadas, 13 deseleccionadas
- Pruebas excluidas por defecto (en pytest.ini): `test_faltantes.py`, `test_basedatos.py` (requieren configuración de base de datos)
✅ **Patrón Screenplay**: Pruebas de ejemplo implementadas
✅ **Selenium IDE**: Grabaciones de pruebas de login, empleados y liquidaciones creadas
✅ **Cypress**: Suite completa de pruebas E2E implementada
✅ **SerenityBDD**: Integración con pytest-bdd y reportes Allure implementada

## Ejecutar Pruebas

### Pruebas Pytest (Unitarias e Integración)

```bash
# Ejecutar todas las pruebas pytest (usa configuración de pytest.ini)
python -m pytest

# Ejecutar pruebas con salida detallada
python -m pytest -v

# Ejecutar archivo de prueba específico
python -m pytest test/test_calculadora.py

# Ejecutar categoría de prueba específica
python -m pytest -k "test_flask"
python -m pytest -k "test_controlador"

# Incluir pruebas de base de datos (requiere configuración de PostgreSQL)
python -m pytest -k "not test_faltantes"
```

### Pruebas con Patrón Screenplay

```bash
# Ejecutar ejemplos de screenplay
python -m pytest test/screenplay/test_screenplay_examples.py -v

# Ver test/screenplay/README.md para más detalles
```

### Pruebas con Selenium IDE

```bash
# Ejecutar pruebas de Selenium convertidas a Python
python -m pytest test/selenium-ide/python-tests/ -v

# Nota: Los archivos .side pueden abrirse en la extensión de navegador Selenium IDE
# Ver test/selenium-ide/README.md para más detalles
```

### Pruebas E2E con Cypress

```bash
# Instalar dependencias (solo la primera vez)
cd test/cypress
npm install

# Abrir Cypress Test Runner (GUI)
npm run cypress:open

# Ejecutar sin interfaz gráfica (CI/CD)
npm run cypress:run

# Ver test/cypress/README.md para más detalles
```

### Pruebas SerenityBDD

```bash
# Instalar dependencias
cd test/serenity-bdd
pip install -r requirements.txt

# Ejecutar pruebas BDD con archivos .feature
pytest

# Ejecutar pruebas simples de ejemplo
pytest test_login_simple.py -v

# Generar reportes Allure
pytest --alluredir=allure-results
allure serve allure-results

# Ver test/serenity-bdd/README.md para documentación completa
```

## Organización de las Pruebas

Las pruebas están organizadas por convención de nombres siguiendo las mejores prácticas de Python:

### Pruebas Unitarias (Lógica de Negocio Pura)
- **test_calculadora.py** - Pruebas para la clase CalculadoraLiquidacion
  - Lógica de cálculo para liquidación, indemnización, vacaciones, cesantías, etc.
  - ✅ Incluye comentarios AAA (Arrange-Act-Assert)

### Pruebas de Controlador (18 archivos)
Todos los archivos con prefijo `test_controlador_*`:
- **test_controlador_unit.py** - Pruebas unitarias con mocks (FakeCursor, FakeConn)
  - ✅ Incluye comentarios AAA
- **test_controlador_auth_and_audit_success.py** - Casos de éxito de autenticación y auditoría
- **test_controlador_auth_delete.py** - Autorización para operaciones de eliminación
- **test_controlador_consultar_paths.py** - Pruebas de rutas de consulta
- **test_controlador_coverage_booster.py** - Pruebas de cobertura adicionales
- **test_controlador_db_create_and_roles.py** - Pruebas de creación de base de datos y roles
- **test_controlador_delete_and_table_errors.py** - Manejo de errores de eliminación y tablas
- **test_controlador_eliminar_rowcount_zero.py** - Pruebas de eliminación con conteo cero
- **test_controlador_es_admin_and_agregar_without_audit.py** - Verificaciones de admin y adiciones no auditadas
- **test_controlador_integrity.py** - Pruebas de integridad de datos y restricciones
- **test_controlador_more.py** - Pruebas de controlador adicionales
- **test_controlador_obtener_auditoria_with_filters.py** - Obtención de auditoría con filtros
- **test_controlador_stats_none.py** - Estadísticas con valores null/none
- **test_controlador_success_more.py** - Escenarios de éxito adicionales

### Pruebas de Aplicación Flask (12 archivos)
Todos los archivos con prefijo `test_flask_*`:
- **test_flask_app.py** - Pruebas principales de la aplicación Flask
- **test_flask_admin_exceptions.py** - Manejo de excepciones de admin
- **test_flask_admin_views.py** - Pruebas de vistas de admin
- **test_flask_coverage_booster.py** - Cobertura adicional de Flask
- **test_flask_export_simple.py** - Pruebas de funcionalidad de exportación
- **test_flask_extra.py** - Pruebas de rutas adicionales de Flask
- **test_flask_logout_no_session.py** - Pruebas de cierre de sesión sin sesión
- **test_flask_misc_routes.py** - Pruebas de rutas misceláneas
- **test_flask_more.py** - Pruebas adicionales de Flask
- **test_flask_more_undercovered_paths.py** - Pruebas de rutas con poca cobertura
- **test_flask_reports_audit.py** - Pruebas de reportes y auditoría (✅ usa assertpy)
- **test_flask_success_more.py** - Escenarios de éxito adicionales

### Pruebas de GUI/Consola
- **test_gui_coverage.py** - Pruebas de interfaz GUI (con mocks de Kivy)
- **test_consola_coverage.py** - Pruebas de interfaz de consola

### Pruebas de Integración (Operaciones de Base de Datos)
- **test_basedatos.py** - Pruebas de integración de base de datos
  - ✅ Usa assertpy para aserciones fluidas
  - ⚠️ Excluido por defecto (requiere PostgreSQL)
- **test_faltantes.py** - Pruebas para funcionalidad faltante/pendiente
  - ⚠️ Excluido por defecto (pruebas que fallan intencionalmente para TDD)

## Prácticas de Pruebas Implementadas

### 1. Aserciones Fluidas (assertpy)
El proyecto usa `assertpy` para aserciones fluidas y legibles en varios archivos de prueba:
- test_basedatos.py
- test_flask_reports_audit.py
- test_flask_misc_routes.py
- test_flask_export_simple.py

Ejemplo:
```python
from assertpy import assert_that, soft_assertions

with soft_assertions():
    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.data).contains(b'Expected Text')
```

### 2. Patrón AAA (Arrange-Act-Assert / Organizar-Actuar-Afirmar)
Los archivos de prueba clave incluyen comentarios AAA explícitos para claridad:
- **test_calculadora.py**: 5 métodos de prueba principales
- **test_controlador_unit.py**: 4 métodos de prueba

Ejemplo:
```python
def test_example(self):
    # Arrange (Organizar)
    data = prepare_test_data()
    
    # Act (Actuar)
    result = function_under_test(data)
    
    # Assert (Afirmar)
    assert result == expected_value
```

### 3. Principios FIRST
- **Fast (Rápido)**: Las pruebas unitarias usan mocks (FakeCursor, FakeConn, DummyBD)
- **Isolated (Aislado)**: Fixtures (pytest) y setUp/tearDown (unittest) aseguran aislamiento
- **Repeatable (Repetible)**: Las pruebas usan IDs aleatorios para prevenir conflictos
- **Self-Validating (Auto-validante)**: Todas las pruebas usan aserciones automatizadas
- **Timely (Oportuno)**: 32 archivos de prueba cubriendo toda la funcionalidad principal

### 4. Fixtures de Prueba
El proyecto usa:
- **pytest fixtures** para clientes de prueba de Flask
- **unittest setUp/tearDown** para inicialización de clases de prueba
- **monkeypatch** para inyección de dependencias y mocking
- **conftest.py** para configuración compartida de pruebas

## Cobertura de Pruebas por Capa

| Capa | Archivos | Pruebas | Cobertura |
|------|----------|---------|-----------|
| Modelo (Lógica de Negocio) | 1 | 20 | Pruebas unitarias |
| Controlador | 18 | ~92 | Unitarias + Integración |
| Vista (Flask) | 12 | ~74 | Pruebas de integración |
| Vista (GUI/Consola) | 2 | ~22 | Pruebas basadas en mocks |
| **Total** | **32** | **~208** | **Completo** |

## Archivos de Configuración

- **pytest.ini** - Configuración de Pytest
  - Excluye pruebas lentas de base de datos por defecto
  - Establece patrones de descubrimiento de pruebas
  - Configura modo silencioso para salida más limpia
  
- **conftest.py** - Fixtures y mocks compartidos de pruebas
  - Agrega `src/` al path de Python
  - Mockea SecretConfig para CI/CD
  - Mockea view.console.consolacontrolador

## Recomendaciones de ANALISIS_PRUEBAS.md

✅ **Completado**:
- Aserciones fluidas (assertpy) en uso en 4-5 archivos
- Patrón AAA implementado en archivos de prueba clave
- Pruebas organizadas por convención de nombres
- Todos los principios FIRST mayormente implementados
- Pruebas auto-validantes con aserciones automatizadas

🔧 **Mejoras Futuras**:
- Completar migración a assertpy en todos los archivos de prueba
- Agregar comentarios AAA a archivos de prueba restantes
- Implementar base de datos de prueba separada para pruebas de integración
- ✅ **COMPLETADO**: Pruebas E2E con Screenplay, Selenium IDE, Cypress y SerenityBDD

## Nuevos Frameworks de Pruebas

### Patrón Screenplay (`test/screenplay/`)

**Qué es**: Un patrón de diseño centrado en el usuario para escribir pruebas automatizadas mantenibles que se enfoca en qué hacen los actores, no en cómo lo hacen.

**Características Clave**:
- 👤 **Actores**: Representan usuarios (Admin, Asistente)
- 💪 **Habilidades**: Qué pueden hacer los actores (BrowseTheWeb, MakeAPIRequests)
- 📋 **Tareas**: Objetivos de alto nivel (Login, AddEmployee, CreateLiquidation)
- ⚡ **Interacciones**: Acciones de bajo nivel (Click, Fill, Open)
- ❓ **Preguntas**: Verificar estado del sistema (TheUrl, TheElement, TheText)

**Documentación**: Ver [test/screenplay/README.md](screenplay/README.md)

### Selenium IDE (`test/selenium-ide/`)

**Qué es**: Una herramienta de grabar y reproducir para automatización de navegador que crea scripts de prueba automatizados sin codificar.

**Características Clave**:
- 🎥 **Grabar** interacciones de usuario en el navegador
- 📝 **Exportar** a Python, Java, C#, y otros lenguajes
- 🔄 **Reproducir** pruebas en diferentes navegadores
- 📦 **Archivos .side**: Grabaciones de pruebas en formato JSON

**Suites de Pruebas**:
- `login-tests.side` - Pruebas de autenticación
- `employee-management.side` - Operaciones CRUD
- `liquidation-tests.side` - Flujos de liquidación
- `python-tests/` - Pruebas convertidas a Python

**Documentación**: Ver [test/selenium-ide/README.md](selenium-ide/README.md)

### Cypress (`test/cypress/`)

**Qué es**: Framework moderno de pruebas E2E con excelente experiencia de desarrollador, espera automática y depuración con viaje en el tiempo.

**Características Clave**:
- ⚡ Ejecución **rápida** con espera automática
- 🐛 **Depuración con viaje en el tiempo** con capturas
- 📸 **Capturas de pantalla** y videos en fallas
- 🔄 **Reintentos automáticos** para pruebas inestables
- 🎯 **Comandos personalizados** para acciones comunes

**Suites de Pruebas**:
- `login.cy.js` - Pruebas completas de autenticación
- `employee-management.cy.js` - CRUD de empleados con autorización
- `liquidation-management.cy.js` - Flujos de liquidación y reportes

**Documentación**: Ver [test/cypress/README.md](cypress/README.md)

### SerenityBDD (`test/serenity-bdd/`)

**Qué es**: Integración de BDD (Behavior-Driven Development) con pytest-bdd y reportes detallados tipo Serenity usando Allure.

**Características Clave**:
- 📝 **Gherkin**: Escenarios en lenguaje natural (español)
- 🎭 **Patrón Screenplay**: Tareas y actores para pruebas mantenibles
- 📊 **Reportes Allure**: Reportes HTML ricos con evidencia visual
- 🧪 **Page Objects**: Encapsulación de interacciones con páginas web

**Archivos Feature**:
- `login.feature` - Escenarios de inicio de sesión
- `empleados.feature` - Gestión de empleados
- `liquidaciones.feature` - Gestión de liquidaciones

**Documentación**: Ver [test/serenity-bdd/README.md](serenity-bdd/README.md)

### Comparación de Frameworks

| Característica | Screenplay | Selenium IDE | Cypress | SerenityBDD |
|----------------|------------|--------------|---------|-------------|
| **Propósito** | Arquitectura de pruebas | Herramienta de grabación | Framework E2E | BDD + Reportes |
| **Lenguaje** | Python | Navegador + Python | JavaScript | Python + Gherkin |
| **Mejor Para** | Mantenibilidad | Pruebas rápidas | E2E de producción | BDD y documentación |
| **Curva de Aprendizaje** | Media | Baja | Media | Media |
| **Listo para CI/CD** | ✅ | ✅ | ✅ | ✅ |

**Documentación Completa**: Ver [TESTING_FRAMEWORKS_OVERVIEW.md](TESTING_FRAMEWORKS_OVERVIEW.md)

## Contribuir

Al agregar nuevas pruebas:
1. Seguir la convención de nombres: `test_<categoría>_<descripción>.py`
2. Usar patrón AAA con comentarios explícitos para claridad
3. Preferir `assertpy` para aserciones cuando sea posible
4. Asegurar que las pruebas estén aisladas y puedan ejecutarse independientemente
5. Usar mocks/fakes para dependencias externas (base de datos, APIs)

## Recursos

- [Documentación de pytest](https://docs.pytest.org/)
- [Documentación de assertpy](https://github.com/assertpy/assertpy)
- [Principios FIRST](https://pragprog.com/magazines/2012-01/unit-tests-are-first)
- [Patrón AAA](http://wiki.c2.com/?ArrangeActAssert)
- [pytest-bdd Documentation](https://pytest-bdd.readthedocs.io/)
- [Allure Framework](https://docs.qameta.io/allure/)
