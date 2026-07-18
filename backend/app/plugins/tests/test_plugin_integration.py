"""
Integration test for the complete Plugin Infrastructure.

Run:
    python -m app.plugins.tests.test_plugin_integration
"""

from app.plugins.interfaces import (
    Plugin,
    PluginContext,
    PluginMetadata,
)
from app.plugins.manager import (
    PluginLoader,
    PluginManager,
)
from app.plugins.models import PluginState
from app.plugins.registry import PluginRegistry


class DummyPlugin(Plugin):
    """
    Simple plugin used to verify the complete plugin lifecycle.
    """

    def __init__(self):
        self.initialized = False
        self.shutdown_called = False

    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="dummy",
            version="1.0.0",
            description="Integration Test Plugin",
            author="AgentForge",
        )

    def initialize(self, context: PluginContext) -> None:
        self.initialized = True

    def execute(self, task):
        return f"Processed: {task}"

    def shutdown(self) -> None:
        self.shutdown_called = True


def create_context() -> PluginContext:
    return PluginContext(
        runtime=None,
        actions=None,
        memory=None,
        configuration=None,
        logger=None,
    )


def run_integration_test() -> None:

    print("\n" + "=" * 65)
    print("Plugin Infrastructure Integration Test")
    print("=" * 65)

    # ------------------------------------------------------------------
    # Create Registry
    # ------------------------------------------------------------------

    registry = PluginRegistry()

    print("✓ PluginRegistry created.")

    # ------------------------------------------------------------------
    # Create Loader
    # ------------------------------------------------------------------

    loader = PluginLoader(registry)

    print("✓ PluginLoader created.")

    # ------------------------------------------------------------------
    # Load Plugin
    # ------------------------------------------------------------------

    managed = loader.load(DummyPlugin)

    assert registry.exists("dummy")

    print("✓ Plugin successfully loaded.")

    # ------------------------------------------------------------------
    # Verify ManagedPlugin
    # ------------------------------------------------------------------

    assert managed.plugin.metadata.name == "dummy"

    assert managed.state == PluginState.CREATED

    print("✓ ManagedPlugin successfully created.")

    # ------------------------------------------------------------------
    # Create Manager
    # ------------------------------------------------------------------

    manager = PluginManager(registry)

    print("✓ PluginManager created.")

    # ------------------------------------------------------------------
    # Initialize Plugin
    # ------------------------------------------------------------------

    context = create_context()

    manager.initialize(
        "dummy",
        context,
    )

    managed = manager.get_managed_plugin("dummy")

    assert managed.state == PluginState.INITIALIZED

    print("✓ Plugin initialized.")

    # ------------------------------------------------------------------
    # Execute Plugin
    # ------------------------------------------------------------------

    result = manager.execute(
        "dummy",
        "Book two tickets",
    )

    assert result == "Processed: Book two tickets"

    assert managed.execution_count == 1

    assert managed.state == PluginState.RUNNING

    print("✓ Plugin executed successfully.")

    # ------------------------------------------------------------------
    # Shutdown Plugin
    # ------------------------------------------------------------------

    manager.shutdown("dummy")

    assert managed.state == PluginState.STOPPED

    print("✓ Plugin shutdown completed.")

    # ------------------------------------------------------------------
    # Final Verification
    # ------------------------------------------------------------------

    assert managed.plugin.initialized

    assert managed.plugin.shutdown_called

    print("-" * 65)
    print("✅ Plugin Infrastructure Integration Test Passed!")
    print("=" * 65)


if __name__ == "__main__":
    run_integration_test()