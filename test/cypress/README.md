# Cypress E2E Tests

> **Español**: Ver [../GUIA_RAPIDA_ESPAÑOL.md](../GUIA_RAPIDA_ESPAÑOL.md) para ejemplos y documentación en español.
> 
> **Spanish**: See [../GUIA_RAPIDA_ESPAÑOL.md](../GUIA_RAPIDA_ESPAÑOL.md) for examples and documentation in Spanish.

## Overview

This directory contains **Cypress** end-to-end tests for the Web Liquidación Definitiva application.

**Cypress** is a modern, fast, and reliable testing framework for anything that runs in a browser. It provides:
- ✅ Real-time test execution and debugging
- ✅ Automatic waiting and retry logic
- ✅ Time-travel debugging with snapshots
- ✅ Network traffic control and stubbing
- ✅ Screenshots and videos of test runs
- ✅ Cross-browser testing

## Directory Structure

```
cypress/
├── e2e/                    # E2E test specifications
│   ├── login.cy.js
│   ├── employee-management.cy.js
│   └── liquidation-management.cy.js
├── fixtures/               # Test data (JSON files)
│   ├── users.json
│   └── employees.json
├── support/                # Support files and custom commands
│   ├── commands.js        # Custom Cypress commands
│   └── e2e.js            # Support file loaded before tests
├── cypress.config.js      # Cypress configuration
├── package.json           # npm dependencies
└── README.md             # This file
```

## Installation

### 1. Install Node.js and npm

Cypress requires Node.js (version 18+ recommended):

```bash
# Check if Node.js is installed
node --version
npm --version

# If not installed, download from: https://nodejs.org/
```

### 2. Install Cypress

Navigate to the cypress directory and install dependencies:

```bash
cd test/cypress
npm install
```

This will install Cypress and all dependencies defined in `package.json`.

### 3. Verify Installation

```bash
# Open Cypress Test Runner
npm run cypress:open

# Or run tests in headless mode
npm run cypress:run
```

## Running Tests

### Interactive Mode (Cypress Test Runner)

Open the Cypress Test Runner for interactive testing:

```bash
# Open Cypress GUI
npm run cypress:open

# Alternative
npx cypress open
```

This opens a GUI where you can:
- Select tests to run
- Watch tests execute in real-time
- Use time-travel debugging
- See command logs and DOM snapshots

### Headless Mode (CI/CD)

Run tests in headless mode without GUI:

```bash
# Run all tests
npm run cypress:run

# Run specific test file
npx cypress run --spec "e2e/login.cy.js"

# Run with specific browser
npm run cypress:run:chrome
npm run cypress:run:firefox

# Run with video and keep browser open
npm run cypress:run:headed
```

## Test Suites

### 1. Login Tests (`login.cy.js`)

Tests for authentication functionality:
- ✅ Admin login success
- ✅ Assistant login success
- ✅ Invalid credentials handling
- ✅ Empty credentials validation
- ✅ Logout functionality
- ✅ Session management
- ✅ Unauthorized access prevention

### 2. Employee Management (`employee-management.cy.js`)

Tests for employee CRUD operations:
- ✅ Add new employee
- ✅ Consult employee information
- ✅ Modify employee data
- ✅ Delete employee
- ✅ List all employees
- ✅ Form validation
- ✅ Authorization checks

### 3. Liquidation Management (`liquidation-management.cy.js`)

Tests for liquidation operations:
- ✅ Create liquidation
- ✅ Consult liquidation details
- ✅ List liquidations
- ✅ Delete liquidation
- ✅ View reports
- ✅ Admin dashboard access
- ✅ Role-based permissions

## Custom Commands

Cypress custom commands are defined in `support/commands.js` to make tests more readable:

### Authentication Commands

```javascript
// Login with default admin credentials
cy.loginAsAdmin()

// Login with default assistant credentials
cy.loginAsAssistant()

// Login with custom credentials
cy.login('username', 'password')

// Logout
cy.logout()

// Clear session
cy.clearSession()
```

### Employee Commands

```javascript
// Add employee
cy.addEmployee({
  nombre: 'Juan',
  apellido: 'Pérez',
  documento: '1234567890',
  correo: 'juan@example.com',
  telefono: '3001234567',
  salario: '2500000'
})

// Consult employee
cy.consultEmployee('1234')
```

### Liquidation Commands

```javascript
// Create liquidation
cy.createLiquidation('1234')
```

### Verification Commands

```javascript
// Verify success message
cy.verifySuccess()
cy.verifySuccess('Empleado agregado exitosamente')

// Verify error message
cy.verifyError()
cy.verifyError('Usuario no encontrado')
```

## Writing Tests

### Basic Test Structure

```javascript
describe('Feature Name', () => {
  
  beforeEach(() => {
    // Setup before each test
    cy.clearSession()
    cy.loginAsAdmin()
  })
  
  it('should perform specific action', () => {
    // Arrange
    cy.visit('/page')
    
    // Act
    cy.get('input[name="field"]').type('value')
    cy.get('button[type="submit"]').click()
    
    // Assert
    cy.url().should('include', '/success')
    cy.contains('Success message').should('be.visible')
  })
  
})
```

### Using Fixtures

Load test data from fixtures:

```javascript
describe('Employee Tests', () => {
  
  it('should add employee from fixture', () => {
    // Load fixture
    cy.fixture('employees').then((employees) => {
      cy.addEmployee(employees.validEmployee)
    })
  })
  
})
```

### Asserting Elements

