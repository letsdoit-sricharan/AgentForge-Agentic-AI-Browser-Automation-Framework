"""
Tests for PluginManager.

Run:
    python -m app.plugins.tests.test_plugin_manager
"""

from app.plugins.interfaces import (
    Plugin,
    PluginContext,
    PluginMetadata,
)
from app.plugins.manager import PluginManager
from app.plugins.models import PluginState
from app.plugins.registry import PluginRegistry


class DummyPlugin(Plugin):

    def __init__(self):
        self.initialized = False
        self.shutdown_called = False

    @property
    def metadata(self):
        return PluginMetadata(
            name="dummy",
            version="1.0.0",
            description="Dummy Plugin",
            author="AgentForge",
        )

    def initialize(self, context):
        self.initialized = True

    def execute(self, task):
        return f"Executed {task}"

    def shutdown(self):
        self.shutdown_called = True


def create_manager():

    registry = PluginRegistry()

    registry.register(DummyPlugin())

    return PluginManager(registry)


def create_context():

    return PluginContext(
        runtime=None,
        actions=None,
        memory=None,
        configuration=None,
        logger=None,
    )


def test_initialize():

    manager = create_manager()

    manager.initialize(
        "dummy",
        create_context(),
    )

    managed = manager.get_managed_plugin("dummy")

    assert managed.state == PluginState.INITIALIZED

    assert managed.context is not None

    assert managed.initialized_at is not None

    print("✓ Plugin initialization test passed.")


def test_execute():

    manager = create_manager()

    manager.initialize(
        "dummy",
        create_context(),
    )

    result = manager.execute(
        "dummy",
        "Book Ticket",
    )

    managed = manager.get_managed_plugin("dummy")

    assert result == "Executed Book Ticket"

    assert managed.execution_count == 1

    assert managed.last_execution_at is not None

    assert managed.state == PluginState.RUNNING

    print("✓ Plugin execution test passed.")


def test_shutdown():

    manager = create_manager()

    manager.initialize(
        "dummy",
        create_context(),
    )

    manager.shutdown("dummy")

    managed = manager.get_managed_plugin("dummy")

    assert managed.state == PluginState.STOPPED

    print("✓ Plugin shutdown test passed.")


def test_helper_methods():

    manager = create_manager()

    manager.initialize(
        "dummy",
        create_context(),
    )

    assert manager.is_initialized("dummy")

    manager.execute(
        "dummy",
        "Task",
    )

    assert manager.is_running("dummy")

    print("✓ Plugin helper methods test passed.")


def run_tests():

    print("\n" + "=" * 60)
    print("Running PluginManager Tests")
    print("=" * 60)

    test_initialize()
    test_execute()
    test_shutdown()
    test_helper_methods()

    print("-" * 60)
    print("✅ All PluginManager tests passed!")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()