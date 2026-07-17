"""
Tests for Action exceptions.
"""

from app.actions.exceptions import (
    ActionError,
    ActionExecutionError,
    ActionTimeoutError,
    InvalidActionError,
    ElementNotFoundError,
    ElementNotInteractableError,
)


def test_action_exceptions():

    print("\n==============================")
    print(" Action Exceptions Test ")
    print("==============================\n")

    exceptions = [
        ActionError("Generic action error"),
        ActionExecutionError("Execution failed"),
        ActionTimeoutError("Timed out"),
        InvalidActionError("Invalid action"),
        ElementNotFoundError("Element not found"),
        ElementNotInteractableError("Element not interactable"),
    ]

    for exc in exceptions:
        print(f"{exc.__class__.__name__}: {exc}")

    assert issubclass(ActionExecutionError, ActionError)
    assert issubclass(ActionTimeoutError, ActionExecutionError)
    assert issubclass(InvalidActionError, ActionError)
    assert issubclass(ElementNotFoundError, ActionExecutionError)
    assert issubclass(ElementNotInteractableError, ActionExecutionError)

    print("\n✅ Action Exceptions Test Passed!")


if __name__ == "__main__":
    test_action_exceptions()