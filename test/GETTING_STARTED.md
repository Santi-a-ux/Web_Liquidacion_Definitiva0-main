# Getting Started with the New Testing Frameworks

This guide provides practical examples for using each of the three testing frameworks.

---

## 🎭 Screenplay Pattern

### What You'll Need
```bash
pip install selenium requests pytest
```

### Example 1: Basic Login Test

```python
from screenplay.actors import AdminUser
from screenplay.abilities import BrowseTheWeb
from screenplay.tasks import Login
from screenplay.questions import TheUrl

# Create an actor
admin = AdminUser()

# Give the actor abilities
admin.who_can(BrowseTheWeb())

# Perform tasks
admin.attempts_to(
    Login.with_credentials("admin", "admin123")
)

# Verify outcomes
admin.should_see(
    TheUrl.current().contains("/dashboard")
)
```

### Example 2: Complete Workflow

```python
from screenplay.actors import AdminUser
from screenplay.abilities import BrowseTheWeb
from screenplay.tasks import Login, AddEmployee, ConsultEmployee
from screenplay.questions import TheElement
from selenium.webdriver.common.by import By

# Setup
admin = AdminUser().who_can(BrowseTheWeb())

# Execute workflow
employee_data = {
    'nombre': 'Juan',
    'apellido': 'Pérez',
    'documento': '1234567890',
    'salario': '2500000'
}

admin.attempts_to(
    Login.with_credentials(admin.username, admin.password),
    AddEmployee.with_data(employee_data)
).should_see(
    TheElement.located((By.CLASS_NAME, "success-message")).is_visible()
)
```

### Running Screenplay Tests

```bash
# Run all screenplay tests
python -m pytest test/screenplay/ -v

# Run specific test
python -m pytest test/screenplay/test_screenplay_examples.py::ScreenplayLoginTests -v
```

---

## 🎥 Selenium IDE

### What You'll Need

