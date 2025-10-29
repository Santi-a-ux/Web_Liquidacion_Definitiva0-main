"""
Example Screenplay Pattern Tests

This module demonstrates how to use the Screenplay pattern to write
maintainable and readable automated tests.

The Screenplay pattern focuses on:
- WHAT actors do (tasks) rather than HOW they do it (interactions)
- Separating concerns (abilities, tasks, questions)
- Reusable components
- Readable test scenarios
"""

import unittest
import sys
import os

# Add test directory to path
test_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if test_dir not in sys.path:
    sys.path.insert(0, test_dir)

from screenplay.actors import AdminUser, AssistantUser
from screenplay.abilities import UseFlaskTestClient
from screenplay.tasks import Login, AddEmployee, CreateLiquidation, ConsultEmployee
from screenplay.questions import TheUrl, TheElement
from selenium.webdriver.common.by import By


class ScreenplayLoginTests(unittest.TestCase):
    """
    Example tests for login functionality using Screenplay pattern.
    
    Note: These are example tests showing the Screenplay pattern structure.
    To run with real browser, uncomment the BrowseTheWeb ability sections.
    """
    
    def test_admin_can_login_successfully(self):
        """
        Scenario: Admin user logs in successfully
        
        Given: An admin user exists in the system
        When: The admin attempts to login with valid credentials
        Then: The admin should see the dashboard
        """
        # Arrange - Create actor with abilities
        admin = AdminUser()
        # For real browser testing:
        # admin.who_can(BrowseTheWeb())
        
        # Act - Perform the login task
        # admin.attempts_to(
        #     Login.with_credentials(admin.username, admin.password)
        # )
        
        # Assert - Verify the outcome
        # admin.should_see(
        #     TheUrl.current().contains("/dashboard")
        # )
        
        # This is a structural example
        self.assertTrue(True, "Example test - demonstrates Screenplay structure")
    
    def test_assistant_can_login_successfully(self):
        """
        Scenario: Assistant user logs in successfully
        
        Given: An assistant user exists in the system
        When: The assistant attempts to login with valid credentials
        Then: The assistant should see their dashboard
        """
        # Arrange
        assistant = AssistantUser()
        
        # Act & Assert
        # assistant.who_can(BrowseTheWeb()).attempts_to(
        #     Login.with_credentials(assistant.username, assistant.password)
        # ).should_see(
        #     TheUrl.current().contains("/dashboard")
        # )
        
        # This is a structural example
        self.assertTrue(True, "Example test - demonstrates Screenplay structure")


class ScreenplayEmployeeTests(unittest.TestCase):
    """
    Example tests for employee management using Screenplay pattern.
    """
    
    def test_admin_can_add_employee(self):
        """
        Scenario: Admin adds a new employee
        
        Given: An admin user is logged in
        When: The admin adds an employee with valid data
        Then: The employee should be created successfully
        """
        # Arrange
        admin = AdminUser()
        employee_data = {
            'nombre': 'Juan',
            'apellido': 'Pérez',
            'documento': '1234567890',
            'correo': 'juan.perez@example.com',
            'telefono': '3001234567',
            'salario': '2500000'
        }
        
        # Act & Assert
        # admin.who_can(BrowseTheWeb()).attempts_to(
        #     Login.with_credentials(admin.username, admin.password),
        #     AddEmployee.with_data(employee_data)
        # ).should_see(
        #     TheElement.located((By.CLASS_NAME, "success-message")).is_visible()
        # )
        
        # This is a structural example
        self.assertTrue(True, "Example test - demonstrates task composition")
    
    def test_admin_can_consult_employee(self):
        """
        Scenario: Admin consults employee information
        
        Given: An admin user is logged in
        And: An employee exists in the system
        When: The admin consults the employee
        Then: The employee information should be displayed
        """
        # Arrange
        admin = AdminUser()
        employee_id = 1234
        
        # Act & Assert
        # admin.who_can(BrowseTheWeb()).attempts_to(
        #     Login.with_credentials(admin.username, admin.password),
        #     ConsultEmployee.with_id(employee_id)
        # ).should_see(
        #     TheElement.located((By.CLASS_NAME, "employee-info")).is_visible()
        # )
        
        # This is a structural example
        self.assertTrue(True, "Example test - demonstrates query tasks")


class ScreenplayLiquidationTests(unittest.TestCase):
    """
    Example tests for liquidation functionality using Screenplay pattern.
    """
    
    def test_admin_can_create_liquidation(self):
        """
        Scenario: Admin creates a liquidation for an employee
        
        Given: An admin user is logged in
        And: An employee exists in the system
        When: The admin creates a liquidation for the employee
        Then: The liquidation should be created successfully
        """
        # Arrange
        admin = AdminUser()
        employee_id = 1234
        
        # Act & Assert
        # admin.who_can(BrowseTheWeb()).attempts_to(
        #     Login.with_credentials(admin.username, admin.password),
        #     CreateLiquidation.for_employee(employee_id)
        # ).should_see(
        #     TheElement.located((By.CLASS_NAME, "success-message")).is_visible()
        # )
        
        # This is a structural example
        self.assertTrue(True, "Example test - demonstrates business flow")


class ScreenplayPatternDemonstration(unittest.TestCase):
    """
    Tests demonstrating key Screenplay pattern concepts.
    """
    
    def test_actor_with_multiple_abilities(self):
        """
        Demonstrates an actor using multiple abilities.
        """
        from screenplay.abilities import BrowseTheWeb, MakeAPIRequests
        
        # An actor can have multiple abilities
        admin = AdminUser()
        # admin.who_can(BrowseTheWeb()).who_can(MakeAPIRequests())
        
        # Can use different abilities in the same test
        # admin.attempts_to(
        #     SendRequest.get("/api/employees")
        # ).should_see(
        #     TheResponse.last().has_status(200)
        # )
        
        self.assertTrue(True, "Demonstrates multiple abilities concept")
    
    def test_actor_remembering_values(self):
        """
        Demonstrates an actor remembering values between steps.
        """
        admin = AdminUser()
        
        # Actor can remember values
        admin.remembers('employee_id', 1234)
        
        # And recall them later
        employee_id = admin.recalls('employee_id')
        
        self.assertEqual(employee_id, 1234)
    
    def test_method_chaining_fluent_interface(self):
        """
        Demonstrates the fluent interface with method chaining.
        """
        admin = AdminUser()
        
        # All methods return self for chaining
        result = admin.remembers('key1', 'value1').remembers('key2', 'value2')
        
        self.assertEqual(result, admin)
        self.assertEqual(admin.recalls('key1'), 'value1')
        self.assertEqual(admin.recalls('key2'), 'value2')


if __name__ == '__main__':
    unittest.main()
