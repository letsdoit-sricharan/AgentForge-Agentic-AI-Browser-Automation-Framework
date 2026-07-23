"""
Tests for Plugin interface.

Run:
    python -m app.plugins.tests.test_plugin
"""

from app.plugins.interfaces import (
    Plugin,
    PluginContext,
    PluginMetadata,
)


class DummyPlugin(Plugin):
    """Simple implementation used for testing."""

    def __init__(self):
        self.initialized = False
        self.shutdown_called = False

    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="dummy",
            version="1.0.0",
            description="Dummy Plugin",
            author="AgentForge",
        )

    def initialize(self, context: PluginContext) -> None:
        self.initialized = True

    def execute(self, task):
        return f"Executed: {task}"

    def shutdown(self) -> None:
        self.shutdown_called = True


def test_plugin_metadata() -> None:
    plugin = DummyPlugin()

    assert plugin.metadata.name == "dummy"
    assert plugin.metadata.version == "1.0.0"

    print("✓ Plugin metadata test passed.")


def test_plugin_lifecycle() -> None:
    plugin = DummyPlugin()

    context = PluginContext(
        runtime=None,
        actions=None,
        memory=None,
        configuration=None,
        logger=None,
    )

    plugin.initialize(context)

    assert plugin.initialized

    result = plugin.execute("book ticket")

    assert result == "Executed: book ticket"

    plugin.shutdown()

    assert plugin.shutdown_called

    print("✓ Plugin lifecycle test passed.")


def run_tests() -> None:
    print("\n" + "=" * 60)
    print("Running Plugin Interface Tests")
    print("=" * 60)

    test_plugin_metadata()
    test_plugin_lifecycle()

    print("-" * 60)
    print("✅ All Plugin Interface tests passed!")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()
