"""
Purpose:
    Opens the BookMyShow homepage.

Responsibilities:
    - Coordinate the business operation of opening the homepage.
    - Delegate browser interactions to the HomePage Page Object.

Does NOT:
    - Import Playwright.
    - Perform browser automation directly.
    - Contain page selectors.
"""

from __future__ import annotations

from app.plugin_framework.steps.step_result import StepResult
from app.plugin_framework.steps.workflow_step import WorkflowStep
from app.plugin_framework.workflow.workflow_context import WorkflowContext

from app.plugins.bookmyshow.pages.home_page import HomePage


class OpenHomepageStep(WorkflowStep):
    """
    Workflow step responsible for opening the BookMyShow homepage.
    """

    @property
    def name(self) -> str:
        return "open_homepage"

    async def execute(
        self,
        context: WorkflowContext,
    ) -> StepResult:
        """
        Open and verify the BookMyShow homepage.
        """

        home_page = HomePage(context)

        try:
            await home_page.open()

            await home_page.wait_until_loaded()

            loaded = await home_page.verify_loaded()

            if not loaded:
                return StepResult(
                    success=False,
                    message="Failed to verify BookMyShow homepage.",
                )

            return StepResult(
                success=True,
                message="BookMyShow homepage opened successfully.",
            )

        except Exception as exc:
            return StepResult(
                success=False,
                message=f"Failed to open homepage: {exc}",
            )