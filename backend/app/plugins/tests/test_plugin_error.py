"""
Tests for Plugin Exceptions.

Run:
    python -m app.plugins.tests.test_plugin_errors
"""

from app.plugins.exceptions import (
    PluginAlreadyRegisteredError,
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

    # PluginRegistrationError is an alias for PluginAlreadyRegisteredError
    assert PluginRegistrationError is PluginAlreadyRegisteredError

    print("✓ Exception inheritance test passed.")


def test_raise_plugin_load_error() -> None:
    """Verify PluginLoadError."""

    try:
        raise PluginLoadError("my_plugin", "module not found")
    except PluginLoadError as exc:
        assert "my_plugin" in str(exc)
        assert exc.plugin_name == "my_plugin"
        assert exc.reason == "module not found"

    print("✓ PluginLoadError test passed.")


def test_raise_plugin_registration_error() -> None:
    """Verify PluginRegistrationError (alias for PluginAlreadyRegisteredError)."""

    try:
        raise PluginRegistrationError("my_plugin")
    except PluginRegistrationError as exc:
        assert "my_plugin" in str(exc)
        assert exc.plugin_name == "my_plugin"

    print("✓ PluginRegistrationError test passed.")


def test_raise_plugin_validation_error() -> None:
    """Verify PluginValidationError."""

    try:
        raise PluginValidationError("my_plugin", ["field_x is required"])
    except PluginValidationError as exc:
        assert "my_plugin" in str(exc)
        assert exc.plugin_name == "my_plugin"

    print("✓ PluginValidationError test passed.")


def test_raise_plugin_execution_error() -> None:
    """Verify PluginExecutionError."""

    try:
        raise PluginExecutionError("my_plugin", "step failed")
    except PluginExecutionError as exc:
        assert "my_plugin" in str(exc)
        assert exc.plugin_name == "my_plugin"
        assert exc.reason == "step failed"

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