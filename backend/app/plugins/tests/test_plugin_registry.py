"""
Tests for PluginRegistry.

Run:
    python -m app.plugins.tests.test_plugin_registry
"""

from app.plugins.exceptions import PluginRegistrationError
from app.plugins.interfaces import (
    Plugin,
    PluginContext,
    PluginMetadata,
)
from app.plugins.models import ManagedPlugin, PluginState
from app.plugins.registry import PluginRegistry


class DummyPlugin(Plugin):

    @property
    def metadata(self):
        return PluginMetadata(
            name="dummy",
            version="1.0",
            description="Dummy",
            author="AgentForge",
        )

    def initialize(self, context: PluginContext):
        pass

    def execute(self, task):
        return task

    def shutdown(self):
        pass


def test_register_plugin():

    registry = PluginRegistry()

    managed = registry.register(DummyPlugin())

    assert isinstance(managed, ManagedPlugin)

    assert managed.state == PluginState.CREATED

    print("✓ Plugin registration test passed.")


def test_get_plugin():

    registry = PluginRegistry()

    registry.register(DummyPlugin())

    managed = registry.get("dummy")

    assert isinstance(managed, ManagedPlugin)

    assert managed.plugin.metadata.name == "dummy"

    print("✓ Plugin retrieval test passed.")


def test_duplicate_registration():

    registry = PluginRegistry()

    registry.register(DummyPlugin())

    try:

        registry.register(DummyPlugin())

    except PluginRegistrationError:

        print("✓ Duplicate registration test passed.")

    else:

        raise AssertionError()


def test_unregister():

    registry = PluginRegistry()

    registry.register(DummyPlugin())

    registry.unregister("dummy")

    assert not registry.exists("dummy")

    print("✓ Plugin unregistration test passed.")


def test_clear():

    registry = PluginRegistry()

    registry.register(DummyPlugin())

    registry.clear()

    assert registry.list_plugins() == []

    print("✓ Registry clear test passed.")


def run_tests():

    print("\n" + "=" * 60)
    print("Running PluginRegistry Tests")
    print("=" * 60)

    test_register_plugin()
    test_get_plugin()
    test_duplicate_registration()
    test_unregister()
    test_clear()

    print("-" * 60)
    print("✅ All PluginRegistry tests passed!")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()