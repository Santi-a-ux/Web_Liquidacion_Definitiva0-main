"""
Interactions Module

Interactions are low-level actions that actors can perform.
They directly manipulate the system (e.g., clicking buttons, filling forms).
"""

from typing import Any
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Interaction:
    """Base class for all interactions."""
    
    def perform_as(self, actor: Any) -> None:
        """
        Perform the interaction as the given actor.
        
        Args:
            actor: The actor performing the interaction
        """
        raise NotImplementedError("Subclasses must implement perform_as")


class Click(Interaction):
    """Interaction to click on an element."""
    
    def __init__(self, locator: tuple, description: str = "element"):
        """
        Initialize a click interaction.
        
        Args:
            locator: Selenium locator tuple (By.ID, "element-id")
            description: Human-readable description of the element
        """
        self.locator = locator
        self.description = description
    
    def perform_as(self, actor: Any) -> None:
        """Click the element."""
        from screenplay.abilities import BrowseTheWeb
        driver = actor.using(BrowseTheWeb).get_driver()
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(self.locator)
        )
        element.click()
    
    @staticmethod
    def on(locator: tuple, description: str = "element") -> 'Click':
        """Factory method to create a Click interaction."""
        return Click(locator, description)


class Fill(Interaction):
    """Interaction to fill a form field."""
    
    def __init__(self, locator: tuple, value: str, description: str = "field"):
        """
        Initialize a fill interaction.
        
        Args:
            locator: Selenium locator tuple
            value: Value to enter
            description: Human-readable description of the field
        """
        self.locator = locator
        self.value = value
        self.description = description
    
    def perform_as(self, actor: Any) -> None:
        """Fill the field with the value."""
        from screenplay.abilities import BrowseTheWeb
        driver = actor.using(BrowseTheWeb).get_driver()
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(self.locator)
        )
        element.clear()
        element.send_keys(self.value)
    
    @staticmethod
    def field(locator: tuple, with_value: str, description: str = "field") -> 'Fill':
        """Factory method to create a Fill interaction."""
        return Fill(locator, with_value, description)


class Open(Interaction):
    """Interaction to open a URL."""
    
    def __init__(self, url: str):
        """
        Initialize an open interaction.
        
        Args:
            url: URL to navigate to
        """
        self.url = url
    
    def perform_as(self, actor: Any) -> None:
        """Navigate to the URL."""
        from screenplay.abilities import BrowseTheWeb
        driver = actor.using(BrowseTheWeb).get_driver()
        driver.get(self.url)
    
    @staticmethod
    def browser_on(url: str) -> 'Open':
        """Factory method to create an Open interaction."""
        return Open(url)


class SendRequest(Interaction):
    """Interaction to send an HTTP request."""
    
    def __init__(self, method: str, endpoint: str, **kwargs):
        """
        Initialize a request interaction.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            **kwargs: Additional request parameters
        """
        self.method = method.upper()
        self.endpoint = endpoint
        self.kwargs = kwargs
    
    def perform_as(self, actor: Any) -> None:
        """Send the HTTP request."""
        from screenplay.abilities import MakeAPIRequests
        api = actor.using(MakeAPIRequests)
        
        if self.method == 'GET':
            response = api.get(self.endpoint, **self.kwargs)
        elif self.method == 'POST':
            response = api.post(self.endpoint, **self.kwargs)
        else:
            raise ValueError(f"Unsupported HTTP method: {self.method}")
        
        actor.remembers('last_response', response)
    
    @staticmethod
    def get(endpoint: str, **kwargs) -> 'SendRequest':
        """Factory method for GET request."""
        return SendRequest('GET', endpoint, **kwargs)
    
    @staticmethod
    def post(endpoint: str, **kwargs) -> 'SendRequest':
        """Factory method for POST request."""
        return SendRequest('POST', endpoint, **kwargs)
