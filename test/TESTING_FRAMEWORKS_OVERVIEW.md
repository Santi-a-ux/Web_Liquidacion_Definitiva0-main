# Testing Frameworks Overview

> **Español**: Ver [GUIA_RAPIDA_ESPAÑOL.md](GUIA_RAPIDA_ESPAÑOL.md) para una guía completa en español que incluye SerenityBDD.
> 
> **Spanish**: See [GUIA_RAPIDA_ESPAÑOL.md](GUIA_RAPIDA_ESPAÑOL.md) for a complete Spanish guide including SerenityBDD.

This document provides an overview of the testing frameworks implemented in this project:
1. **Screenplay Pattern** - Behavior-driven design pattern
2. **Selenium IDE** - Browser automation and recording
3. **Cypress** - Modern E2E testing framework
4. **SerenityBDD** - BDD integration with detailed reports

---

## Quick Start

### Screenplay Pattern
```bash
# Run screenplay example tests
python -m pytest test/screenplay/test_screenplay_examples.py -v

# Documentation
See: test/screenplay/README.md
```

### Selenium IDE
```bash
# Install dependencies
pip install selenium

# Run Python tests
python -m pytest test/selenium-ide/python-tests/ -v

# Open .side files in Selenium IDE browser extension
# Documentation
See: test/selenium-ide/README.md
```

### Cypress
```bash
# Install Cypress
cd test/cypress
npm install

# Open Test Runner (GUI)
npm run cypress:open

# Run headless
npm run cypress:run

# Documentation
See: test/cypress/README.md
```

---

## Framework Comparison

| Feature | Screenplay | Selenium IDE | Cypress |
|---------|-----------|--------------|---------|
| **Type** | Design Pattern | Recording Tool | E2E Framework |
| **Language** | Python | Browser UI + Python | JavaScript |
| **Learning Curve** | Medium | Low | Medium |
| **Best For** | Maintainable tests | Quick automation | Modern E2E |
| **Browser Support** | Chrome, Firefox, etc | Chrome, Firefox | Chrome, Edge, Firefox |
| **Real Browser** | Yes (via Selenium) | Yes | Yes |
| **Speed** | Medium | Medium | Fast |
| **Debugging** | Standard | Standard | Excellent |
| **CI/CD** | Good | Good | Excellent |

---

## When to Use Each Framework

### Use Screenplay Pattern When:
- ✅ You need **highly maintainable** tests
- ✅ You want **readable** test scenarios
- ✅ You need to **reuse** test components
- ✅ You're building a **test automation framework**
- ✅ You have **complex user workflows**

**Example Use Case**: Testing complete business processes like "Employee creates liquidation and reviews report"

