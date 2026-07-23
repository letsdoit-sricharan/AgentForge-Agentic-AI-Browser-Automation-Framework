"""
Tests for the Locator package public API.
"""

from app.actions.locator import (
    FindAction,
    WaitForElementAction,
    WaitUntilHiddenAction,
    validate_selector,
)


def test_locator_imports():

    print("\n==============================")
    print(" Locator Package Import Test ")
    print("==============================\n")

    exports = [
        FindAction,
        WaitForElementAction,
        WaitUntilHiddenAction,
        validate_selector,
    ]

    for item in exports:
        print(f"✓ {item.__name__}")

    print("\nTesting selector validation...")

    assert validate_selector("#login") == "#login"

    print("✓ validate_selector()")

    print("\n✅ Locator Package Import Test Passed!")


if __name__ == "__main__":
    test_locator_imports()
