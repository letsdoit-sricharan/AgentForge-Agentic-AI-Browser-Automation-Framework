class AgentRuntimeError(Exception):
    """Base exception for Agent Runtime errors."""
    pass

class TerminatedError(AgentRuntimeError):
    """Raised when the agent loop is forcefully terminated."""
    pass

class MaxRetriesExceededError(AgentRuntimeError):
    """Raised when the agent exceeds the maximum allowed retries for a task."""
    pass

class GoalFailedError(AgentRuntimeError):
    """Raised when the agent concludes that the goal is unachievable."""
    pass
