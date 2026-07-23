"""
Purpose:
    Workflow step that accepts the terms and conditions popup on BookMyShow.

Responsibilities:
    - Accept the terms and conditions popup to proceed to seat selection.

Does NOT:
    - Import Playwright.
    - Contain page selectors.
"""

from __future__ import annotations

from app.plugin_framework.workflow.workflow_context import WorkflowContext
from app.plugins.bookmyshow.pages.theatre_page import TheatrePage
from app.plugins.bookmyshow.steps.base_step import BaseBookMyShowStep


class ChooseShowStep(BaseBookMyShowStep):
    """
    Workflow step: accept terms/conditions to confirm the show selection.
    """

    @property
    def name(self) -> str:
        return "choose_show"

    @property
    def success_message(self) -> str:
        return "Show selected successfully."

    async def perform(
        self,
        context: WorkflowContext,
    ) -> None:
        page = TheatrePage(context)
        await page.accept_terms()