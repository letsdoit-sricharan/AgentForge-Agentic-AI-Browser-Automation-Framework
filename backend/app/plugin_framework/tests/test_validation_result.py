"""
Tests for ValidationResult.

Run:
    python -m app.plugin_framework.tests.test_validation_result
"""

from app.plugin_framework.validators.validation_result import ValidationResult


def test_successful_validation() -> None:
    """
    Test a successful validation result.
    """

    result = ValidationResult(
        valid=True,
        message="Validation succeeded.",
        details={
            "validated": True,
        },
    )

    assert result.valid is True
    assert result.message == "Validation succeeded."
    assert result.details["validated"] is True

    print("✓ Successful ValidationResult test passed.")


def test_failed_validation() -> None:
    """
    Test a failed validation result.
    """

    result = ValidationResult(
        valid=False,
        message="Movie name is missing.",
        details={
            "missing_field": "movie_name",
        },
    )

    assert result.valid is False
    assert result.message == "Movie name is missing."
    assert result.details["missing_field"] == "movie_name"

    print("✓ Failed ValidationResult test passed.")


def test_default_values() -> None:
    """
    Test default values.
    """

    result = ValidationResult(valid=True)

    assert result.message == ""
    assert result.details == {}

    print("✓ ValidationResult default values test passed.")


def run_tests() -> None:

    print("\n" + "=" * 65)
    print("ValidationResult Tests")
    print("=" * 65)

    test_successful_validation()
    test_failed_validation()
    test_default_values()

    print("-" * 65)
    print("✅ All ValidationResult tests passed!")
    print("=" * 65)


if __name__ == "__main__":
    run_tests()