# Resumen de Frameworks de Pruebas - Guía Rápida en Español

Este documento proporciona un resumen en español de todos los frameworks de pruebas disponibles en el proyecto.

## 📚 Documentación Completa

Para documentación detallada en inglés, consulte:
- [GETTING_STARTED.md](GETTING_STARTED.md) - Guía completa de inicio
- [TESTING_FRAMEWORKS_OVERVIEW.md](TESTING_FRAMEWORKS_OVERVIEW.md) - Resumen técnico detallado
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Resumen de implementación

## 🚀 Inicio Rápido

### 1. Patrón Screenplay

El patrón Screenplay es un enfoque centrado en el usuario para escribir pruebas automatizadas.

**Ejecutar pruebas:**
```bash
python -m pytest test/screenplay/test_screenplay_examples.py -v
```

**Ejemplo básico:**
```python
from screenplay.actors import AdminUser
from screenplay.tasks import Login

admin = AdminUser().who_can(BrowseTheWeb())
admin.attempts_to(Login.with_credentials("admin", "admin123"))
```

**Documentación**: [test/screenplay/README.md](screenplay/README.md)

### 2. Selenium IDE

Selenium IDE es una herramienta de grabar y reproducir para crear pruebas de navegador sin codificar.

**Ejecutar pruebas:**
```bash
python -m pytest test/selenium-ide/python-tests/ -v
```

**Grabar nuevas pruebas:**
1. Instalar extensión de navegador Selenium IDE
2. Abrir archivos .side en: `test/selenium-ide/recordings/`
3. Grabar nuevas interacciones
4. Exportar a Python si es necesario

**Documentación**: [test/selenium-ide/README.md](selenium-ide/README.md)

### 3. Cypress

Cypress es un framework moderno de pruebas E2E con excelente experiencia de desarrollador.

**Ejecutar pruebas:**
```bash
cd test/cypress
npm install        # Solo la primera vez
npm run cypress:open    # Modo interactivo
npm run cypress:run     # Modo headless (CI/CD)
```

**Documentación**: [test/cypress/README.md](cypress/README.md)

### 4. SerenityBDD

SerenityBDD integra BDD (Behavior-Driven Development) con reportes detallados usando Allure.

**Ejecutar pruebas:**
```bash
cd test/serenity-bdd
pip install -r requirements.txt    # Solo la primera vez

# Ejecutar pruebas BDD
pytest

# Generar reportes Allure
pytest --alluredir=allure-results
allure serve allure-results
```

**Archivos Feature (Gherkin en español):**
- `features/login.feature` - Escenarios de inicio de sesión
- `features/empleados.feature` - Gestión de empleados  
- `features/liquidaciones.feature` - Gestión de liquidaciones

**Documentación completa**: [test/serenity-bdd/README.md](serenity-bdd/README.md)

## 📊 Comparación Rápida

| Framework | Lenguaje | Propósito | Mejor Para |
|-----------|----------|-----------|------------|
| **Screenplay** | Python | Patrón de arquitectura | Pruebas mantenibles |
| **Selenium IDE** | Browser/Python | Grabar y reproducir | Pruebas rápidas |
| **Cypress** | JavaScript | Framework E2E | Pruebas de producción |
| **SerenityBDD** | Python+Gherkin | BDD + Reportes | Documentación viva |

## 🎯 ¿Cuándo Usar Cada Framework?

### Usar Screenplay cuando:
- ✅ Necesitas pruebas altamente mantenibles
- ✅ Quieres código de prueba reutilizable
- ✅ Tienes flujos de usuario complejos

### Usar Selenium IDE cuando:
- ✅ Necesitas crear pruebas rápidamente
- ✅ Personas no técnicas van a grabar pruebas
- ✅ Quieres explorar funcionalidad manualmente

### Usar Cypress cuando:
- ✅ Necesitas pruebas E2E rápidas y confiables
- ✅ Quieres excelente depuración
- ✅ Tu equipo conoce JavaScript

### Usar SerenityBDD cuando:
- ✅ Necesitas documentación ejecutable en español
- ✅ Quieres reportes detallados con evidencia visual
- ✅ Trabajas con metodología BDD
- ✅ Necesitas trazabilidad de requisitos

## 🔧 Configuración Inicial

### Requisitos Previos

