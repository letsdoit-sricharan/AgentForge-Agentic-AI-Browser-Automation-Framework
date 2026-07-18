"""
Tests for PluginContext.

Run:
    python -m app.plugins.tests.test_plugin_context
"""

from app.plugins.interfaces import PluginContext


class DummyRuntime:
    pass


class DummyActions:
    pass


class DummyMemory:
    pass


class DummyConfiguration:
    pass


class DummyLogger:
    pass


def test_plugin_context_creation() -> None:
    """Verify PluginContext stores framework services."""

    context = PluginContext(
        runtime=DummyRuntime(),
        actions=DummyActions(),
        memory=DummyMemory(),
        configuration=DummyConfiguration(),
        logger=DummyLogger(),
    )

    assert isinstance(context.runtime, DummyRuntime)
    assert isinstance(context.actions, DummyActions)
    assert isinstance(context.memory, DummyMemory)
    assert isinstance(context.configuration, DummyConfiguration)
    assert isinstance(context.logger, DummyLogger)

    print("✓ PluginContext creation test passed.")


def run_tests() -> None:
    print("\n" + "=" * 60)
    print("Running PluginContext Tests")
    print("=" * 60)

    test_plugin_context_creation()

    print("-" * 60)
    print("✅ All PluginContext tests passed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()