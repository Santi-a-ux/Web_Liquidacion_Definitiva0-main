"""
Selenium WebDriver Tests - Login Functionality

These tests are converted from Selenium IDE recordings and demonstrate
how to use Selenium WebDriver directly with Python for browser automation.

Tests cover:
- Admin login success
- Assistant login success
- Invalid login attempts
"""

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class SeleniumLoginTests(unittest.TestCase):
    """
    Login functionality tests using Selenium WebDriver.
    
    Note: These tests require the Flask application to be running at
    http://127.0.0.1:8080 and Chrome/Chromium to be installed.
    """
    
    @classmethod
    def setUpClass(cls):
        """Set up Selenium WebDriver for all tests."""
        options = Options()
        options.add_argument('--headless')  # Run in headless mode
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        
        try:
            cls.driver = webdriver.Chrome(options=options)
            cls.driver.implicitly_wait(10)
            cls.base_url = "http://127.0.0.1:8080"
        except Exception as e:
            raise unittest.SkipTest(f"Chrome WebDriver not available: {e}")
    
    @classmethod
    def tearDownClass(cls):
        """Close the browser after all tests."""
        if hasattr(cls, 'driver'):
            cls.driver.quit()
    
    def setUp(self):
        """Clear cookies before each test."""
        if hasattr(self, 'driver'):
            self.driver.delete_all_cookies()
    
    def test_admin_login_success(self):
        """
        Test Case: Admin Login Success
        
        Given: The login page is accessible
        When: Admin enters valid credentials
        Then: Admin is redirected to dashboard
        """
        # Arrange
        self.driver.get(f"{self.base_url}/login")
        
        # Act - Enter admin credentials
        username_field = self.driver.find_element(By.NAME, "username")
        password_field = self.driver.find_element(By.NAME, "password")
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        
        username_field.clear()
        username_field.send_keys("admin")
        
        password_field.clear()
        password_field.send_keys("admin123")
        
        submit_button.click()
        
        # Assert - Wait for redirect to dashboard
        try:
            WebDriverWait(self.driver, 10).until(
                lambda driver: "/dashboard" in driver.current_url or "/admin" in driver.current_url
            )
            # Successful login redirects away from login page
            self.assertNotIn("/login", self.driver.current_url)
        except TimeoutException:
            self.fail("Login did not redirect to dashboard")
    
    def test_assistant_login_success(self):
        """
        Test Case: Assistant Login Success
        
        Given: The login page is accessible
        When: Assistant enters valid credentials
        Then: Assistant is logged in successfully
        """
        # Arrange
        self.driver.get(f"{self.base_url}/login")
        
        # Act - Enter assistant credentials
        username_field = self.driver.find_element(By.NAME, "username")
        password_field = self.driver.find_element(By.NAME, "password")
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        
        username_field.clear()
        username_field.send_keys("asistente")
        
        password_field.clear()
        password_field.send_keys("asistente123")
        
        submit_button.click()
        
        # Assert - Successful login (redirects away from login)
        try:
            WebDriverWait(self.driver, 10).until(
                lambda driver: "/login" not in driver.current_url
            )
            # Should be redirected to some page after login
            self.assertNotEqual(f"{self.base_url}/login", self.driver.current_url)
        except TimeoutException:
            self.fail("Assistant login did not redirect")
    
    def test_invalid_login_attempt(self):
        """
        Test Case: Invalid Login Attempt
        
        Given: The login page is accessible
        When: User enters invalid credentials
        Then: User remains on login page with error message
        """
        # Arrange
        self.driver.get(f"{self.base_url}/login")
        
        # Act - Enter invalid credentials
        username_field = self.driver.find_element(By.NAME, "username")
        password_field = self.driver.find_element(By.NAME, "password")
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        
        username_field.clear()
        username_field.send_keys("invalid_user")
        
        password_field.clear()
        password_field.send_keys("wrong_password")
        
        submit_button.click()
        
        # Assert - Should stay on login page or show error
        # Wait a bit for any potential redirect
        import time
        time.sleep(2)
        
        # Either still on login page OR has error message displayed
        current_url = self.driver.current_url
        page_source = self.driver.page_source.lower()
        
        # Check for error indicators
        has_error = (
            "error" in page_source or 
            "invalid" in page_source or
            "incorrect" in page_source or
            "/login" in current_url
        )
        
        self.assertTrue(has_error, "No error indication found for invalid login")
    
    def test_empty_credentials(self):
        """
        Test Case: Empty Credentials
        
        Given: The login page is accessible
        When: User submits form with empty credentials
        Then: Form validation prevents submission or shows error
        """
        # Arrange
        self.driver.get(f"{self.base_url}/login")
        
        # Act - Try to submit without entering credentials
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Assert - Should remain on login page
        import time
        time.sleep(1)
        
        # Check we're still on login or form shows validation
        self.assertIn("/login", self.driver.current_url)


class SeleniumNavigationTests(unittest.TestCase):
    """
    Navigation tests using Selenium WebDriver.
    """
    
    @classmethod
    def setUpClass(cls):
        """Set up Selenium WebDriver."""
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        try:
            cls.driver = webdriver.Chrome(options=options)
            cls.driver.implicitly_wait(10)
            cls.base_url = "http://127.0.0.1:8080"
        except Exception as e:
            raise unittest.SkipTest(f"Chrome WebDriver not available: {e}")
    
    @classmethod
    def tearDownClass(cls):
        """Close the browser."""
        if hasattr(cls, 'driver'):
            cls.driver.quit()
    
    def test_login_page_accessible(self):
        """
        Test Case: Login Page Accessibility
        
        Given: The application is running
        When: User navigates to /login
        Then: Login page loads successfully
        """
        # Act
        self.driver.get(f"{self.base_url}/login")
        
        # Assert
        self.assertIn("/login", self.driver.current_url)
        
        # Verify login form elements exist
        try:
            self.driver.find_element(By.NAME, "username")
            self.driver.find_element(By.NAME, "password")
            self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        except NoSuchElementException as e:
            self.fail(f"Login form element not found: {e}")
    
    def test_homepage_redirects_to_login(self):
        """
        Test Case: Homepage Redirect
        
        Given: User is not logged in
        When: User accesses the homepage
        Then: User is redirected to login page
        """
        # Act
        self.driver.get(self.base_url)
        
        # Assert - Should redirect to login
        import time
        time.sleep(2)  # Give time for redirect
        
        # Should end up at login page
        self.assertIn("/login", self.driver.current_url)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
