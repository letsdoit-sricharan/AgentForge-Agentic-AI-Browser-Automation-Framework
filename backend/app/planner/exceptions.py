class PlannerError(Exception):
    """Base exception for Planner errors."""
    pass

class IntentRecognitionError(PlannerError):
    """Raised when the planner cannot recognize a valid intent from the prompt."""
    pass

class ParameterExtractionError(PlannerError):
    """Raised when required parameters cannot be extracted for a recognized intent."""
    pass

class PlanGenerationError(PlannerError):
    """Raised when the planner fails to generate a valid execution plan for the goal."""
    pass
