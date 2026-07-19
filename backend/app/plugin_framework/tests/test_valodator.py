"""
Tests for Validator.

Run:
    python -m app.plugin_framework.tests.test_validator
"""

from typing import Any

from app.plugin_framework.validators.validator import Validator
from app.plugin_framework.validators.validation_result import ValidationResult


class DummyValidator(Validator):
    """
    Dummy validator used for testing.
    """

    @property
    def name(self) -> str:
        return "dummy_validator"

    def validate(
        self,
        data: Any,
    ) -> ValidationResult:

        if data:
            return ValidationResult(
                valid=True,
                message="Validation succeeded.",
            )

        return ValidationResult(
            valid=False,
            message="Validation failed.",
        )


def test_validator_name() -> None:
    """
    Test validator name.
    """

    validator = DummyValidator()

    assert validator.name == "dummy_validator"

    print("✓ Validator name test passed.")


def test_successful_validation() -> None:
    """
    Test successful validation.
    """

    validator = DummyValidator()

    result = validator.validate(
        {
            "movie": "Coolie",
        }
    )

    assert result.valid is True
    assert result.message == "Validation succeeded."

    print("✓ Successful validator test passed.")


def test_failed_validation() -> None:
    """
    Test failed validation.
    """

    validator = DummyValidator()

    result = validator.validate(None)

    assert result.valid is False
    assert result.message == "Validation failed."

    print("✓ Failed validator test passed.")


def run_tests() -> None:

    print("\n" + "=" * 65)
    print("Validator Tests")
    print("=" * 65)

    test_validator_name()
    test_successful_validation()
    test_failed_validation()

    print("-" * 65)
    print("✅ All Validator tests passed!")
    print("=" * 65)


if __name__ == "__main__":
    run_tests()