**Python:**
```bash
python --version  # Debería ser 3.8 o superior
pip install pytest selenium requests
```

**Node.js (para Cypress):**
```bash
node --version  # Debería ser 14 o superior
npm --version
```

**Allure (para reportes SerenityBDD):**
```bash
# Ubuntu/Debian
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure

# macOS
brew install allure

# Windows
scoop install allure
```

## 📝 Ejemplos Prácticos

### Ejemplo 1: Prueba de Login con Screenplay

```python
from screenplay.actors import AdminUser
from screenplay.abilities import BrowseTheWeb
from screenplay.tasks import Login
from screenplay.questions import TheUrl

# Crear actor
admin = AdminUser()
admin.who_can(BrowseTheWeb())

# Ejecutar tarea
admin.attempts_to(
    Login.with_credentials("admin", "admin123")
)

# Verificar resultado
admin.should_see(
    TheUrl.current().contains("/dashboard")
)
```

### Ejemplo 2: Prueba de Login con Cypress

```javascript
describe('Pruebas de Login', () => {
  it('Login exitoso como administrador', () => {
    cy.visit('/login')
    cy.get('[name="usuario"]').type('admin')
    cy.get('[name="clave"]').type('admin123')
    cy.get('button[type="submit"]').click()
    cy.url().should('include', '/dashboard')
  })
})
```

### Ejemplo 3: Escenario BDD con SerenityBDD

```gherkin
# features/login.feature
Característica: Inicio de Sesión
  Como usuario del sistema
  Quiero poder iniciar sesión
  Para acceder a las funcionalidades

  Escenario: Login exitoso como administrador
    Dado que estoy en la página de inicio de sesión
    Cuando ingreso el usuario "admin" y la contraseña "admin123"
    Y hago clic en el botón de iniciar sesión
    Entonces debería ver el panel de administración
```

## 🐛 Depuración

### Screenplay
```python
# Agregar breakpoint
import pdb; pdb.set_trace()

# Tomar captura de pantalla
driver.save_screenshot('debug.png')
```

### Cypress
```javascript
// Pausar ejecución
cy.pause()

// Ver en consola
cy.log('Mensaje de depuración')

// Captura de pantalla
cy.screenshot('debug')
```

### SerenityBDD
Los reportes de Allure incluyen automáticamente:
- Capturas de pantalla en cada paso
- Logs detallados de ejecución
- Marcas de tiempo
- Estado de cada paso

## 📖 Recursos Adicionales

### Documentación Oficial
- **Pytest**: https://docs.pytest.org/
- **Selenium**: https://www.selenium.dev/
- **Cypress**: https://docs.cypress.io/
- **pytest-bdd**: https://pytest-bdd.readthedocs.io/
- **Allure**: https://docs.qameta.io/allure/

### Tutoriales
- **Screenplay Pattern**: https://serenity-js.org/handbook/design/screenplay-pattern.html
- **BDD con Python**: https://automationpanda.com/bdd/
- **Page Object Model**: https://selenium-python.readthedocs.io/page-objects.html

## 🤝 Contribuir

Para agregar nuevas pruebas:

1. **Elige el framework apropiado** según el tipo de prueba
2. **Sigue las convenciones de nombres** existentes
3. **Documenta tus pruebas** con comentarios claros
4. **Asegura que las pruebas sean independientes**
5. **Usa datos de prueba apropiados** (fixtures, factories)

## 💡 Consejos

1. **Empieza pequeño**: Comienza con un framework y un simple test
2. **Sigue los patrones**: Usa los ejemplos como plantillas
3. **Lee la documentación**: Cada framework tiene docs extensas
4. **Haz preguntas**: Usa las comunidades de cada framework
5. **Itera**: Mejora tus pruebas conforme aprendes

## ✅ Lista de Verificación para Nuevas Pruebas

- [ ] La prueba tiene un nombre descriptivo
- [ ] La prueba es independiente (no depende de otras)
- [ ] La prueba limpia sus datos después de ejecutarse
- [ ] La prueba usa aserciones claras
- [ ] La prueba está documentada
- [ ] La prueba pasa consistentemente
- [ ] La prueba está categorizada correctamente (marcadores/tags)

---

**¿Necesitas ayuda?** Consulta la documentación detallada de cada framework en sus respectivos directorios README.md

**¡Feliz Testing! 🎉**
