"""
Tasks Module

Tasks represent high-level business goals that actors want to achieve.
They are composed of multiple interactions.
"""

from typing import Any
from selenium.webdriver.common.by import By


class Task:
    """Base class for all tasks."""
    
    def perform_as(self, actor: Any) -> None:
        """
        Perform the task as the given actor.
        
        Args:
            actor: The actor performing the task
        """
        raise NotImplementedError("Subclasses must implement perform_as")


class Login(Task):
    """Task to log in to the system."""
    
    def __init__(self, username: str, password: str):
        """
        Initialize a login task.
        
        Args:
            username: Username to log in with
            password: Password to log in with
        """
        self.username = username
        self.password = password
    
    def perform_as(self, actor: Any) -> None:
        """Perform the login task."""
        from test.screenplay.interactions import Fill, Click, Open
        
        # Navigate to login page
        Open.browser_on("http://127.0.0.1:8080/login").perform_as(actor)
        
        # Fill credentials
        Fill.field((By.NAME, "username"), self.username, "username field").perform_as(actor)
        Fill.field((By.NAME, "password"), self.password, "password field").perform_as(actor)
        
        # Submit
        Click.on((By.CSS_SELECTOR, "button[type='submit']"), "login button").perform_as(actor)
    
    @staticmethod
    def with_credentials(username: str, password: str) -> 'Login':
        """Factory method to create a Login task."""
        return Login(username, password)


class AddEmployee(Task):
    """Task to add a new employee."""
    
    def __init__(self, employee_data: dict):
        """
        Initialize an add employee task.
        
        Args:
            employee_data: Dictionary with employee information
        """
        self.employee_data = employee_data
    
    def perform_as(self, actor: Any) -> None:
        """Perform the add employee task."""
        from test.screenplay.interactions import Fill, Click, Open
        
        # Navigate to add employee page
        Open.browser_on("http://127.0.0.1:8080/agregar_usuario").perform_as(actor)
        
        # Fill employee form
        if 'nombre' in self.employee_data:
            Fill.field((By.NAME, "nombre"), self.employee_data['nombre']).perform_as(actor)
        if 'apellido' in self.employee_data:
            Fill.field((By.NAME, "apellido"), self.employee_data['apellido']).perform_as(actor)
        if 'documento' in self.employee_data:
            Fill.field((By.NAME, "documento"), str(self.employee_data['documento'])).perform_as(actor)
        if 'correo' in self.employee_data:
            Fill.field((By.NAME, "correo"), self.employee_data['correo']).perform_as(actor)
        if 'telefono' in self.employee_data:
            Fill.field((By.NAME, "telefono"), self.employee_data['telefono']).perform_as(actor)
        if 'salario' in self.employee_data:
            Fill.field((By.NAME, "salario"), str(self.employee_data['salario'])).perform_as(actor)
        
        # Submit form
        Click.on((By.CSS_SELECTOR, "button[type='submit']"), "submit button").perform_as(actor)
    
    @staticmethod
    def with_data(employee_data: dict) -> 'AddEmployee':
        """Factory method to create an AddEmployee task."""
        return AddEmployee(employee_data)


class CreateLiquidation(Task):
    """Task to create a liquidation for an employee."""
    
    def __init__(self, employee_id: int):
        """
        Initialize a create liquidation task.
        
        Args:
            employee_id: ID of the employee
        """
        self.employee_id = employee_id
    
    def perform_as(self, actor: Any) -> None:
        """Perform the create liquidation task."""
        from test.screenplay.interactions import Fill, Click, Open
        
        # Navigate to create liquidation page
        Open.browser_on("http://127.0.0.1:8080/agregar_liquidacion").perform_as(actor)
        
        # Fill employee ID
        Fill.field((By.NAME, "id_usuario"), str(self.employee_id)).perform_as(actor)
        
        # Submit form
        Click.on((By.CSS_SELECTOR, "button[type='submit']"), "create button").perform_as(actor)
    
    @staticmethod
    def for_employee(employee_id: int) -> 'CreateLiquidation':
        """Factory method to create a CreateLiquidation task."""
        return CreateLiquidation(employee_id)


class ConsultEmployee(Task):
    """Task to consult/query an employee."""
    
    def __init__(self, employee_id: int):
        """
        Initialize a consult employee task.
        
        Args:
            employee_id: ID of the employee to consult
        """
        self.employee_id = employee_id
    
    def perform_as(self, actor: Any) -> None:
        """Perform the consult employee task."""
        from test.screenplay.interactions import Fill, Click, Open
        
        # Navigate to consult page
        Open.browser_on("http://127.0.0.1:8080/consultar_usuario").perform_as(actor)
        
        # Fill employee ID
        Fill.field((By.NAME, "id_usuario"), str(self.employee_id)).perform_as(actor)
        
        # Submit
        Click.on((By.CSS_SELECTOR, "button[type='submit']"), "consult button").perform_as(actor)
    
    @staticmethod
    def with_id(employee_id: int) -> 'ConsultEmployee':
        """Factory method to create a ConsultEmployee task."""
        return ConsultEmployee(employee_id)