```javascript
// Visibility
cy.get('.element').should('be.visible')
cy.get('.element').should('not.be.visible')

// Text content
cy.contains('Text to find').should('exist')
cy.get('.element').should('have.text', 'Exact text')
cy.get('.element').should('contain', 'Partial text')

// Attributes
cy.get('input').should('have.attr', 'type', 'password')
cy.get('input').should('have.value', 'value')

// URL
cy.url().should('include', '/dashboard')
cy.url().should('eq', 'http://127.0.0.1:8080/login')

// Multiple assertions
cy.get('.element')
  .should('be.visible')
  .and('have.text', 'Expected')
  .and('have.class', 'active')
```

### Handling Forms

```javascript
// Type in input
cy.get('input[name="username"]').type('admin')

// Clear and type
cy.get('input[name="username"]').clear().type('new value')

// Select dropdown option
cy.get('select').select('Option text')

// Check checkbox
cy.get('input[type="checkbox"]').check()

// Uncheck checkbox
cy.get('input[type="checkbox"]').uncheck()

// Submit form
cy.get('form').submit()
cy.get('button[type="submit"]').click()
```

### Waiting and Timing

```javascript
// Wait for element
cy.get('.element', { timeout: 10000 }).should('exist')

// Wait for specific time (avoid if possible)
cy.wait(1000)

// Wait for request
cy.intercept('POST', '/api/employees').as('createEmployee')
cy.get('button').click()
cy.wait('@createEmployee')

// Wait for condition
cy.get('.loading').should('not.exist')
```

## Configuration

### `cypress.config.js`

Main configuration file:

```javascript
{
  baseUrl: 'http://127.0.0.1:8080',  // Application URL
  viewportWidth: 1280,                // Browser width
  viewportHeight: 720,                // Browser height
  defaultCommandTimeout: 10000,       // Command timeout
  video: true,                        // Record videos
  screenshotOnRunFailure: true,       // Screenshot on fail
  retries: { runMode: 2, openMode: 0 } // Retry failed tests
}
```

### Environment Variables

Set in `cypress.config.js` under `env`:

```javascript
env: {
  adminUsername: 'admin',
  adminPassword: 'admin123',
  assistantUsername: 'asistente',
  assistantPassword: 'asistente123'
}
```

Access in tests:

```javascript
const username = Cypress.env('adminUsername')
```

## Best Practices

### ✅ DO:

1. **Use custom commands** for repeated actions
2. **Use fixtures** for test data
3. **Use data-test attributes** for stable selectors
4. **Write independent tests** that don't depend on each other
5. **Use beforeEach** for test setup
6. **Clean up** test data after tests
7. **Use descriptive test names**
8. **Group related tests** with describe blocks
9. **Wait for elements** instead of using fixed waits

### ❌ DON'T:

1. **Don't use fixed waits** (cy.wait(5000)) - use smart waits
2. **Don't share state** between tests
3. **Don't use fragile selectors** - avoid nth-child, complex XPath
4. **Don't test external sites** - stub external APIs
5. **Don't make tests too long** - split into smaller tests
6. **Don't hardcode data** - use fixtures and variables
7. **Don't ignore flaky tests** - fix root causes

## Debugging Tests

### Time-Travel Debugging

Cypress saves snapshots at each command:
1. Click on a command in the Test Runner
2. View DOM state at that moment
3. Inspect elements and console

### Pause Execution

```javascript
cy.pause()  // Pause test execution
cy.debug()  // Debugger breakpoint
```

### Logging

```javascript
cy.log('Custom log message')
cy.get('.element').then(console.log)
```

### Screenshots

```javascript
cy.screenshot('screenshot-name')
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Cypress Tests

on: [push]

jobs:
  cypress:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Start Flask App
        run: |
          pip install -r requirements.txt
          python app.py &
          sleep 5
      
      - name: Cypress Tests
        uses: cypress-io/github-action@v5
        with:
          working-directory: test/cypress
          browser: chrome
```

## Reporting

### Built-in Reporters

```bash
# Spec reporter (default)
npx cypress run --reporter spec

# JSON reporter
npx cypress run --reporter json

# JUnit reporter
npx cypress run --reporter junit
```

### Mochawesome Reporter

Install and configure for better HTML reports:

```bash
npm install --save-dev mochawesome mochawesome-merge mochawesome-report-generator
```

## Troubleshooting

### Common Issues

**Issue**: Application not running
```bash
# Solution: Start Flask app before tests
python app.py &
sleep 5
npm run cypress:run
```

**Issue**: Timeout errors
```javascript
// Solution: Increase timeout
cy.get('.element', { timeout: 20000 })
```

**Issue**: Element not found
```javascript
// Solution: Wait for element to exist
cy.get('.element').should('exist')
```

**Issue**: Tests pass locally but fail in CI
```javascript
// Solution: Add explicit waits
cy.get('.loading').should('not.exist')
cy.get('.content').should('be.visible')
```

## Resources

### Official Documentation
- [Cypress Documentation](https://docs.cypress.io/)
- [Best Practices](https://docs.cypress.io/guides/references/best-practices)
- [API Reference](https://docs.cypress.io/api/table-of-contents)

### Tutorials
- [Cypress Real World App](https://github.com/cypress-io/cypress-realworld-app)
- [Cypress Testing Library](https://testing-library.com/docs/cypress-testing-library/intro/)

### Community
- [Cypress Discord](https://discord.gg/cypress)
- [Cypress Examples](https://example.cypress.io/)

## Next Steps

1. Install Cypress: `cd test/cypress && npm install`
2. Open Test Runner: `npm run cypress:open`
3. Run existing tests against your application
4. Write new tests for additional features
5. Integrate with CI/CD pipeline
6. Generate test reports
7. Add test coverage monitoring
