"""
Tests for PluginLoader.

Run:
    python -m app.plugins.tests.test_plugin_loader
"""

from app.plugins.exceptions import PluginValidationError
from app.plugins.interfaces import (
    Plugin,
    PluginContext,
    PluginMetadata,
)
from app.plugins.manager import PluginLoader
from app.plugins.registry import PluginRegistry


class DummyPlugin(Plugin):

    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="dummy",
            version="1.0.0",
            description="Dummy Plugin",
            author="AgentForge",
        )

    def initialize(self, context: PluginContext) -> None:
        pass

    def execute(self, task):
        return task

    def shutdown(self) -> None:
        pass


class InvalidPlugin(Plugin):

    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="",
            version="",
            description="Invalid",
            author="AgentForge",
        )

    def initialize(self, context: PluginContext) -> None:
        pass

    def execute(self, task):
        return task

    def shutdown(self) -> None:
        pass


def test_load_plugin() -> None:

    registry = PluginRegistry()

    loader = PluginLoader(registry)

    plugin = loader.load(DummyPlugin)

    assert registry.exists("dummy")

    assert plugin.metadata.name == "dummy"

    print("✓ Plugin loading test passed.")


def test_load_many() -> None:

    registry = PluginRegistry()

    loader = PluginLoader(registry)

    plugins = loader.load_many([DummyPlugin])

    assert len(plugins) == 1

    assert registry.exists("dummy")

    print("✓ Multiple plugin loading test passed.")


def test_validation() -> None:

    registry = PluginRegistry()

    loader = PluginLoader(registry)

    try:

        loader.load(InvalidPlugin)

    except PluginValidationError:

        print("✓ Plugin validation test passed.")

    else:

        raise AssertionError("Validation should fail.")


def test_discover_placeholder() -> None:

    registry = PluginRegistry()

    loader = PluginLoader(registry)

    try:

        loader.discover()

    except NotImplementedError:

        print("✓ Discover placeholder test passed.")

    else:

        raise AssertionError("discover() should raise NotImplementedError.")


def run_tests() -> None:

    print("\n" + "=" * 60)
    print("Running PluginLoader Tests")
    print("=" * 60)

    test_load_plugin()
    test_load_many()
    test_validation()
    test_discover_placeholder()

    print("-" * 60)
    print("✅ All PluginLoader tests passed!")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()