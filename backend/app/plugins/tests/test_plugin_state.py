"""
Tests for PluginState.

Run:
    python -m app.plugins.tests.test_plugin_state
"""

from app.plugins.models import PluginState


def test_plugin_states_exist() -> None:
    """Verify all plugin states exist."""

    assert PluginState.CREATED.value == "created"
    assert PluginState.LOADED.value == "loaded"
    assert PluginState.INITIALIZED.value == "initialized"
    assert PluginState.RUNNING.value == "running"
    assert PluginState.STOPPED.value == "stopped"
    assert PluginState.FAILED.value == "failed"

    print("✓ Plugin states existence test passed.")


def test_plugin_state_is_enum() -> None:
    """Verify PluginState behaves as an Enum."""

    assert PluginState.CREATED != PluginState.RUNNING
    assert isinstance(PluginState.CREATED, PluginState)

    print("✓ PluginState enum behavior test passed.")


def run_tests() -> None:
    print("\n" + "=" * 60)
    print("Running PluginState Tests")
    print("=" * 60)

    test_plugin_states_exist()
    test_plugin_state_is_enum()

    print("-" * 60)
    print("✅ All PluginState tests passed!")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()