# Screenplay Pattern Implementation

## Overview

The **Screenplay pattern** is a user-centered approach to writing automated acceptance tests. It focuses on **what** actors (users) do to accomplish their goals, rather than **how** they interact with the system at a technical level.

### Key Benefits

- ✅ **Readable**: Tests read like scenarios describing user behavior
- ✅ **Maintainable**: Changes to UI don't require updating every test
- ✅ **Reusable**: Tasks and interactions can be reused across multiple tests
- ✅ **Scalable**: Easy to add new features without duplicating code
- ✅ **Expressive**: Uses domain language, not technical implementation details

## Pattern Components

### 1. Actors 👤

Actors represent users or personas who interact with the system.

```python
from test.screenplay.actors import AdminUser, AssistantUser

# Create actors
admin = AdminUser()
assistant = AssistantUser()
```

**Built-in Actors:**
- `AdminUser` - Administrator with full access
- `AssistantUser` - Assistant with limited access

### 2. Abilities 💪

Abilities define what actors CAN DO. They are the foundational capabilities.

```python
from test.screenplay.abilities import BrowseTheWeb, MakeAPIRequests, UseFlaskTestClient

# Grant abilities to an actor
admin.who_can(BrowseTheWeb())
admin.who_can(MakeAPIRequests())
```

**Available Abilities:**
- `BrowseTheWeb` - Web browser automation via Selenium
- `MakeAPIRequests` - HTTP API calls via requests
- `UseFlaskTestClient` - Flask test client for integration tests

### 3. Tasks 📋

Tasks represent high-level business goals that actors want to achieve.

```python
from test.screenplay.tasks import Login, AddEmployee, CreateLiquidation

# Perform tasks
admin.attempts_to(
    Login.with_credentials("admin", "admin123"),
    AddEmployee.with_data({
        'nombre': 'Juan',
        'apellido': 'Pérez',
        'salario': '2500000'
    })
)
```

**Available Tasks:**
- `Login.with_credentials(username, password)` - Log into the system
- `AddEmployee.with_data(employee_data)` - Add a new employee
- `CreateLiquidation.for_employee(employee_id)` - Create liquidation
- `ConsultEmployee.with_id(employee_id)` - Query employee info

### 4. Interactions ⚡

Interactions are low-level actions that directly manipulate the system.

```python
from test.screenplay.interactions import Click, Fill, Open

# Low-level interactions
admin.attempts_to(
    Open.browser_on("http://127.0.0.1:8080/login"),
    Fill.field((By.NAME, "username"), "admin"),
    Click.on((By.ID, "submit-button"))
)
```

**Available Interactions:**
- `Open.browser_on(url)` - Navigate to URL
- `Click.on(locator)` - Click element
- `Fill.field(locator, value)` - Fill form field
- `SendRequest.get(endpoint)` - Send GET request
- `SendRequest.post(endpoint)` - Send POST request

### 5. Questions ❓

Questions allow actors to query the system state and verify expectations.

```python
from test.screenplay.questions import TheUrl, TheText, TheElement

# Verify expectations
admin.should_see(
    TheUrl.current().contains("/dashboard"),
    TheElement.located((By.CLASS_NAME, "success")).is_visible()
)
```

**Available Questions:**
- `TheUrl.current().contains(path)` - Verify URL contains path
- `TheText.of(locator).contains(text)` - Verify element text
- `TheElement.located(locator).is_visible()` - Verify element visibility
- `TheResponse.last().has_status(code)` - Verify HTTP status

## Complete Example

Here's a complete test using the Screenplay pattern:

```python
import unittest
from test.screenplay.actors import AdminUser
from test.screenplay.abilities import BrowseTheWeb
from test.screenplay.tasks import Login, AddEmployee
from test.screenplay.questions import TheUrl, TheElement
from selenium.webdriver.common.by import By


class TestEmployeeManagement(unittest.TestCase):
    
    def test_admin_adds_employee_successfully(self):
        """
        Scenario: Admin adds a new employee
        
        Given: An admin user with browser capabilities
        When: The admin logs in and adds an employee
        Then: The employee is created successfully
        """
        # Arrange - Create actor with abilities
        admin = AdminUser().who_can(BrowseTheWeb())
        
        employee_data = {
            'nombre': 'María',
            'apellido': 'García',
            'documento': '9876543210',
            'correo': 'maria.garcia@example.com',
            'telefono': '3009876543',
            'salario': '3000000'
        }
        
        # Act - Perform business tasks
        admin.attempts_to(
            Login.with_credentials(admin.username, admin.password),
            AddEmployee.with_data(employee_data)
        )
        
        # Assert - Verify expectations
        admin.should_see(
            TheElement.located((By.CLASS_NAME, "success-message")).is_visible()
        )
```

## Writing Your Own Components

### Creating a New Task

```python
# In test/screenplay/tasks/
class DeleteEmployee(Task):
    """Task to delete an employee."""
    
    def __init__(self, employee_id: int):
        self.employee_id = employee_id
    
    def perform_as(self, actor: Any) -> None:
        from test.screenplay.interactions import Fill, Click, Open
        
        Open.browser_on("http://127.0.0.1:8080/eliminar_usuario").perform_as(actor)
        Fill.field((By.NAME, "id_usuario"), str(self.employee_id)).perform_as(actor)
        Click.on((By.CSS_SELECTOR, "button[type='submit']")).perform_as(actor)
    
    @staticmethod
    def with_id(employee_id: int) -> 'DeleteEmployee':
        return DeleteEmployee(employee_id)
```

### Creating a New Question

```python
# In test/screenplay/questions/
class TheEmployeeCount(Question):
    """Question about the number of employees."""
    
    def answered_by(self, actor: Any) -> int:
        from test.screenplay.abilities import BrowseTheWeb
        driver = actor.using(BrowseTheWeb).get_driver()
        elements = driver.find_elements(By.CLASS_NAME, "employee-row")
        return len(elements)
    
    @staticmethod
    def displayed() -> 'TheEmployeeCount':
        return TheEmployeeCount()
```

## Running Tests

```bash
# Run all screenplay tests
python -m pytest test/screenplay/

# Run specific test file
python -m pytest test/screenplay/test_screenplay_examples.py

# Run with verbose output
python -m pytest test/screenplay/ -v
```

## Best Practices

1. **Use Domain Language**: Name tasks and questions using business terminology
2. **Single Responsibility**: Each task should have one clear purpose
3. **Composition**: Build complex scenarios by composing simple tasks
4. **Reusability**: Create reusable tasks that work in multiple contexts
5. **Readability**: Tests should read like user stories

## Resources

- **Screenplay Pattern Documentation**: https://serenity-js.org/handbook/design/screenplay-pattern.html
- **Original Paper**: http://www.janmolak.com/screenplay-pattern/
- **Example Projects**: https://github.com/serenity-js/serenity-js-examples

## Comparison with Page Object Model

| Aspect | Page Object Model | Screenplay Pattern |
|--------|------------------|-------------------|
| Focus | Pages and elements | User goals and tasks |
| Reusability | Limited to pages | High - tasks work across pages |
| Readability | Technical | Business-oriented |
| Maintenance | High - changes affect many tests | Low - changes isolated to tasks |
| Scalability | Difficult with complex flows | Excellent |

## Next Steps

1. Explore the example tests in `test_screenplay_examples.py`
2. Create custom tasks for your specific use cases
3. Build a library of reusable components
4. Write readable, maintainable tests using the pattern
