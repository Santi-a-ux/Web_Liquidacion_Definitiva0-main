# Organización de la Suite de Pruebas

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
# Run all pytest tests (uses pytest.ini configuration)
python -m pytest

# Run tests with verbose output
python -m pytest -v

# Run specific test file
python -m pytest test/test_calculadora.py

# Run specific test category
python -m pytest -k "test_flask"
python -m pytest -k "test_controlador"

# Include database tests (requires PostgreSQL setup)
python -m pytest -k "not test_faltantes"
```

### Screenplay Pattern Tests

```bash
# Run screenplay examples
python -m pytest test/screenplay/test_screenplay_examples.py -v

# See test/screenplay/README.md for more details
```

### Selenium IDE Tests

```bash
# Run Python-converted Selenium tests
python -m pytest test/selenium-ide/python-tests/ -v

# Note: .side files can be opened in Selenium IDE browser extension
# See test/selenium-ide/README.md for more details
```

### Cypress E2E Tests

```bash
# Install dependencies (first time only)
cd test/cypress
npm install

# Open Cypress Test Runner (GUI)
npm run cypress:open

# Run headless (CI/CD)
npm run cypress:run

# See test/cypress/README.md for more details
```

## Test Organization

Tests are organized by naming convention following Python best practices:

### Unit Tests (Pure Business Logic)
- **test_calculadora.py** - Tests for CalculadoraLiquidacion class
  - Calculation logic for liquidation, indemnification, vacations, cesantías, etc.
  - ✅ Includes AAA (Arrange-Act-Assert) comments

### Controller Tests (18 files)
All files prefixed with `test_controlador_*`:
- **test_controlador_unit.py** - Unit tests with mocks (FakeCursor, FakeConn)
  - ✅ Includes AAA comments
- **test_controlador_auth_and_audit_success.py** - Authentication and audit success cases
- **test_controlador_auth_delete.py** - Authorization for delete operations
- **test_controlador_consultar_paths.py** - Consultation path tests
- **test_controlador_coverage_booster.py** - Additional coverage tests
- **test_controlador_db_create_and_roles.py** - Database creation and role tests
- **test_controlador_delete_and_table_errors.py** - Delete and table error handling
- **test_controlador_eliminar_rowcount_zero.py** - Zero rowcount deletion tests
- **test_controlador_es_admin_and_agregar_without_audit.py** - Admin checks and non-audited additions
- **test_controlador_integrity.py** - Data integrity and constraint tests
- **test_controlador_more.py** - Additional controller tests
- **test_controlador_obtener_auditoria_with_filters.py** - Audit retrieval with filters
- **test_controlador_stats_none.py** - Statistics with null/none values
- **test_controlador_success_more.py** - Additional success scenarios

### Flask Application Tests (12 files)
All files prefixed with `test_flask_*`:
- **test_flask_app.py** - Core Flask application tests
- **test_flask_admin_exceptions.py** - Admin exception handling
- **test_flask_admin_views.py** - Admin view tests
- **test_flask_coverage_booster.py** - Additional Flask coverage
- **test_flask_export_simple.py** - Export functionality tests
- **test_flask_extra.py** - Extra Flask route tests
- **test_flask_logout_no_session.py** - Logout without session tests
- **test_flask_misc_routes.py** - Miscellaneous route tests
- **test_flask_more.py** - Additional Flask tests
- **test_flask_more_undercovered_paths.py** - Under-covered path tests
- **test_flask_reports_audit.py** - Reports and audit tests (✅ uses assertpy)
- **test_flask_success_more.py** - Additional success scenarios

### GUI/Console Tests
- **test_gui_coverage.py** - GUI interface tests (with Kivy mocks)
- **test_consola_coverage.py** - Console interface tests

### Integration Tests (Database Operations)
- **test_basedatos.py** - Database integration tests
  - ✅ Uses assertpy for fluent assertions
  - ⚠️ Excluded by default (requires PostgreSQL)
- **test_faltantes.py** - Tests for missing/pending functionality
  - ⚠️ Excluded by default (intentionally failing tests for TDD)

## Test Practices Implemented

### 1. FluentAssertions (assertpy)
The project uses `assertpy` for fluent, readable assertions in several test files:
- test_basedatos.py
- test_flask_reports_audit.py
- test_flask_misc_routes.py
- test_flask_export_simple.py

Example:
```python
from assertpy import assert_that, soft_assertions

with soft_assertions():
    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.data).contains(b'Expected Text')
```

### 2. AAA Pattern (Arrange-Act-Assert)
Key test files include explicit AAA comments for clarity:
- **test_calculadora.py**: 5 main test methods
- **test_controlador_unit.py**: 4 test methods

Example:
```python
def test_example(self):
    # Arrange
    data = prepare_test_data()
    
    # Act
    result = function_under_test(data)
    
    # Assert
    assert result == expected_value