1. **Browser Extension** (Chrome or Firefox)
   - Chrome: [Selenium IDE Extension](https://chrome.google.com/webstore/detail/selenium-ide/mooikfkahbdckldjjndioackbalphokd)
   - Firefox: [Selenium IDE Add-on](https://addons.mozilla.org/en-US/firefox/addon/selenium-ide/)

2. **Python Driver** (for Python tests)
```bash
pip install selenium pytest
```

### Example 1: Using Recorded Tests

1. **Open Selenium IDE**
   - Click the Selenium IDE extension icon
   - Choose "Open an existing project"
   - Select `test/selenium-ide/recordings/login-tests.side`

2. **Run Tests**
   - Ensure your Flask app is running: `python app.py`
   - Click "Run all tests" in Selenium IDE
   - Watch tests execute in real-time

### Example 2: Recording Your Own Test

1. **Start Recording**
   - Click "Create a new test in a new project"
   - Enter base URL: `http://127.0.0.1:8080`
   - Click "Start Recording"

2. **Perform Actions**
   - Navigate to login page
   - Enter credentials
   - Click login button
   - IDE records all actions automatically

3. **Add Assertions**
   - Right-click elements
   - Select "Assert" > "text" or "element present"
   - Stop recording

4. **Save**
   - Save your test
   - Export to Python if needed

### Example 3: Running Python Tests

```bash
# Make sure app is running
python app.py &

# Run Selenium Python tests
python -m pytest test/selenium-ide/python-tests/test_selenium_login.py -v
```

---

## 🌲 Cypress

### What You'll Need
```bash
cd test/cypress
npm install
```

### Example 1: Running Existing Tests

```bash
# Option 1: Interactive GUI (Recommended for Development)
npm run cypress:open

# Then:
# 1. Click "E2E Testing"
# 2. Choose a browser
# 3. Click a test file to run it
# 4. Watch it execute with time-travel debugging

# Option 2: Headless (CI/CD)
npm run cypress:run

# Run specific test file
npx cypress run --spec "e2e/login.cy.js"
```

### Example 2: Writing a New Test

Create `test/cypress/e2e/my-test.cy.js`:

```javascript
describe('My Feature Tests', () => {
  
  beforeEach(() => {
    // Clear session before each test
    cy.clearSession()
    cy.loginAsAdmin()  // Use custom command
  })
  
  it('should perform my feature', () => {
    // Navigate
    cy.visit('/my-page')
    
    // Interact
    cy.get('input[name="field"]').type('value')
    cy.get('button[type="submit"]').click()
    
    // Assert
    cy.url().should('include', '/success')
    cy.contains('Success!').should('be.visible')
  })
  
})
```

### Example 3: Using Custom Commands

```javascript
describe('Employee Management', () => {
  
  it('should add employee using custom command', () => {
    cy.loginAsAdmin()
    
    // Use custom command from support/commands.js
    cy.addEmployee({
      nombre: 'María',
      apellido: 'García',
      documento: '9876543210',
      correo: 'maria@example.com',
      telefono: '3009876543',
      salario: '3000000'
    })
    
    // Verify success
    cy.verifySuccess()
  })
  
})
```

### Example 4: Using Fixtures

```javascript
describe('Tests with Fixtures', () => {
  
  it('should use fixture data', () => {
    // Load fixture
    cy.fixture('employees').then((employees) => {
      cy.loginAsAdmin()
      cy.addEmployee(employees.validEmployee)
    })
  })
  
})
```

---

## 🚀 Practical Scenarios

### Scenario 1: Testing Login as Different Users

**Screenplay:**
```python
def test_multiple_users():
    admin = AdminUser().who_can(BrowseTheWeb())
    admin.attempts_to(Login.with_credentials("admin", "admin123"))
    admin.should_see(TheUrl.current().contains("/admin"))
    
    assistant = AssistantUser().who_can(BrowseTheWeb())
    assistant.attempts_to(Login.with_credentials("asistente", "asistente123"))
    assistant.should_see(TheUrl.current().contains("/dashboard"))
```

**Cypress:**
```javascript
it('should allow different users to login', () => {
  // Admin login
  cy.loginAsAdmin()
  cy.url().should('include', '/admin')
  cy.logout()
  
  // Assistant login
  cy.loginAsAssistant()
  cy.url().should('not.include', '/admin')
})
```

### Scenario 2: Creating and Verifying Employee

**Screenplay:**
```python
def test_create_and_verify_employee():
    admin = AdminUser().who_can(BrowseTheWeb())
    
    employee = {
        'nombre': 'Test',
        'apellido': 'User',
        'documento': '1111111111',
        'salario': '2000000'
    }
    
    admin.attempts_to(
        Login.with_credentials("admin", "admin123"),
        AddEmployee.with_data(employee),
        ConsultEmployee.with_id('1111111111')
    ).should_see(
        TheText.of((By.CLASS_NAME, "employee-info")).contains("Test User")
    )
```

**Cypress:**
```javascript
it('should create and verify employee', () => {
  const employee = {
    nombre: 'Test',
    apellido: 'User',
    documento: `${Date.now()}`,
    salario: '2000000'
  }
  
  cy.loginAsAdmin()
  cy.addEmployee(employee)
  cy.verifySuccess()
  
  cy.consultEmployee(employee.documento)
  cy.contains(`${employee.nombre} ${employee.apellido}`).should('be.visible')
})
```

### Scenario 3: Complete Business Workflow

**Cypress (Recommended for E2E workflows):**
```javascript
describe('Complete Employee Lifecycle', () => {
  
  it('should complete full employee workflow', () => {
    const employee = {
      nombre: 'Carlos',
      apellido: 'Rodríguez',
      documento: `${Date.now()}`,
      correo: `carlos.${Date.now()}@example.com`,
      telefono: '3001234567',
      salario: '2500000'
    }
    
    // Login
    cy.loginAsAdmin()
    
    // Create employee
    cy.addEmployee(employee)
    cy.verifySuccess('agregado exitosamente')
    
    // View employee list
    cy.visit('/listar_usuarios')
    cy.contains(employee.nombre).should('exist')
    
    // Create liquidation
    cy.createLiquidation(employee.documento)
    cy.verifySuccess()
    
    // View liquidation
    cy.visit('/listar_liquidaciones')
    cy.contains(employee.nombre).should('exist')
  })
  
})
```

---

## 🎯 When to Use Each Framework

### Use Screenplay When:
- ✅ Building a reusable test framework
- ✅ You need highly maintainable tests
- ✅ Tests should read like business requirements
- ✅ Multiple team members will write tests
- ✅ Complex workflows with many steps

### Use Selenium IDE When:
- ✅ Quick regression test creation
- ✅ Non-developers record tests
- ✅ Exploratory testing sessions
- ✅ Need to export to multiple languages
- ✅ Simple smoke tests

### Use Cypress When:
- ✅ Comprehensive E2E test suite
- ✅ Fast, reliable tests for CI/CD
- ✅ Need excellent debugging tools
- ✅ Team familiar with JavaScript
- ✅ Want automatic waiting and retries

---

## 🐛 Debugging Tips

### Screenplay
```python
# Add breakpoint
import pdb; pdb.set_trace()

# Check actor state
print(admin.remembered_items)

# Take screenshot (if using BrowseTheWeb)
driver = admin.using(BrowseTheWeb).get_driver()
driver.save_screenshot('debug.png')
```

### Selenium IDE
- Set breakpoints by clicking line numbers
- Step through tests command by command
- View element highlights during execution
- Check log panel for errors

### Cypress
```javascript
// Pause execution
cy.pause()

// Debug
cy.debug()

// Log to console
cy.log('Debug message')

// Take screenshot
cy.screenshot('debug-screenshot')

// Check element in DevTools
cy.get('.element').then(console.log)
```

---

## 📚 Next Steps

1. **Try the Examples**
   - Copy and run the code examples above
   - Modify them for your use cases

2. **Read the Documentation**
   - `test/screenplay/README.md`
   - `test/selenium-ide/README.md`
   - `test/cypress/README.md`

3. **Extend the Frameworks**
   - Create new Screenplay tasks
   - Record more Selenium IDE tests
   - Add Cypress test cases

4. **Integrate with CI/CD**
   - Add to GitHub Actions
   - Configure automated test runs
   - Set up test reporting

---

## 💡 Tips for Success

1. **Start Small**: Begin with one framework and one simple test
2. **Follow Patterns**: Use the examples as templates
3. **Read Documentation**: Each framework has extensive docs
4. **Ask Questions**: Use the framework communities for help
5. **Iterate**: Improve tests as you learn more

Happy Testing! 🎉
