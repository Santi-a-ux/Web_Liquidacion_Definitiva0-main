# 📋 PLAN DE PRUEBAS PARA BOOKSTACK
## Basado en el Análisis de Web Liquidación Definitiva

---

## 🎯 Propósito del Documento

Este plan de pruebas está diseñado para implementar una infraestructura de testing profesional en el proyecto **BookStack** (https://github.com/BookStackApp/BookStack), basándose en las mejores prácticas y lecciones aprendidas del análisis exhaustivo del proyecto Web Liquidación Definitiva.

**Fecha de creación:** 2025-11-04  
**Proyecto destino:** BookStack  
**Tecnología base:** PHP/Laravel  
**Basado en:** Análisis de Web Liquidación Definitiva (298+ tests, 5 frameworks, >80% cobertura)

---

## 📊 RESUMEN EJECUTIVO

### Objetivos del Plan
1. Implementar una estrategia de pruebas multinivel (unitarias, integración, E2E)
2. Alcanzar >80% de cobertura de código
3. Automatizar pruebas con CI/CD
4. Implementar múltiples frameworks complementarios
5. Establecer documentación exhaustiva
6. Aplicar mejores prácticas de testing (BDD, Screenplay, AAA, FIRST)

### Métricas Objetivo
- **Cobertura de código:** >80%
- **Pruebas unitarias:** 200+ tests
- **Pruebas de integración:** 80+ tests
- **Pruebas E2E:** 50+ tests
- **Escenarios BDD:** 30+ scenarios
- **Frameworks:** 4-5 frameworks integrados
- **Tiempo de ejecución CI/CD:** <10 minutos

---

## 🔍 ANÁLISIS DEL PROYECTO BOOKSTACK

### Tecnologías Identificadas
- **Backend:** PHP 8.1+ / Laravel Framework
- **Base de datos:** MySQL/MariaDB, PostgreSQL, SQLite (soportado)
- **Frontend:** Blade templates, JavaScript, Vue.js components
- **Testing actual:** PHPUnit (framework nativo Laravel)
- **Gestión de dependencias:** Composer (PHP)

### Funcionalidades Principales a Probar
1. **Gestión de Usuarios y Autenticación**
   - Login/Logout
   - Registro de usuarios
   - Roles y permisos
   - Autenticación LDAP/SAML/OAuth

2. **Gestión de Contenido**
   - Libros (Books)
   - Capítulos (Chapters)
   - Páginas (Pages)
   - Estantes (Shelves)
   - WYSIWYG Editor

3. **Búsqueda y Navegación**
   - Búsqueda de contenido
   - Tags y categorización
   - Navegación por jerarquía

4. **Colaboración**
   - Comentarios
   - Historial de revisiones
   - Versionado de páginas
   - Actividad de usuarios

5. **Exportación e Importación**
   - PDF export
   - HTML export
   - Markdown export/import

6. **Configuración y Administración**
   - Settings del sistema
   - Gestión de roles
   - Personalización (themes, idiomas)
   - Backups y mantenimiento

---

## 🏗️ ARQUITECTURA DE PRUEBAS PROPUESTA

### Pirámide de Pruebas

```
                    /\
                   /  \
                  / E2E \           50+ tests (15%)
                 /--------\
                /          \
               / Integración \      80+ tests (25%)
              /--------------\
             /                \
            /    Unitarias     \    200+ tests (60%)
           /--------------------\
```

### Capas de Testing

| Capa | Framework Principal | Tests Estimados | Cobertura Objetivo |
|------|-------------------|-----------------|-------------------|
| **Unitaria** | PHPUnit | 200+ | >85% |
| **Integración** | PHPUnit + Laravel Testing | 80+ | >80% |
| **E2E** | Laravel Dusk / Cypress | 50+ | Flujos críticos |
| **BDD** | Behat / Codeception | 30+ scenarios | Requisitos negocio |
| **API** | PHPUnit + Pest | 40+ | >90% |

---

## 🔧 FASE 1: FRAMEWORKS Y HERRAMIENTAS

### 1.1 Framework Principal: PHPUnit (Ya existente)
**Propósito:** Pruebas unitarias y de integración  
**Estado:** Ya implementado en BookStack  
**Acción:** Expandir cobertura y mejorar organización

**Configuración recomendada en `phpunit.xml`:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="./vendor/phpunit/phpunit/phpunit.xsd"
         bootstrap="vendor/autoload.php"
         colors="true">
    <testsuites>
        <testsuite name="Unit">
            <directory suffix="Test.php">./tests/Unit</directory>
        </testsuite>
        <testsuite name="Feature">
            <directory suffix="Test.php">./tests/Feature</directory>
        </testsuite>
        <testsuite name="Api">
            <directory suffix="Test.php">./tests/Api</directory>
        </testsuite>
    </testsuites>
    <coverage processUncoveredFiles="true">
        <include>
            <directory suffix=".php">./app</directory>
        </include>
        <report>
            <clover outputFile="coverage.xml"/>
            <html outputDirectory="coverage-html"/>
            <text outputFile="php://stdout" showUncoveredFiles="true"/>
        </report>
    </coverage>
</phpunit>
```

---

### 1.2 Framework BDD: Behat o Codeception
**Propósito:** Behavior Driven Development con Gherkin  
**Lenguaje:** Gherkin (Given-When-Then)  
**Tests objetivo:** 30+ escenarios

**Instalación:**
```bash
composer require --dev behat/behat
composer require --dev friends-of-behat/mink-extension
composer require --dev friends-of-behat/mink-browserkit-driver
```

**Estructura propuesta:**
```
tests/
├── Behat/
│   ├── behat.yml                  # Configuración Behat
│   ├── features/                  # Archivos .feature
│   │   ├── authentication.feature
│   │   ├── book-management.feature
│   │   ├── page-editing.feature
│   │   └── search.feature
│   └── Context/                   # Definiciones de pasos
│       ├── AuthenticationContext.php
│       ├── BookContext.php
│       └── SearchContext.php
```

**Ejemplo de escenario Gherkin:**
```gherkin
# features/book-management.feature
Feature: Book Management
  As an authenticated user
  I want to create and manage books
  So that I can organize my documentation

  Scenario: Create a new book
    Given I am logged in as an editor
    When I navigate to the books page
    And I click on "Create New Book"
    And I fill in "Name" with "API Documentation"
    And I fill in "Description" with "Complete API reference"
    And I click "Save Book"
    Then I should see "Book created successfully"
    And I should see "API Documentation" in the books list

  Scenario: Edit an existing book
    Given I am logged in as an editor
    And a book named "User Guide" exists
    When I navigate to the "User Guide" book
    And I click on "Edit"
    And I change the name to "Complete User Guide"
    And I click "Save Book"
    Then I should see "Book updated successfully"
    And I should see "Complete User Guide"
```

---

### 1.3 Framework E2E: Laravel Dusk + Cypress
**Propósito:** Pruebas end-to-end de interfaz de usuario  
**Tests objetivo:** 50+ pruebas

#### Laravel Dusk (Nativo Laravel)
**Instalación:**
```bash
composer require --dev laravel/dusk
php artisan dusk:install
```

**Estructura:**
```
tests/
├── Browser/
│   ├── LoginTest.php
│   ├── BookCreationTest.php
│   ├── PageEditingTest.php
│   ├── SearchTest.php
│   └── ExportTest.php
```

**Ejemplo de test Dusk:**
```php
<?php

namespace Tests\Browser;

use Tests\DuskTestCase;
use Laravel\Dusk\Browser;
use App\Models\User;

class BookCreationTest extends DuskTestCase
{
    public function test_user_can_create_book()
    {
        $user = User::factory()->create();

        $this->browse(function (Browser $browser) use ($user) {
            $browser->loginAs($user)
                    ->visit('/books')
                    ->click('@create-book-button')
                    ->type('name', 'Test Book')
                    ->type('description', 'Test Description')
                    ->click('@save-button')
                    ->assertSee('Book created successfully')
                    ->assertSee('Test Book');
        });
    }
}
```

#### Cypress (Complementario)
**Instalación:**
```bash
npm install --save-dev cypress
npx cypress open
```

**Estructura:**
```
tests/
├── cypress/
│   ├── cypress.config.js
│   ├── e2e/
│   │   ├── authentication/
│   │   │   ├── login.cy.js
│   │   │   └── registration.cy.js
│   │   ├── books/
│   │   │   ├── create-book.cy.js
│   │   │   ├── edit-book.cy.js
│   │   │   └── delete-book.cy.js
│   │   ├── pages/
│   │   │   ├── create-page.cy.js
│   │   │   ├── edit-page.cy.js
│   │   │   └── wysiwyg-editor.cy.js
│   │   └── search/
│   │       └── search-functionality.cy.js
│   ├── fixtures/
│   │   ├── users.json
│   │   ├── books.json
│   │   └── pages.json
│   └── support/
│       ├── commands.js
│       └── e2e.js
```

**Ejemplo Cypress:**
```javascript
// e2e/books/create-book.cy.js
describe('Book Creation', () => {
  beforeEach(() => {
    cy.login('editor@example.com', 'password')
  })

  it('should create a new book successfully', () => {
    cy.visit('/books')
    cy.get('[data-cy="create-book"]').click()
    cy.get('[name="name"]').type('API Documentation')
    cy.get('[name="description"]').type('Complete API reference')
    cy.get('[data-cy="save-book"]').click()
    
    cy.contains('Book created successfully').should('be.visible')
    cy.contains('API Documentation').should('be.visible')
  })

  it('should validate required fields', () => {
    cy.visit('/books/create')
    cy.get('[data-cy="save-book"]').click()
    
    cy.contains('The name field is required').should('be.visible')
  })
})
```

---

### 1.4 Framework API Testing: PHPUnit + Pest
**Propósito:** Pruebas de API REST  
**Tests objetivo:** 40+ pruebas

**Instalación Pest (opcional, sintaxis moderna):**
```bash
composer require --dev pestphp/pest
composer require --dev pestphp/pest-plugin-laravel
./vendor/bin/pest --init
```

**Estructura:**
```
tests/
├── Api/
│   ├── AuthenticationApiTest.php
│   ├── BooksApiTest.php
│   ├── PagesApiTest.php
│   ├── ChaptersApiTest.php
│   ├── SearchApiTest.php
│   └── ExportApiTest.php
```

**Ejemplo con Pest:**
```php
<?php

use App\Models\User;
use App\Models\Book;

test('can retrieve list of books via API', function () {
    $user = User::factory()->create();
    Book::factory()->count(5)->create();

    $response = $this->actingAs($user, 'api')
                     ->getJson('/api/books');

    $response->assertStatus(200)
             ->assertJsonStructure([
                 'data' => [
                     '*' => ['id', 'name', 'description', 'created_at']
                 ]
             ])
             ->assertJsonCount(5, 'data');
});

test('can create book via API', function () {
    $user = User::factory()->create();

    $response = $this->actingAs($user, 'api')
                     ->postJson('/api/books', [
                         'name' => 'API Test Book',
                         'description' => 'Created via API'
                     ]);

    $response->assertStatus(201)
             ->assertJson([
                 'name' => 'API Test Book',
                 'description' => 'Created via API'
             ]);

    $this->assertDatabaseHas('books', [
        'name' => 'API Test Book'
    ]);
});
```

---

### 1.5 Patrón Screenplay (Opcional, Avanzado)
**Propósito:** Arquitectura mantenible para tests E2E  
**Implementación:** PHP + Selenium WebDriver

**Estructura propuesta:**
```
tests/
├── Screenplay/
│   ├── Actors/
│   │   ├── User.php
│   │   ├── Editor.php
│   │   └── Admin.php
│   ├── Abilities/
│   │   ├── BrowseTheWeb.php
│   │   └── CallAnApi.php
│   ├── Tasks/
│   │   ├── Login.php
│   │   ├── CreateBook.php
│   │   └── EditPage.php
│   ├── Interactions/
│   │   ├── Click.php
│   │   ├── Fill.php
│   │   └── Navigate.php
│   └── Questions/
│       ├── TheText.php
│       └── TheElement.php
```

---

## 📁 FASE 2: ESTRUCTURA DE DIRECTORIOS PROPUESTA

```
bookstack/
├── tests/
│   ├── Unit/                          # Pruebas unitarias
│   │   ├── Auth/
│   │   ├── Entities/
│   │   ├── Http/
│   │   └── Uploads/
│   │
│   ├── Feature/                       # Pruebas de integración Laravel
│   │   ├── Auth/
│   │   ├── Books/
│   │   ├── Pages/
│   │   ├── Chapters/
│   │   ├── Search/
│   │   └── Settings/
│   │
│   ├── Api/                          # Pruebas de API
│   │   ├── AuthApiTest.php
│   │   ├── BooksApiTest.php
│   │   └── PagesApiTest.php
│   │
│   ├── Browser/                      # Laravel Dusk (E2E)
│   │   ├── AuthenticationTest.php
│   │   ├── BookManagementTest.php
│   │   └── PageEditorTest.php
│   │
│   ├── Behat/                        # BDD con Gherkin
│   │   ├── behat.yml
│   │   ├── features/
│   │   └── Context/
│   │
│   ├── cypress/                      # Cypress E2E
│   │   ├── cypress.config.js
│   │   ├── e2e/
│   │   ├── fixtures/
│   │   └── support/
│   │
│   └── Screenplay/                   # Patrón Screenplay (opcional)
│       ├── Actors/
│       ├── Abilities/
│       ├── Tasks/
│       ├── Interactions/
│       └── Questions/
│
├── docs/
│   ├── testing/
│   │   ├── README.md                 # Documentación principal
│   │   ├── UNIT_TESTING.md          # Guía de pruebas unitarias
│   │   ├── INTEGRATION_TESTING.md   # Guía de integración
│   │   ├── E2E_TESTING.md           # Guía E2E
│   │   ├── BDD_TESTING.md           # Guía BDD
│   │   └── API_TESTING.md           # Guía API
│   │
│   └── validation/
│       ├── TEST_PLAN.md             # Este documento
│       ├── COVERAGE_REPORT.md       # Reporte de cobertura
│       └── VALIDATION_CRITERIA.md   # Criterios de validación
│
├── .github/
│   └── workflows/
│       ├── tests.yml                # CI/CD principal
│       ├── e2e-tests.yml            # Tests E2E separados
│       └── code-quality.yml         # Análisis de calidad
│
├── phpunit.xml                      # Configuración PHPUnit
├── behat.yml                        # Configuración Behat
├── cypress.config.js                # Configuración Cypress
└── codecov.yml                      # Configuración Codecov
```

---

## 🧪 FASE 3: CASOS DE PRUEBA DETALLADOS

### 3.1 Módulo: Autenticación y Usuarios

#### Pruebas Unitarias (PHPUnit)
```
tests/Unit/Auth/
├── LoginControllerTest.php          # Login logic
├── RegisterControllerTest.php       # Registration logic
├── PasswordResetTest.php            # Password reset
├── UserPermissionsTest.php          # Permissions logic
└── RoleTest.php                     # Role model tests
```

**Casos de prueba:**
1. Login con credenciales válidas
2. Login con credenciales inválidas
3. Login con cuenta deshabilitada
4. Registro de nuevo usuario
5. Validación de email único
6. Validación de contraseña fuerte
7. Reset de contraseña
8. Verificación de permisos por rol
9. LDAP authentication
10. OAuth authentication

#### Pruebas de Integración (Feature)
```
tests/Feature/Auth/
├── LoginTest.php
├── RegistrationTest.php
├── PasswordResetTest.php
└── SocialAuthTest.php
```

#### Pruebas E2E (Dusk/Cypress)
```
tests/Browser/Auth/
├── LoginFlowTest.php
├── RegistrationFlowTest.php
└── PasswordResetFlowTest.php
```

#### Escenarios BDD (Behat)
```gherkin
Feature: User Authentication
  Scenario: Successful login
    Given I am on the login page
    When I enter "user@example.com" in the email field
    And I enter "password123" in the password field
    And I click the "Login" button
    Then I should be redirected to the dashboard
    And I should see "Welcome back"
```

---

### 3.2 Módulo: Gestión de Libros (Books)

#### Pruebas Unitarias
```
tests/Unit/Entities/
├── BookTest.php                     # Book model
├── BookSlugTest.php                 # Slug generation
└── BookPermissionsTest.php          # Book permissions
```

**Casos de prueba:**
1. Crear libro con nombre válido
2. Validar nombre único de libro
3. Generar slug automático
4. Actualizar información de libro
5. Eliminar libro (soft delete)
6. Validar permisos de lectura
7. Validar permisos de escritura
8. Ordenar libros por nombre/fecha
9. Filtrar libros por usuario
10. Contar páginas en libro

#### Pruebas de Integración
```
tests/Feature/Books/
├── BookCreationTest.php
├── BookUpdateTest.php
├── BookDeletionTest.php
├── BookPermissionsTest.php
└── BookSearchTest.php
```

#### Pruebas API
```
tests/Api/
├── BooksApiTest.php
├── BookPagesApiTest.php
└── BookChaptersApiTest.php
```

**Endpoints a probar:**
- GET /api/books
- GET /api/books/{id}
- POST /api/books
- PUT /api/books/{id}
- DELETE /api/books/{id}
- GET /api/books/{id}/pages
- GET /api/books/{id}/chapters

#### Pruebas E2E
```
tests/Browser/Books/
├── CreateBookTest.php
├── EditBookTest.php
├── DeleteBookTest.php
├── BookNavigationTest.php
└── BookExportTest.php
```

---

### 3.3 Módulo: Gestión de Páginas (Pages)

#### Pruebas Unitarias
```
tests/Unit/Entities/
├── PageTest.php
├── PageContentTest.php
├── PageRevisionTest.php
└── PageTagTest.php
```

**Casos de prueba:**
1. Crear página con contenido Markdown
2. Crear página con contenido HTML
3. Validar título de página
4. Guardar revisión de página
5. Restaurar revisión anterior
6. Agregar tags a página
7. Buscar por tags
8. Mover página entre libros
9. Copiar página
10. Página como template

#### Pruebas de Integración
```
tests/Feature/Pages/
├── PageCreationTest.php
├── PageUpdateTest.php
├── PageRevisionTest.php
├── PageTaggingTest.php
├── PageMoveTest.php
└── PageExportTest.php
```

#### Pruebas E2E - Editor WYSIWYG
```
tests/Browser/Pages/
├── WysiwygEditorTest.php           # Editor visual
├── MarkdownEditorTest.php          # Editor Markdown
├── PageImageUploadTest.php         # Upload de imágenes
├── PageLinkingTest.php             # Enlaces internos
└── PagePreviewTest.php             # Vista previa
```

**Casos específicos del editor:**
1. Escribir texto en editor WYSIWYG
2. Aplicar formato (negrita, cursiva, subrayado)
3. Insertar lista ordenada/desordenada
4. Insertar tabla
5. Insertar imagen desde upload
6. Insertar imagen desde URL
7. Crear enlace interno
8. Crear enlace externo
9. Insertar código (code block)
10. Cambiar entre WYSIWYG y Markdown
11. Vista previa de página
12. Autosave de contenido

---

### 3.4 Módulo: Búsqueda (Search)

#### Pruebas Unitarias
```
tests/Unit/Search/
├── SearchServiceTest.php
├── SearchIndexTest.php
└── SearchQueryTest.php
```

**Casos de prueba:**
1. Búsqueda simple por texto
2. Búsqueda con operadores booleanos
3. Búsqueda por tags
4. Búsqueda por autor
5. Búsqueda por fecha
6. Búsqueda en títulos solamente
7. Búsqueda en contenido
8. Búsqueda con wildcard
9. Indexación de nuevo contenido
10. Re-indexación

#### Pruebas de Integración
```
tests/Feature/Search/
├── BasicSearchTest.php
├── AdvancedSearchTest.php
├── SearchFilterTest.php
└── SearchPermissionsTest.php
```

#### Pruebas E2E
```
tests/Browser/Search/
├── SearchBarTest.php
├── SearchResultsTest.php
└── SearchFiltersTest.php
```

---

### 3.5 Módulo: Exportación (Export)

#### Pruebas Unitarias
```
tests/Unit/Exports/
├── PdfExportTest.php
├── HtmlExportTest.php
├── MarkdownExportTest.php
└── PlainTextExportTest.php
```

**Casos de prueba:**
1. Exportar página a PDF
2. Exportar libro completo a PDF
3. Exportar a HTML
4. Exportar a Markdown
5. Exportar a texto plano
6. Validar formato de salida
7. Incluir imágenes en export
8. Mantener formato en export
9. Generar TOC en PDF
10. Custom styling en PDF

#### Pruebas de Integración
```
tests/Feature/Export/
├── PageExportTest.php
├── BookExportTest.php
└── ExportPermissionsTest.php
```

#### Pruebas E2E
```
tests/Browser/Export/
├── PdfExportTest.php
├── HtmlExportTest.php
└── BulkExportTest.php
```

---

### 3.6 Módulo: Configuración y Administración

#### Pruebas Unitarias
```
tests/Unit/Settings/
├── SettingsServiceTest.php
├── RoleManagementTest.php
├── PermissionTest.php
└── ThemeTest.php
```

#### Pruebas de Integración
```
tests/Feature/Settings/
├── GeneralSettingsTest.php
├── RoleManagementTest.php
├── MaintenanceModeTest.php
└── BackupTest.php
```

---

## 🔄 FASE 4: INTEGRACIÓN CONTINUA (CI/CD)

### 4.1 GitHub Actions - Workflow Principal

**Archivo:** `.github/workflows/tests.yml`

```yaml
name: Tests

on:
  push:
    branches: [ main, development ]
  pull_request:
    branches: [ main, development ]

jobs:
  unit-tests:
    name: Unit & Integration Tests
    runs-on: ubuntu-latest
    
    services:
      mysql:
        image: mysql:8.0
        env:
          MYSQL_ROOT_PASSWORD: password
          MYSQL_DATABASE: bookstack_test
        ports:
          - 3306:3306
        options: --health-cmd="mysqladmin ping" --health-interval=10s --health-timeout=5s --health-retries=3

    steps:
      - uses: actions/checkout@v3
      
      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: '8.2'
          extensions: mbstring, xml, ctype, iconv, intl, pdo_mysql, dom, fileinfo, libxml
          coverage: xdebug
      
      - name: Install dependencies
        run: composer install --prefer-dist --no-progress
      
      - name: Copy environment file
        run: cp .env.testing .env
      
      - name: Generate application key
        run: php artisan key:generate
      
      - name: Run migrations
        run: php artisan migrate --force
      
      - name: Run PHPUnit tests with coverage
        run: vendor/bin/phpunit --coverage-clover=coverage.xml --coverage-html=coverage-html
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
          flags: unittests
          name: codecov-umbrella
      
      - name: Upload coverage HTML
        uses: actions/upload-artifact@v3
        with:
          name: coverage-html
          path: coverage-html
          retention-days: 30

  api-tests:
    name: API Tests
    runs-on: ubuntu-latest
    needs: unit-tests
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: '8.2'
      
      - name: Install dependencies
        run: composer install
      
      - name: Run API tests
        run: vendor/bin/phpunit --testsuite=Api

  e2e-tests:
    name: End-to-End Tests
    runs-on: ubuntu-latest
    needs: unit-tests
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: '8.2'
      
      - name: Install Composer dependencies
        run: composer install
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install npm dependencies
        run: npm ci
      
      - name: Build assets
        run: npm run build
      
      - name: Install Chrome
        run: |
          sudo apt-get update
          sudo apt-get install -y google-chrome-stable
      
      - name: Start Laravel server
        run: php artisan serve &
        env:
          APP_ENV: testing
      
      - name: Run Laravel Dusk tests
        run: php artisan dusk
      
      - name: Upload Dusk screenshots
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: dusk-screenshots
          path: tests/Browser/screenshots

  cypress-tests:
    name: Cypress E2E Tests
    runs-on: ubuntu-latest
    needs: unit-tests
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: '8.2'
      
      - name: Install Composer dependencies
        run: composer install
      
      - name: Start Laravel server
        run: php artisan serve &
      
      - name: Cypress run
        uses: cypress-io/github-action@v5
        with:
          working-directory: tests/cypress
          wait-on: 'http://localhost:8000'
          wait-on-timeout: 120
      
      - name: Upload Cypress videos
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: cypress-videos
          path: tests/cypress/videos
      
      - name: Upload Cypress screenshots
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: cypress-screenshots
          path: tests/cypress/screenshots

  bdd-tests:
    name: BDD Tests (Behat)
    runs-on: ubuntu-latest
    needs: unit-tests
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: '8.2'
      
      - name: Install dependencies
        run: composer install
      
      - name: Run Behat tests
        run: vendor/bin/behat --format=progress --out=std --format=junit --out=reports/behat
      
      - name: Upload Behat reports
        uses: actions/upload-artifact@v3
        with:
          name: behat-reports
          path: reports/behat
```

---

### 4.2 Workflow de Calidad de Código

**Archivo:** `.github/workflows/code-quality.yml`

```yaml
name: Code Quality

on:
  push:
    branches: [ main, development ]
  pull_request:
    branches: [ main, development ]

jobs:
  phpstan:
    name: PHPStan Static Analysis
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: '8.2'
      
      - name: Install dependencies
        run: composer install
      
      - name: Run PHPStan
        run: vendor/bin/phpstan analyse app tests

  phpcs:
    name: PHP Code Sniffer
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: '8.2'
      
      - name: Install dependencies
        run: composer install
      
      - name: Run PHP_CodeSniffer
        run: vendor/bin/phpcs app tests --standard=PSR12

  sonarcloud:
    name: SonarCloud Analysis
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      
      - name: SonarCloud Scan
        uses: SonarSource/sonarcloud-github-action@master
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

---

## 📊 FASE 5: MÉTRICAS Y COBERTURA

### 5.1 Configuración de Codecov

**Archivo:** `codecov.yml`

```yaml
coverage:
  status:
    project:
      default:
        target: 80%
        threshold: 2%
    patch:
      default:
        target: 75%
        threshold: 5%

comment:
  layout: "reach,diff,flags,files,footer"
  behavior: default
  require_changes: false

ignore:
  - "tests/**/*"
  - "database/**/*"
  - "config/**/*"
  - "public/**/*"
```

### 5.2 Configuración de SonarQube

**Archivo:** `sonar-project.properties`

```properties
sonar.projectKey=bookstack_bookstack
sonar.organization=bookstack
sonar.projectName=BookStack
sonar.projectVersion=1.0

sonar.sources=app
sonar.tests=tests
sonar.language=php

sonar.sourceEncoding=UTF-8

sonar.php.coverage.reportPaths=coverage.xml
sonar.php.tests.reportPath=reports/phpunit.junit.xml

sonar.coverage.exclusions=**/*Test.php,**/database/**,**/config/**

sonar.cpd.php.minimumTokens=50
```

### 5.3 Objetivos de Cobertura por Módulo

| Módulo | Objetivo | Actual | Estado |
|--------|----------|--------|--------|
| Auth | >85% | - | 🔵 Por iniciar |
| Books | >85% | - | 🔵 Por iniciar |
| Chapters | >80% | - | 🔵 Por iniciar |
| Pages | >85% | - | 🔵 Por iniciar |
| Search | >80% | - | 🔵 Por iniciar |
| Uploads | >75% | - | 🔵 Por iniciar |
| Permissions | >90% | - | 🔵 Por iniciar |
| Export | >75% | - | 🔵 Por iniciar |
| Settings | >80% | - | 🔵 Por iniciar |
| **TOTAL** | **>80%** | **-** | **🔵 Por iniciar** |

---

## 📚 FASE 6: DOCUMENTACIÓN

### 6.1 Documentos a Crear

1. **docs/testing/README.md** - Guía principal de testing
2. **docs/testing/UNIT_TESTING.md** - Guía de pruebas unitarias
3. **docs/testing/INTEGRATION_TESTING.md** - Guía de integración
4. **docs/testing/E2E_TESTING.md** - Guía E2E
5. **docs/testing/BDD_TESTING.md** - Guía BDD
6. **docs/testing/API_TESTING.md** - Guía API
7. **docs/testing/BEST_PRACTICES.md** - Mejores prácticas
8. **docs/validation/TEST_PLAN.md** - Este documento
9. **docs/validation/COVERAGE_REPORT.md** - Reporte de cobertura
10. **docs/validation/VALIDATION_CRITERIA.md** - Criterios de validación

### 6.2 README Principal de Testing

**Contenido sugerido para `docs/testing/README.md`:**

```markdown
# Testing Guide - BookStack

## Quick Start

### Running All Tests
```bash
php artisan test
```

### Running Specific Test Suites
```bash
# Unit tests only
php artisan test --testsuite=Unit

# Feature tests only
php artisan test --testsuite=Feature

# API tests only
php artisan test --testsuite=Api
```

### Running with Coverage
```bash
php artisan test --coverage --min=80
```

### Running E2E Tests
```bash
# Laravel Dusk
php artisan dusk

# Cypress
cd tests/cypress
npm run cypress:run
```

### Running BDD Tests
```bash
vendor/bin/behat
```

## Test Organization

- `tests/Unit/` - Unit tests
- `tests/Feature/` - Integration tests
- `tests/Api/` - API tests
- `tests/Browser/` - E2E tests (Dusk)
- `tests/Behat/` - BDD tests (Behat)
- `tests/cypress/` - E2E tests (Cypress)

## Writing Tests

See detailed guides:
- [Unit Testing](./UNIT_TESTING.md)
- [Integration Testing](./INTEGRATION_TESTING.md)
- [E2E Testing](./E2E_TESTING.md)
- [BDD Testing](./BDD_TESTING.md)
- [API Testing](./API_TESTING.md)
- [Best Practices](./BEST_PRACTICES.md)
```

---

## 🎯 FASE 7: IMPLEMENTACIÓN - CRONOGRAMA

### Semana 1-2: Configuración Base
- ✅ Configurar PHPUnit para mejor cobertura
- ✅ Instalar y configurar Behat
- ✅ Instalar y configurar Laravel Dusk
- ✅ Instalar y configurar Cypress
- ✅ Configurar GitHub Actions workflows
- ✅ Configurar Codecov
- ✅ Configurar SonarQube/SonarCloud

### Semana 3-4: Pruebas Unitarias - Módulo Auth
- ✅ Escribir 20+ pruebas unitarias para autenticación
- ✅ Cobertura objetivo: >85%
- ✅ Documentar casos de prueba

### Semana 5-6: Pruebas Unitarias - Módulo Books
- ✅ Escribir 30+ pruebas unitarias para libros
- ✅ Cobertura objetivo: >85%
- ✅ Documentar casos de prueba

### Semana 7-8: Pruebas Unitarias - Módulo Pages
- ✅ Escribir 40+ pruebas unitarias para páginas
- ✅ Cobertura objetivo: >85%
- ✅ Documentar casos de prueba

### Semana 9-10: Pruebas de Integración
- ✅ Escribir 40+ pruebas de integración Feature
- ✅ Cubrir flujos completos
- ✅ Cobertura objetivo: >80%

### Semana 11-12: Pruebas API
- ✅ Escribir 40+ pruebas de API
- ✅ Cubrir todos los endpoints
- ✅ Cobertura objetivo: >90%

### Semana 13-14: Pruebas E2E - Dusk
- ✅ Escribir 25+ pruebas E2E con Laravel Dusk
- ✅ Cubrir flujos críticos de usuario
- ✅ Automatizar screenshots en fallos

### Semana 15-16: Pruebas E2E - Cypress
- ✅ Escribir 25+ pruebas E2E con Cypress
- ✅ Configurar grabación de videos
- ✅ Implementar comandos personalizados

### Semana 17-18: Pruebas BDD
- ✅ Escribir 30+ escenarios Gherkin
- ✅ Implementar step definitions
- ✅ Generar reportes HTML

### Semana 19-20: Optimización y Documentación
- ✅ Optimizar tiempos de ejecución
- ✅ Paralelizar pruebas
- ✅ Completar documentación
- ✅ Crear guías de mejores prácticas
- ✅ Validar cobertura >80%

---

## ✅ FASE 8: CRITERIOS DE ACEPTACIÓN

### Criterios Técnicos
- [ ] Cobertura de código >80% en total
- [ ] Cobertura de código >85% en módulos críticos (Auth, Books, Pages)
- [ ] 200+ pruebas unitarias implementadas
- [ ] 80+ pruebas de integración implementadas
- [ ] 50+ pruebas E2E implementadas
- [ ] 30+ escenarios BDD implementados
- [ ] 40+ pruebas API implementadas
- [ ] Tiempo de ejecución CI/CD <10 minutos
- [ ] 0 pruebas fallando en main branch
- [ ] Quality Gate PASSED en SonarCloud

### Criterios de Documentación
- [ ] README principal de testing completo
- [ ] 6 guías específicas por tipo de prueba
- [ ] Documentación de casos de prueba
- [ ] Matrices de trazabilidad
- [ ] Guía de mejores prácticas

### Criterios de Automatización
- [ ] GitHub Actions workflows configurados
- [ ] Tests ejecutándose en cada PR
- [ ] Reportes de cobertura automáticos
- [ ] Integración con Codecov
- [ ] Integración con SonarCloud
- [ ] Artefactos guardados (screenshots, videos, reportes)

---

## 🏆 FASE 9: MEJORES PRÁCTICAS A IMPLEMENTAR

### Principios AAA (Arrange-Act-Assert)
```php
public function test_user_can_create_book()
{
    // Arrange
    $user = User::factory()->create();
    $this->actingAs($user);
    
    // Act
    $response = $this->post('/books', [
        'name' => 'Test Book',
        'description' => 'Test Description'
    ]);
    
    // Assert
    $response->assertStatus(201);
    $this->assertDatabaseHas('books', ['name' => 'Test Book']);
}
```

### Principios FIRST
- **F**ast: Pruebas rápidas (<5 segundos)
- **I**ndependent: Independientes entre sí
- **R**epeatable: Reproducibles
- **S**elf-validating: Auto-validación
- **T**imely: Escritas a tiempo

### DRY (Don't Repeat Yourself)
- Usar factories para datos de prueba
- Crear helpers compartidos
- Implementar traits reutilizables
- Centralizar configuración

### Test Data Builders
```php
class BookBuilder
{
    private $name = 'Default Book';
    private $description = 'Default Description';
    
    public function withName(string $name): self
    {
        $this->name = $name;
        return $this;
    }
    
    public function withDescription(string $description): self
    {
        $this->description = $description;
        return $this;
    }
    
    public function build(): Book
    {
        return Book::factory()->create([
            'name' => $this->name,
            'description' => $this->description
        ]);
    }
}

// Uso
$book = (new BookBuilder())
    ->withName('API Documentation')
    ->withDescription('Complete API reference')
    ->build();
```

---

## 📊 FASE 10: REPORTES Y SEGUIMIENTO

### Dashboard de Métricas

```
╔══════════════════════════════════════════════════════════════╗
║              BOOKSTACK - TEST METRICS DASHBOARD              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Total Tests                              330+  ████████████ ║
║  ├─ Unit Tests                            200+  ████████     ║
║  ├─ Integration Tests                      80+  ████         ║
║  ├─ E2E Tests                              50+  ███          ║
║  ├─ BDD Scenarios                          30+  ██           ║
║  └─ API Tests                              40+  ███          ║
║                                                              ║
║  Code Coverage                            >80%  ████████████ ║
║  ├─ Auth Module                           >85%  ████████████ ║
║  ├─ Books Module                          >85%  ████████████ ║
║  ├─ Pages Module                          >85%  ████████████ ║
║  ├─ Search Module                         >80%  ███████████  ║
║  └─ Export Module                         >75%  ██████████   ║
║                                                              ║
║  CI/CD Status                              ✅   All Passing  ║
║  Quality Gate                              ✅   PASSED       ║
║  Test Execution Time                      <10m  ████████████ ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Reporte Semanal de Progreso

**Plantilla:** `docs/validation/WEEKLY_PROGRESS.md`

```markdown
# Weekly Progress Report - Week X

## Tests Implemented This Week
- Unit tests: X new tests
- Integration tests: X new tests
- E2E tests: X new tests
- BDD scenarios: X new scenarios

## Coverage Progress
- Overall coverage: X% (target: >80%)
- Module coverage:
  - Auth: X%
  - Books: X%
  - Pages: X%

## Issues Found
- X critical bugs found via tests
- X medium bugs found via tests
- X minor issues found via tests

## Next Week Goals
- Implement X more unit tests
- Complete Y module coverage
- Fix Z failing tests
```

---

## 🎯 CONCLUSIÓN

Este plan de pruebas proporciona una hoja de ruta completa para implementar una infraestructura de testing profesional en BookStack, basada en las mejores prácticas identificadas en el análisis del proyecto Web Liquidación Definitiva.

### Beneficios Esperados
✅ **Mayor confiabilidad** del código  
✅ **Detección temprana** de bugs  
✅ **Refactoring seguro**  
✅ **Documentación viva** del comportamiento  
✅ **Confianza en deployments**  
✅ **Mejor calidad de código**  
✅ **Reducción de deuda técnica**  

### Recursos Necesarios
- **Tiempo:** 20 semanas para implementación completa
- **Equipo:** 2-3 desarrolladores con experiencia en testing
- **Herramientas:** PHPUnit, Behat, Dusk, Cypress, GitHub Actions, Codecov, SonarCloud
- **Infraestructura:** Servidores CI/CD, bases de datos de prueba

### Siguiente Paso
Comenzar con la Fase 1: Configuración base de frameworks y herramientas.

---

**Plan creado:** 2025-11-04  
**Basado en:** Análisis de Web Liquidación Definitiva  
**Para:** BookStack Project  
**Versión:** 1.0  
**Estado:** ✅ Completo - Listo para implementación