```

### 3. FIRST Principles
- **Fast**: Unit tests use mocks (FakeCursor, FakeConn, DummyBD)
- **Isolated**: Fixtures (pytest) and setUp/tearDown (unittest) ensure isolation
- **Repeatable**: Tests use random IDs to prevent conflicts
- **Self-Validating**: All tests use automated assertions
- **Timely**: 32 test files covering all major functionality

### 4. Test Fixtures
The project uses:
- **pytest fixtures** for Flask test clients
- **unittest setUp/tearDown** for test class initialization
- **monkeypatch** for dependency injection and mocking
- **conftest.py** for shared test configuration

## Test Coverage by Layer

| Layer | Files | Tests | Coverage |
|-------|-------|-------|----------|
| Model (Business Logic) | 1 | 20 | Unit tests |
| Controller | 18 | ~92 | Unit + Integration |
| View (Flask) | 12 | ~74 | Integration tests |
| View (GUI/Console) | 2 | ~22 | Mock-based tests |
| **Total** | **32** | **~208** | **Comprehensive** |

## Configuration Files

- **pytest.ini** - Pytest configuration
  - Excludes slow database tests by default
  - Sets test discovery patterns
  - Configures quiet mode for cleaner output
  
- **conftest.py** - Shared test fixtures and mocks
  - Adds `src/` to Python path
  - Mocks SecretConfig for CI/CD
  - Mocks view.console.consolacontrolador

## Recommendations from ANALISIS_PRUEBAS.md

✅ **Completed**:
- FluentAssertions (assertpy) in use in 4-5 files
- AAA pattern implemented in key test files
- Tests organized by naming convention
- All FIRST principles mostly implemented
- Self-validating tests with automated assertions

🔧 **Future Improvements**:
- Complete migration to assertpy in all test files
- Add AAA comments to remaining test files
- Implement separate test database for integration tests
- ✅ **COMPLETED**: E2E tests with Screenplay, Selenium IDE, and Cypress

## New Testing Frameworks

### Screenplay Pattern (`test/screenplay/`)

**What it is**: A user-centered design pattern for writing maintainable automated tests that focuses on what actors do, not how they do it.

**Key Features**:
- 👤 **Actors**: Represent users (Admin, Assistant)
- 💪 **Abilities**: What actors can do (BrowseTheWeb, MakeAPIRequests)
- 📋 **Tasks**: High-level goals (Login, AddEmployee, CreateLiquidation)
- ⚡ **Interactions**: Low-level actions (Click, Fill, Open)
- ❓ **Questions**: Verify system state (TheUrl, TheElement, TheText)

**Documentation**: See [test/screenplay/README.md](screenplay/README.md)

### Selenium IDE (`test/selenium-ide/`)

**What it is**: A record-and-playback tool for browser automation that creates automated test scripts without coding.

**Key Features**:
- 🎥 **Record** user interactions in the browser
- 📝 **Export** to Python, Java, C#, and other languages
- 🔄 **Replay** tests across different browsers
- 📦 **.side files**: Test recordings in JSON format

**Test Suites**:
- `login-tests.side` - Authentication tests
- `employee-management.side` - CRUD operations
- `liquidation-tests.side` - Liquidation workflows
- `python-tests/` - Python-converted tests

**Documentation**: See [test/selenium-ide/README.md](selenium-ide/README.md)

### Cypress (`test/cypress/`)

**What it is**: Modern E2E testing framework with excellent developer experience, automatic waiting, and time-travel debugging.

**Key Features**:
- ⚡ **Fast** execution with automatic waiting
- 🐛 **Time-travel debugging** with snapshots
- 📸 **Screenshots** and videos on failure
- 🔄 **Automatic retries** for flaky tests
- 🎯 **Custom commands** for common actions

**Test Suites**:
- `login.cy.js` - Comprehensive authentication tests
- `employee-management.cy.js` - Employee CRUD with authorization
- `liquidation-management.cy.js` - Liquidation workflows and reports

**Documentation**: See [test/cypress/README.md](cypress/README.md)

### Framework Comparison

| Feature | Screenplay | Selenium IDE | Cypress |
|---------|-----------|--------------|---------|
| **Purpose** | Test architecture | Recording tool | E2E framework |
| **Language** | Python | Browser + Python | JavaScript |
| **Best For** | Maintainability | Quick tests | Production E2E |
| **Learning Curve** | Medium | Low | Medium |
| **CI/CD Ready** | ✅ | ✅ | ✅ |

**Complete Documentation**: See [TESTING_FRAMEWORKS_OVERVIEW.md](TESTING_FRAMEWORKS_OVERVIEW.md)

## Contributing

When adding new tests:
1. Follow the naming convention: `test_<category>_<description>.py`
2. Use AAA pattern with explicit comments for clarity
3. Prefer `assertpy` for assertions when possible
4. Ensure tests are isolated and can run independently
5. Use mocks/fakes for external dependencies (database, APIs)

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [assertpy Documentation](https://github.com/assertpy/assertpy)
- [FIRST Principles](https://pragprog.com/magazines/2012-01/unit-tests-are-first)
- [AAA Pattern](http://wiki.c2.com/?ArrangeActAssert)
