"""
Purpose:
    Defines the reusable base class for all plugin page objects.

Responsibilities:
    - Store the WorkflowContext.
    - Provide convenient access to browser resources.
    - Expose framework services to page objects.
    - Act as the base class for all plugin pages.

Does NOT:
    - Import Playwright.
    - Contain website-specific logic.
    - Execute workflow orchestration.
"""

from __future__ import annotations

from abc import ABC
from typing import final

from app.browser_engine.interfaces.page import Page
from app.browser_engine.interfaces.session import Session
from app.plugin_framework.workflow.workflow_context import WorkflowContext


class BasePage(ABC):
    """
    Base class for all plugin page objects.
    """

    def __init__(
        self,
        context: WorkflowContext,
    ) -> None:
        self._context = context

    @property
    @final
    def context(self) -> WorkflowContext:
        """
        Return the workflow execution context.
        """
        return self._context

    @property
    @final
    def plugin_context(self):
        """
        Return the plugin context.
        """
        return self._context.plugin_context

    @property
    @final
    def page(self) -> Page:
        """
        Return the active browser page.
        """
        return self._context.page

    @property
    @final
    def session(self) -> Session:
        """
        Return the active browser session.
        """
        return self._context.session

    @property
    @final
    def runtime(self):
        """
        Shortcut to the runtime service.
        """
        return self.plugin_context.runtime

    @property
    @final
    def actions(self):
        """
        Shortcut to the Action Library.
        """
        return self.plugin_context.actions

    @property
    @final
    def memory(self):
        """
        Shortcut to runtime memory.
        """
        return self.plugin_context.memory

    @property
    @final
    def configuration(self):
        """
        Shortcut to plugin configuration.
        """
        return self.plugin_context.configuration

    @property
    @final
    def logger(self):
        """
        Shortcut to framework logger.
        """
        return self.plugin_context.logger
