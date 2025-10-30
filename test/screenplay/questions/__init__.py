"""
Questions Module

Questions allow actors to query the state of the system and verify expectations.
"""

from typing import Any
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Question:
    """Base class for all questions."""
    
    def answered_by(self, actor: Any) -> Any:
        """
        Answer the question using the actor's abilities.
        
        Args:
            actor: The actor asking the question
            
        Returns:
            The answer to the question
        """
        raise NotImplementedError("Subclasses must implement answered_by")


class TheText(Question):
    """Question about the text of an element."""
    
    def __init__(self, locator: tuple):
        """
        Initialize a text question.
        
        Args:
            locator: Selenium locator tuple
        """
        self.locator = locator
        self.expected_value = None
    
    def answered_by(self, actor: Any) -> str:
        """Get the text of the element."""
        from screenplay.abilities import BrowseTheWeb
        driver = actor.using(BrowseTheWeb).get_driver()
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(self.locator)
        )
        text = element.text
        
        # If we have an expected value, assert it
        if self.expected_value is not None:
            assert self.expected_value in text, \
                f"Expected '{self.expected_value}' to be in '{text}'"
        
        return text
    
    def contains(self, value: str) -> 'TheText':
        """Set expected value for assertion."""
        self.expected_value = value
        return self
    
    @staticmethod
    def of(locator: tuple) -> 'TheText':
        """Factory method to create a TheText question."""
        return TheText(locator)


class TheUrl(Question):
    """Question about the current URL."""
    
    def __init__(self):
        """Initialize a URL question."""
        self.expected_path = None
    
    def answered_by(self, actor: Any) -> str:
        """Get the current URL."""
        from screenplay.abilities import BrowseTheWeb
        driver = actor.using(BrowseTheWeb).get_driver()
        url = driver.current_url
        
        # If we have an expected path, assert it
        if self.expected_path is not None:
            assert self.expected_path in url, \
                f"Expected '{self.expected_path}' to be in URL '{url}'"
        
        return url
    
    def contains(self, path: str) -> 'TheUrl':
        """Set expected path for assertion."""
        self.expected_path = path
        return self
    
    @staticmethod
    def current() -> 'TheUrl':
        """Factory method to create a TheUrl question."""
        return TheUrl()


class TheElement(Question):
    """Question about element visibility."""
    
    def __init__(self, locator: tuple):
        """
        Initialize an element question.
        
        Args:
            locator: Selenium locator tuple
        """
        self.locator = locator
        self.should_be_visible = None
    
    def answered_by(self, actor: Any) -> bool:
        """Check if element is visible."""
        from screenplay.abilities import BrowseTheWeb
        driver = actor.using(BrowseTheWeb).get_driver()
        
        try:
            element = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located(self.locator)
            )
            is_visible = element.is_displayed()
        except:
            is_visible = False
        
        # If we have an expectation, assert it
        if self.should_be_visible is not None:
            if self.should_be_visible:
                assert is_visible, f"Element {self.locator} should be visible but is not"
            else:
                assert not is_visible, f"Element {self.locator} should not be visible but is"
        
        return is_visible
    
    def is_visible(self) -> 'TheElement':
        """Set expectation that element should be visible."""
        self.should_be_visible = True
        return self
    
    def is_not_visible(self) -> 'TheElement':
        """Set expectation that element should not be visible."""
        self.should_be_visible = False
        return self
    
    @staticmethod
    def located(locator: tuple) -> 'TheElement':
        """Factory method to create a TheElement question."""
        return TheElement(locator)


class TheResponse(Question):
    """Question about HTTP response."""
    
    def __init__(self):
        """Initialize a response question."""
        self.expected_status = None
    
    def answered_by(self, actor: Any) -> Any:
        """Get the last HTTP response."""
        response = actor.recalls('last_response')
        
        # If we have an expected status, assert it
        if self.expected_status is not None:
            assert response.status_code == self.expected_status, \
                f"Expected status {self.expected_status}, got {response.status_code}"
        
        return response
    
    def has_status(self, status_code: int) -> 'TheResponse':
        """Set expected status code for assertion."""
        self.expected_status = status_code
        return self
    
    @staticmethod
    def last() -> 'TheResponse':
        """Factory method to create a TheResponse question."""
        return TheResponse()
