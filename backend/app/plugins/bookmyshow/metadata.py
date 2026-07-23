"""
Purpose:
    Defines the metadata for the BookMyShow plugin.

Responsibilities:
    - Describe the plugin.
    - Provide plugin capabilities.
    - Expose reusable plugin metadata.

Does NOT:
    - Execute workflows.
    - Perform browser actions.
    - Contain business logic.
"""

from __future__ import annotations

from app.plugins.interfaces.plugin_metadata import PluginMetadata

BOOKMYSHOW_METADATA = PluginMetadata(
    name="bookmyshow",
    version="1.0.0",
    description="Movie ticket booking automation plugin.",
    author="AgentForge",
    capabilities=(
        "movie_booking",
        "theatre_selection",
        "show_selection",
        "seat_selection",
        "ticket_download",
    ),
)

# Alias for backwards compatibility
METADATA = BOOKMYSHOW_METADATA
