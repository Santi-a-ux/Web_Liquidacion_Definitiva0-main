"""
Actors Module

Actors represent users or personas who interact with the system.
Each actor has abilities that allow them to perform tasks.
"""

from typing import Dict, Any, List


class Actor:
    """
    Base Actor class representing a user in the system.
    """
    
    def __init__(self, name: str):
        """
        Initialize an actor with a name and empty abilities.
        
        Args:
            name: The name of the actor (e.g., "Admin User", "Assistant")
        """
        self.name = name
        self.abilities: Dict[str, Any] = {}
        self.remembered_items: Dict[str, Any] = {}
    
    def who_can(self, ability: Any) -> 'Actor':
        """
        Grant an ability to the actor.
        
        Args:
            ability: An ability instance (e.g., BrowseTheWeb, MakeAPIRequests)
            
        Returns:
            Self for method chaining
        """
        ability_name = ability.__class__.__name__
        self.abilities[ability_name] = ability
        return self
    
    def using(self, ability_class: type) -> Any:
        """
        Retrieve an ability to use it.
        
        Args:
            ability_class: The class of the ability to retrieve
            
        Returns:
            The ability instance
            
        Raises:
            ValueError: If the actor doesn't have the requested ability
        """
        ability_name = ability_class.__name__
        if ability_name not in self.abilities:
            raise ValueError(f"{self.name} cannot use {ability_name}")
        return self.abilities[ability_name]
    
    def attempts_to(self, *tasks) -> 'Actor':
        """
        Have the actor perform one or more tasks.
        
        Args:
            *tasks: Task instances to perform
            
        Returns:
            Self for method chaining
        """
        for task in tasks:
            task.perform_as(self)
        return self
    
    def should_see(self, *questions) -> 'Actor':
        """
        Verify expectations using questions.
        
        Args:
            *questions: Question instances to evaluate
            
        Returns:
            Self for method chaining
        """
        for question in questions:
            question.answered_by(self)
        return self
    
    def remembers(self, key: str, value: Any) -> 'Actor':
        """
        Store a value for later retrieval.
        
        Args:
            key: The key to store the value under
            value: The value to remember
            
        Returns:
            Self for method chaining
        """
        self.remembered_items[key] = value
        return self
    
    def recalls(self, key: str) -> Any:
        """
        Retrieve a previously stored value.
        
        Args:
            key: The key to retrieve
            
        Returns:
            The stored value
            
        Raises:
            KeyError: If the key doesn't exist
        """
        return self.remembered_items[key]
    
    def __repr__(self) -> str:
        return f"Actor('{self.name}')"


# Pre-defined actor personas for the application
class AdminUser(Actor):
    """Administrator user with full system access."""
    
    def __init__(self):
        super().__init__("Administrator")
        # La app usa ID numérico como usuario
        self.username = "1"  # compat (Login task lo enviará a id_usuario)
        self.password = "admin123"


class AssistantUser(Actor):
    """Assistant user with limited access."""
    
    def __init__(self):
        super().__init__("Assistant")
        self.username = "2"  # compat (Login task lo enviará a id_usuario)
        self.password = "user123"
