"""
Purpose:
    Placeholder workflow step for opening the BookMyShow homepage.
"""

from __future__ import annotations

from app.plugins.bookmyshow.steps.base_step import BaseBookMyShowStep


class OpenHomepageStep(BaseBookMyShowStep):
    """
    Workflow step for opening the BookMyShow homepage.
    """

    @property
    def name(self) -> str:
        return "open_homepage"

    @property
    def success_message(self) -> str:
        return "BookMyShow homepage opened successfully."