# Selenium IDE Tests

> **Español**: Ver [../GUIA_RAPIDA_ESPAÑOL.md](../GUIA_RAPIDA_ESPAÑOL.md) para ejemplos y documentación en español.
> 
> **Spanish**: See [../GUIA_RAPIDA_ESPAÑOL.md](../GUIA_RAPIDA_ESPAÑOL.md) for examples and documentation in Spanish.

## Overview

This directory contains **Selenium IDE** test recordings and Python-converted tests for the Web Liquidación Definitiva application.

**Selenium IDE** is a record-and-playback tool for browser automation that allows you to:
- Record user interactions in the browser
- Create automated test scripts without coding
- Export tests to various programming languages (Python, Java, C#, etc.)
- Run tests across different browsers

## Directory Structure

```
selenium-ide/
├── recordings/          # Selenium IDE .side files (test recordings)
│   ├── login-tests.side
│   ├── employee-management.side
│   └── liquidation-tests.side
├── python-tests/        # Python tests converted from IDE recordings
│   └── test_selenium_login.py
└── README.md           # This file
```

## Test Suites

### 1. Login Tests (`login-tests.side`)

Tests for user authentication functionality:
- ✅ Admin login with valid credentials
- ✅ Assistant login with valid credentials
- ✅ Invalid login attempt (error handling)

### 2. Employee Management (`employee-management.side`)

Tests for employee CRUD operations:
- ✅ Add new employee
- ✅ Consult employee information
- ✅ Modify employee data

### 3. Liquidation Tests (`liquidation-tests.side`)

Tests for liquidation functionality:
- ✅ Create employee liquidation
- ✅ Consult liquidation details
- ✅ List all liquidations

## Getting Started

### Installation

#### 1. Install Selenium IDE Browser Extension

**Chrome:**
1. Go to [Chrome Web Store](https://chrome.google.com/webstore/detail/selenium-ide/mooikfkahbdckldjjndioackbalphokd)
2. Click "Add to Chrome"
3. Pin the extension to your toolbar

**Firefox:**
1. Go to [Firefox Add-ons](https://addons.mozilla.org/en-US/firefox/addon/selenium-ide/)
2. Click "Add to Firefox"

#### 2. Install Python Selenium WebDriver

```bash
# Install Selenium for Python
pip install selenium

# Install ChromeDriver (for Chrome automation)
# On Ubuntu/Debian:
sudo apt-get install chromium-chromedriver

# On macOS:
brew install chromedriver

# Or download from: https://chromedriver.chromium.org/
```

### Using Selenium IDE

#### Opening a Test Suite

1. Click the Selenium IDE extension icon in your browser
2. Click "Open an existing project"
3. Select a `.side` file from `recordings/`
4. The test suite will load with all test cases

#### Running Tests in Selenium IDE

1. Open a test suite
2. Make sure your Flask application is running at `http://127.0.0.1:8080`
3. Click the "Run all tests" button (play icon)
4. Watch as tests execute in the browser
5. View results in the IDE panel

#### Recording New Tests

1. Click "Record a new test in a new project"
2. Enter the base URL: `http://127.0.0.1:8080`
3. Start interacting with the application
4. IDE will record all actions automatically
5. Click "Stop recording" when done
6. Save the test with a descriptive name

#### Editing Tests

- Click on any command to edit it
- Add assertions by right-clicking elements and selecting "Assert"
- Insert waits, breakpoints, or comments
- Reorganize commands with drag-and-drop

### Running Python Tests

The Python tests in `python-tests/` are converted from Selenium IDE recordings
and can be run with pytest or unittest:

```bash
# Run with pytest
pytest test/selenium-ide/python-tests/ -v

# Run with unittest
python -m unittest test/selenium-ide/python-tests/test_selenium_login.py

# Run specific test
python -m unittest test.selenium-ide.python-tests.test_selenium_login.SeleniumLoginTests.test_admin_login_success
```

**Requirements:**
- Flask application must be running at `http://127.0.0.1:8080`
- ChromeDriver must be installed and in PATH
- Chrome/Chromium browser must be installed

## Test Structure

### Selenium IDE Format (.side files)

`.side` files are JSON format containing:
- Test metadata (name, version, URL)
- Test commands (open, click, type, assert, etc.)
- Element locators (ID, name, CSS selectors, XPath)
- Test suites for organizing multiple tests

Example command structure:
```json
{
  "id": "1",
  "comment": "Enter username",
  "command": "type",
  "target": "name=username",
  "value": "admin"
}
```

### Python Test Structure

Python tests follow standard unittest structure:
```python
class SeleniumLoginTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize WebDriver once for all tests
        cls.driver = webdriver.Chrome(options=options)
    
    def test_admin_login_success(self):
        # Arrange - Navigate to page
        self.driver.get(f"{self.base_url}/login")
        
        # Act - Perform actions
        username_field = self.driver.find_element(By.NAME, "username")
        username_field.send_keys("admin")
        
        # Assert - Verify outcome
        self.assertIn("/dashboard", self.driver.current_url)
    
    @classmethod
    def tearDownClass(cls):
        # Clean up WebDriver
        cls.driver.quit()
```

## Common Selenium Commands

### Navigation
- `open` - Navigate to URL
- `close` - Close current window
- `selectWindow` - Switch between windows/tabs

### Interaction
- `click` - Click on element
- `type` - Enter text in field
- `select` - Select option from dropdown
- `check` / `uncheck` - Toggle checkboxes

### Assertions
- `assertText` - Verify element text
- `assertValue` - Verify input value
- `assertElementPresent` - Verify element exists
- `assertTitle` - Verify page title

### Waits
- `waitForElementPresent` - Wait for element to appear
- `waitForElementVisible` - Wait for element to be visible
- `pause` - Simple pause (milliseconds)

## Element Locators

Selenium IDE supports multiple locator strategies:

1. **ID**: `id=element-id`
2. **Name**: `name=field-name`
3. **CSS Selector**: `css=.class-name` or `css=#id-name`
4. **XPath**: `xpath=//div[@class='example']`
5. **Link Text**: `linkText=Click Here`

**Best Practices:**
- Prefer ID and name attributes (fastest, most reliable)
- Use CSS selectors for complex queries
- Avoid XPath when possible (brittle, slow)
- Use data-test attributes for test-specific locators

## Converting IDE Tests to Python

Selenium IDE can export tests to Python:

1. Open your test suite in Selenium IDE
2. Click on a test case
3. Click "Export" from the menu
4. Choose "Python pytest" or "Python unittest"
5. Save the generated file

**Note**: Exported code may need manual adjustments:
- Add proper error handling
- Implement better waits (explicit waits vs implicit)
- Add descriptive assertions
- Follow Python naming conventions

## Debugging Tests

### In Selenium IDE

1. Set breakpoints by clicking line numbers
2. Step through tests command-by-command
3. View element highlights during execution
4. Check log panel for errors

### In Python Tests

1. Add `import pdb; pdb.set_trace()` for debugging
2. Remove `--headless` option to see browser
3. Add screenshots on failure:
   ```python
   self.driver.save_screenshot('error.png')
   ```
4. Increase timeouts for slow operations

## Best Practices

### Recording Tests

✅ **DO:**
- Start with clean browser state (incognito/private mode)
- Use descriptive test names
- Add comments for complex steps
- Verify outcomes with assertions
- Keep tests focused on single functionality

❌ **DON'T:**
- Record too many actions in one test
- Depend on data from previous tests
- Use hard-coded waits (use smart waits)
- Record tests with dynamic content without verification

### Writing Python Tests

✅ **DO:**
- Use explicit waits (WebDriverWait)
- Clean up resources in tearDown
- Use descriptive variable names
- Follow AAA pattern (Arrange-Act-Assert)
- Make tests independent

❌ **DON'T:**
- Use sleep() for synchronization
- Share state between tests
- Hard-code URLs or credentials
- Ignore exceptions silently

## Continuous Integration

To run Selenium tests in CI/CD:

```yaml
# Example GitHub Actions workflow
- name: Install dependencies
  run: |
    pip install selenium pytest
    sudo apt-get install chromium-chromedriver

- name: Start Flask app
  run: python app.py &
  
- name: Wait for app
  run: sleep 5

- name: Run Selenium tests
  run: pytest test/selenium-ide/python-tests/ -v
```

## Resources

### Official Documentation
- [Selenium IDE Documentation](https://www.selenium.dev/selenium-ide/)
- [Selenium WebDriver (Python)](https://selenium-python.readthedocs.io/)
- [Selenium Commands Reference](https://www.selenium.dev/selenium-ide/docs/en/api/commands)

### Tutorials
- [Selenium IDE Getting Started](https://www.selenium.dev/selenium-ide/docs/en/introduction/getting-started)
- [Python Selenium Tutorial](https://realpython.com/modern-web-automation-with-python-and-selenium/)

### Tools
- [Selenium IDE Chrome Extension](https://chrome.google.com/webstore/detail/selenium-ide/mooikfkahbdckldjjndioackbalphokd)
- [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads)
- [Selenium Grid](https://www.selenium.dev/documentation/grid/) - For parallel test execution

## Troubleshooting

### Common Issues

**Issue**: "Chrome WebDriver not found"
```bash
# Solution: Install ChromeDriver
brew install chromedriver  # macOS
sudo apt-get install chromium-chromedriver  # Ubuntu
```

**Issue**: "Element not found"
```python
# Solution: Add explicit wait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "username"))
)
```

**Issue**: "Tests fail in headless mode"
```python
# Solution: Remove headless option for debugging
# options.add_argument('--headless')  # Comment this line
```

**Issue**: "Application not running"
```bash
# Solution: Start Flask app before tests
python app.py &
sleep 5  # Wait for app to start
pytest test/selenium-ide/python-tests/
```

## Next Steps

1. Open existing test suites in Selenium IDE
2. Run tests against your local application
3. Record new tests for uncovered functionality
4. Convert tests to Python for CI/CD integration
5. Integrate with your test automation pipeline
