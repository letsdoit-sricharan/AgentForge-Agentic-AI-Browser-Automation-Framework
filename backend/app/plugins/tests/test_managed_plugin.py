"""
Tests for ManagedPlugin.

Run:
    python -m app.plugins.tests.test_managed_plugin
"""

from app.plugins.interfaces import (
    Plugin,
    PluginContext,
    PluginMetadata,
)
from app.plugins.models import (
    ManagedPlugin,
    PluginStatus,
)


class DummyPlugin(Plugin):

    @property
    def metadata(self):
        return PluginMetadata(
            name="dummy",
            version="1.0",
            description="Dummy Plugin",
            author="AgentForge",
        )

    def initialize(self, context: PluginContext):
        pass

    async def execute(self, task):
        return task

    def shutdown(self):
        pass


def test_default_values():

    managed = ManagedPlugin(
        plugin=DummyPlugin()
    )

    # ManagedPlugin uses .status (PluginStatus), not .state (PluginState)
    assert managed.status == PluginStatus.UNLOADED

    assert managed.execution_count == 0

    assert managed.context is None

    assert managed.last_error is None

    assert managed.initialized_at is None

    assert managed.last_execution_at is None

    print("✓ Default ManagedPlugin state test passed.")


def test_plugin_storage():

    plugin = DummyPlugin()

    managed = ManagedPlugin(plugin)

    assert managed.plugin is plugin

    print("✓ Plugin storage test passed.")


def test_state_update():

    managed = ManagedPlugin(
        DummyPlugin()
    )

    # Status transitions use .status, and PluginStatus enum (not PluginState)
    managed.status = PluginStatus.READY

    assert managed.status == PluginStatus.READY

    print("✓ State update test passed.")


def test_execution_counter():

    managed = ManagedPlugin(
        DummyPlugin()
    )

    managed.execution_count += 1

    managed.execution_count += 1

    assert managed.execution_count == 2

    print("✓ Execution counter test passed.")


def run_tests():

    print("\n" + "=" * 60)
    print("Running ManagedPlugin Tests")
    print("=" * 60)

    test_default_values()
    test_plugin_storage()
    test_state_update()
    test_execution_counter()

    print("-" * 60)
    print("✅ All ManagedPlugin tests passed!")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()