### Use Selenium IDE When:
- ✅ You need to **quickly record** tests
- ✅ You're **learning** test automation
- ✅ You want to **export to code** (Python, Java, C#)
- ✅ You need **simple** regression tests
- ✅ Non-developers create tests

**Example Use Case**: Recording smoke tests during manual testing sessions

### Use Cypress When:
- ✅ You need **fast, reliable** E2E tests
- ✅ You want **excellent debugging** capabilities
- ✅ You need **automatic waiting** and retries
- ✅ You want **screenshots/videos** of failures
- ✅ Your team knows **JavaScript**

**Example Use Case**: Comprehensive E2E test suite for CI/CD pipeline

---

## Test Coverage by Framework

### Screenplay Pattern
- ✅ Login flows (admin, assistant)
- ✅ Employee management
- ✅ Liquidation creation
- ✅ Employee consultation
- 📚 **Structural examples** (see README for extending)

### Selenium IDE
- ✅ Login tests (.side recordings)
- ✅ Employee management (.side recordings)
- ✅ Liquidation tests (.side recordings)
- ✅ Python converted tests (login functionality)

### Cypress
- ✅ Comprehensive login tests
- ✅ Employee CRUD operations
- ✅ Liquidation management
- ✅ Authorization checks
- ✅ Navigation tests
- ✅ Form validation

---

## Integration with Existing Tests

This project already has extensive **pytest** unit and integration tests. The new frameworks complement these:

```
test/
├── pytest Tests (existing)         ← Unit & Integration
│   ├── test_calculadora.py
│   ├── test_controlador_*.py
│   └── test_flask_*.py
│
├── screenplay/                     ← NEW: Maintainable E2E
│   ├── actors/
│   ├── tasks/
│   ├── questions/
│   └── test_screenplay_examples.py
│
├── selenium-ide/                   ← NEW: Recorded tests
│   ├── recordings/*.side
│   └── python-tests/
│
└── cypress/                        ← NEW: Modern E2E
    ├── e2e/*.cy.js
    ├── support/
    └── cypress.config.js
```

---

## Running All Tests

### Run Everything
```bash
# 1. Unit and integration tests (pytest)
python -m pytest test/ -v

# 2. Screenplay examples
python -m pytest test/screenplay/ -v

# 3. Selenium tests
python -m pytest test/selenium-ide/python-tests/ -v

# 4. Cypress tests
cd test/cypress && npm run cypress:run
```

### CI/CD Pipeline Example

```yaml
name: All Tests

on: [push]

jobs:
  pytest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run pytest
        run: python -m pytest test/ -v
  
  selenium:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install dependencies
        run: |
          pip install selenium pytest
          sudo apt-get install chromium-chromedriver
      - name: Start app
        run: python app.py &
      - name: Run Selenium tests
        run: python -m pytest test/selenium-ide/python-tests/ -v
  
  cypress:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Start app
        run: |
          pip install flask
          python app.py &
          sleep 5
      - name: Run Cypress
        uses: cypress-io/github-action@v5
        with:
          working-directory: test/cypress
```

---

## Dependencies

### Python Dependencies
```bash
# Core testing
pytest>=7.0.0
pytest-cov>=4.0.0
assertpy>=1.1

# Selenium
selenium>=4.0.0

# Screenplay pattern (uses Selenium)
selenium>=4.0.0
requests>=2.28.0
```

### JavaScript Dependencies
```bash
# Cypress
cd test/cypress
npm install cypress@^13.0.0
```

---

## Architecture Decisions

### Why Three Frameworks?

1. **Screenplay Pattern**: Provides a **design pattern** for maintainable tests
   - Not a tool, but a way of organizing test code
   - Works with any automation tool (Selenium, Playwright, etc.)

2. **Selenium IDE**: Offers **low barrier to entry**
   - Non-developers can record tests
   - Can be exported to code
   - Good for quick regression tests

3. **Cypress**: Delivers **modern E2E testing**
   - Fast, reliable, with great DX
   - Excellent for CI/CD
   - JavaScript ecosystem

### Complementary Strengths

- **Screenplay** = Test **Architecture** & **Maintainability**
- **Selenium IDE** = Quick **Recording** & **Exploration**
- **Cypress** = **Production** E2E tests in CI/CD

---

## Learning Path

### For New Team Members:

1. **Start with Selenium IDE** (1-2 hours)
   - Record some basic tests
   - Understand browser automation
   - See how tests work

2. **Move to Cypress** (1-2 days)
   - Write JavaScript E2E tests
   - Learn modern testing practices
   - Integrate with CI/CD

3. **Learn Screenplay Pattern** (3-5 days)
   - Understand the pattern philosophy
   - Write maintainable test suites
   - Build reusable components

---

## Best Practices

### General
- ✅ Write independent tests
- ✅ Use descriptive test names
- ✅ Clean up test data
- ✅ Use test fixtures/factories
- ✅ Don't test third-party code

### Framework-Specific

**Screenplay:**
- Use domain language in tasks
- Keep interactions low-level
- Make questions reusable

**Selenium IDE:**
- Add comments to recordings
- Use smart waits, not fixed waits
- Export and enhance in code

**Cypress:**
- Use custom commands
- Leverage automatic waiting
- Use fixtures for test data

---

## Troubleshooting

### Application Not Running
```bash
# Start Flask app before running tests
python app.py &
sleep 5
# Then run tests
```

### Browser Driver Issues
```bash
# Selenium
sudo apt-get install chromium-chromedriver

# Cypress (automatically manages drivers)
cd test/cypress && npm install
```

### Port Conflicts
```bash
# If port 8080 is in use, change in:
# - app.py
# - cypress.config.js (baseUrl)
# - Selenium tests (base_url)
```

---

## Resources

### Screenplay Pattern
- [Documentation](test/screenplay/README.md)
- [Serenity JS Guide](https://serenity-js.org/handbook/design/screenplay-pattern.html)

### Selenium IDE
- [Documentation](test/selenium-ide/README.md)
- [Official Docs](https://www.selenium.dev/selenium-ide/)

### Cypress
- [Documentation](test/cypress/README.md)
- [Official Docs](https://docs.cypress.io/)

---

## Contributing

When adding new tests:

1. Choose the appropriate framework
2. Follow existing patterns
3. Add documentation
4. Update this overview if needed
5. Ensure tests pass in CI/CD

---

## Future Enhancements

- [ ] Add Screenplay tests with real browser
- [ ] Integrate test reporting (Allure, etc.)
- [ ] Add visual regression testing
- [ ] Add API testing layer
- [ ] Add performance testing
- [ ] Add accessibility testing
