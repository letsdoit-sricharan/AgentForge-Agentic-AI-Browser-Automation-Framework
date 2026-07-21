"""
Task Base Class

Represents a single business objective in the automation system.

Responsibilities:
    - Define task interface
    - Encapsulate business intent
    - Provide task metadata
    - Validate task inputs

Does NOT:
    - Execute browser operations
    - Know about plugins
    - Know about workflows
    - Import Playwright
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import KW_ONLY, dataclass, field
from typing import Any
from uuid import uuid4


@dataclass
class Task(ABC):
    """
    Base class for all tasks.
    
    A Task represents a business objective that needs to be accomplished,
    without specifying HOW it should be done.
    
    Examples:
        - SearchMovieTask: Find a movie
        - SelectSeatsTask: Choose theater seats
        - PurchaseTicketTask: Complete payment
        - SearchProductTask: Find product on e-commerce site
        - AddToCartTask: Add item to cart

    Design note:
        All fields below the KW_ONLY sentinel are keyword-only.
        This allows concrete subclasses to define their own required
        positional fields without hitting the Python restriction that
        non-default arguments cannot follow default arguments in a
        dataclass inheritance chain.
    """

    _: KW_ONLY

    # Task metadata
    task_id: str = field(default_factory=lambda: str(uuid4()))
    
    # Task priority (higher = more urgent)
    priority: int = 0
    
    # Correlation ID for tracking related tasks
    correlation_id: str | None = None
    
    # Additional metadata
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    @abstractmethod
    def task_type(self) -> str:
        """
        Return the task type identifier.
        
        This is used by the TaskRegistry to match tasks to plugins.
        
        Examples:
            "search_movie"
            "select_seats"
            "purchase_ticket"
        """
        raise NotImplementedError

    @abstractmethod
    def validate(self) -> tuple[bool, list[str]]:
        """
        Validate task inputs.
        
        Returns:
            Tuple of (is_valid, error_messages)
            
        Example:
            >>> task.validate()
            (True, [])  # Valid
            
            >>> task.validate()
            (False, ["Movie name is required", "City is required"])  # Invalid
        """
        raise NotImplementedError

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """
        Serialize task to dictionary.
        
        This is used for:
        - Logging
        - Storage
        - API responses
        - AI planner integration
        
        Returns:
            Dictionary representation of the task
        """
        raise NotImplementedError

    def __repr__(self) -> str:
        """String representation of the task."""
        return f"{self.__class__.__name__}(task_id={self.task_id}, type={self.task_type})"
