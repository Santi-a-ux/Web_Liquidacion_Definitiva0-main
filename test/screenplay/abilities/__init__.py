"""
Abilities Module

Abilities define what actors CAN DO. They are the foundational capabilities
that enable actors to interact with the system.
"""

from typing import Any, Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import requests


class Ability:
    """Base class for all abilities."""
    
    def as_(self, actor: Any) -> 'Ability':
        """
        Associate this ability with an actor.
        
        Args:
            actor: The actor to associate with
            
        Returns:
            Self for method chaining
        """
        return self


LAST_DRIVER: Optional[webdriver.Chrome] = None


def set_last_driver(driver: Optional[webdriver.Chrome]) -> None:
    global LAST_DRIVER
    LAST_DRIVER = driver


def get_last_driver() -> Optional[webdriver.Chrome]:
    return LAST_DRIVER


class BrowseTheWeb(Ability):
    """
    Ability to browse the web using Selenium WebDriver.
    """
    
    def __init__(self, driver: Optional[webdriver.Chrome] = None):
        """
        Initialize the web browsing ability.
        
        Args:
            driver: Selenium WebDriver instance. If None, creates a new one.
        """
        if driver is None:
            options = Options()
            # Headless moderno (Chrome 109+)
            options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--window-size=1280,800')

            # Intentar usar webdriver-manager si está disponible
            try:
                from webdriver_manager.chrome import ChromeDriverManager
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)
            except Exception:
                # Fallback: requiere chromedriver en PATH
                self.driver = webdriver.Chrome(options=options)
            # Registrar último driver para reportes
            set_last_driver(self.driver)
        else:
            self.driver = driver
            set_last_driver(self.driver)
    
    def get_driver(self) -> webdriver.Chrome:
        """Get the WebDriver instance."""
        return self.driver
    
    def navigate_to(self, url: str) -> None:
        """Navigate to a URL."""
        self.driver.get(url)
    
    def close(self) -> None:
        """Close the browser."""
        if self.driver:
            self.driver.quit()
            set_last_driver(None)
    
    def __del__(self):
        """Cleanup when ability is destroyed."""
        self.close()


class MakeAPIRequests(Ability):
    """
    Ability to make HTTP API requests.
    """
    
    def __init__(self, base_url: str = "http://127.0.0.1:8080"):
        """
        Initialize the API request ability.
        
        Args:
            base_url: The base URL for API requests
        """
        self.base_url = base_url
        self.session = requests.Session()
    
    def get_session(self) -> requests.Session:
        """Get the requests session."""
        return self.session
    
    def get(self, endpoint: str, **kwargs) -> requests.Response:
        """Make a GET request."""
        url = f"{self.base_url}{endpoint}"
        return self.session.get(url, **kwargs)
    
    def post(self, endpoint: str, **kwargs) -> requests.Response:
        """Make a POST request."""
        url = f"{self.base_url}{endpoint}"
        return self.session.post(url, **kwargs)
    
    def close(self) -> None:
        """Close the session."""
        self.session.close()


class UseFlaskTestClient(Ability):
    """
    Ability to use Flask test client for testing.
    """
    
    def __init__(self, app):
        """
        Initialize with a Flask application.
        
        Args:
            app: Flask application instance
        """
        self.app = app
        self.client = app.test_client()
    
    def get_client(self):
        """Get the Flask test client."""
        return self.client
