from app.plugins.interfaces.plugin_metadata import PluginMetadata
from app.plugins.interfaces.agent_plugin import AgentPlugin

metadata = PluginMetadata(
    name="{{cookiecutter.plugin_name}}",
    version="1.0.0",
    description="{{cookiecutter.plugin_description}}",
    author="Auto Generated",
    capabilities=["{{cookiecutter.plugin_name}}"]
)

class {{cookiecutter.plugin_name.title().replace('_', '')}}Plugin(AgentPlugin):
    """
    Main entrypoint for {{cookiecutter.plugin_name}}.
    """
    
    def __init__(self):
        super().__init__(metadata)

def get_plugin() -> AgentPlugin:
    return {{cookiecutter.plugin_name.title().replace('_', '')}}Plugin()
