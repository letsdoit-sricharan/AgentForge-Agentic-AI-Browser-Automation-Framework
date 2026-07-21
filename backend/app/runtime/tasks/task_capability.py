"""
Task Capabilities

Describes what capabilities a task requires for execution.

Responsibilities:
    - Define capability types
    - Support capability-based reasoning
    - Enable AI planner decision-making

Does NOT:
    - Execute tasks
    - Validate capabilities
    - Contain business logic
"""

from __future__ import annotations

from enum import Enum, auto


class TaskCapability(Enum):
    """
    Capabilities that tasks may require.
    
    Used by AI planners to understand what infrastructure or
    permissions are needed to execute a task.
    """

    # Browser capabilities
    REQUIRES_BROWSER = auto()
    REQUIRES_JAVASCRIPT = auto()
    REQUIRES_COOKIES = auto()
    
    # Authentication capabilities
    REQUIRES_AUTHENTICATION = auto()
    REQUIRES_LOGIN = auto()
    REQUIRES_2FA = auto()
    
    # Payment capabilities
    REQUIRES_PAYMENT = auto()
    REQUIRES_PAYMENT_METHOD = auto()
    REQUIRES_CREDIT_CARD = auto()
    
    # Human interaction capabilities
    REQUIRES_HUMAN_CONFIRMATION = auto()
    REQUIRES_CAPTCHA_SOLVE = auto()
    REQUIRES_OTP = auto()
    
    # Data capabilities
    REQUIRES_USER_DATA = auto()
    REQUIRES_LOCATION = auto()
    REQUIRES_PREFERENCES = auto()
    
    # Network capabilities
    REQUIRES_INTERNET = auto()
    REQUIRES_VPN = auto()
    
    # File capabilities
    REQUIRES_FILE_UPLOAD = auto()
    REQUIRES_FILE_DOWNLOAD = auto()
    
    # Time capabilities
    REQUIRES_REAL_TIME_EXECUTION = auto()
    REQUIRES_SCHEDULED_EXECUTION = auto()
    
    # Resource capabilities
    REQUIRES_HIGH_BANDWIDTH = auto()
    REQUIRES_LONG_EXECUTION_TIME = auto()
    
    # Security capabilities
    REQUIRES_SECURE_CONNECTION = auto()
    REQUIRES_ENCRYPTED_STORAGE = auto()
    
    # Multi-step capabilities
    REQUIRES_STATE_PERSISTENCE = auto()
    REQUIRES_ROLLBACK = auto()
    
    @classmethod
    def get_browser_capabilities(cls) -> set[TaskCapability]:
        """Get all browser-related capabilities."""
        return {
            cls.REQUIRES_BROWSER,
            cls.REQUIRES_JAVASCRIPT,
            cls.REQUIRES_COOKIES,
        }
    
    @classmethod
    def get_auth_capabilities(cls) -> set[TaskCapability]:
        """Get all authentication-related capabilities."""
        return {
            cls.REQUIRES_AUTHENTICATION,
            cls.REQUIRES_LOGIN,
            cls.REQUIRES_2FA,
        }
    
    @classmethod
    def get_payment_capabilities(cls) -> set[TaskCapability]:
        """Get all payment-related capabilities."""
        return {
            cls.REQUIRES_PAYMENT,
            cls.REQUIRES_PAYMENT_METHOD,
            cls.REQUIRES_CREDIT_CARD,
        }
    
    @classmethod
    def get_human_interaction_capabilities(cls) -> set[TaskCapability]:
        """Get all human interaction capabilities."""
        return {
            cls.REQUIRES_HUMAN_CONFIRMATION,
            cls.REQUIRES_CAPTCHA_SOLVE,
            cls.REQUIRES_OTP,
        }


def capability_to_string(capability: TaskCapability) -> str:
    """Convert capability to human-readable string."""
    return capability.name.replace("REQUIRES_", "").replace("_", " ").title()


def string_to_capability(s: str) -> TaskCapability | None:
    """Convert string to TaskCapability."""
    normalized = "REQUIRES_" + s.upper().replace(" ", "_")
    try:
        return TaskCapability[normalized]
    except KeyError:
        return None
