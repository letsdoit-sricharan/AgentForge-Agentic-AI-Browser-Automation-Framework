"""
Tests for locator utilities.
"""

from app.actions.locator.locator_utils import validate_selector


def test_locator_utils():

    print("\n==============================")
    print(" Locator Utils Test ")
    print("==============================\n")

    selector = validate_selector("#login")

    assert selector == "#login"

    print("✓ Valid selector accepted")

    try:
        validate_selector("   ")
    except ValueError:
        print("✓ Empty selector rejected")

    print("\n✅ Locator Utils Test Passed!")


if __name__ == "__main__":
    test_locator_utils()