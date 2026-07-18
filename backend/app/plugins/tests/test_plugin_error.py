"""
Tests for Plugin Exceptions.

Run:
    python -m app.plugins.tests.test_plugin_errors
"""

from app.plugins.exceptions import (
    PluginError,
    PluginExecutionError,
    PluginLoadError,
    PluginRegistrationError,
    PluginValidationError,
)


def test_exception_inheritance() -> None:
    """Verify exception hierarchy."""

    assert issubclass(PluginLoadError, PluginError)
    assert issubclass(PluginRegistrationError, PluginError)
    assert issubclass(PluginValidationError, PluginError)
    assert issubclass(PluginExecutionError, PluginError)

    print("✓ Exception inheritance test passed.")


def test_raise_plugin_load_error() -> None:
    """Verify PluginLoadError."""

    try:
        raise PluginLoadError("Unable to load plugin.")
    except PluginLoadError as exc:
        assert str(exc) == "Unable to load plugin."

    print("✓ PluginLoadError test passed.")


def test_raise_plugin_registration_error() -> None:
    """Verify PluginRegistrationError."""

    try:
        raise PluginRegistrationError("Plugin already registered.")
    except PluginRegistrationError as exc:
        assert str(exc) == "Plugin already registered."

    print("✓ PluginRegistrationError test passed.")


def test_raise_plugin_validation_error() -> None:
    """Verify PluginValidationError."""

    try:
        raise PluginValidationError("Invalid plugin.")
    except PluginValidationError as exc:
        assert str(exc) == "Invalid plugin."

    print("✓ PluginValidationError test passed.")


def test_raise_plugin_execution_error() -> None:
    """Verify PluginExecutionError."""

    try:
        raise PluginExecutionError("Execution failed.")
    except PluginExecutionError as exc:
        assert str(exc) == "Execution failed."

    print("✓ PluginExecutionError test passed.")


def run_tests() -> None:
    print("\n" + "=" * 60)
    print("Running Plugin Exception Tests")
    print("=" * 60)

    test_exception_inheritance()
    test_raise_plugin_load_error()
    test_raise_plugin_registration_error()
    test_raise_plugin_validation_error()
    test_raise_plugin_execution_error()

    print("-" * 60)
    print("✅ All Plugin Exception tests passed!")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()