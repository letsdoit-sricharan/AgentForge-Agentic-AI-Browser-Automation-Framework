from app.plugins.interfaces.plugin_metadata import PluginMetadata
from app.plugins.interfaces.agent_plugin import AgentPlugin

metadata = PluginMetadata(
    name="test_plugin",
    version="1.0.0",
    description="A new AgentForge plugin",
    author="Auto Generated",
    capabilities=["test_plugin"]
)

class TestPluginPlugin(AgentPlugin):
    """
    Main entrypoint for test_plugin.
    """
    
    def __init__(self):
        super().__init__(metadata)

def get_plugin() -> AgentPlugin:
    return TestPluginPlugin()
