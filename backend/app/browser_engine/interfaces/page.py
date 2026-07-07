"""
Purpose:
    Defines the abstract Page interface for the AgentForge Browser Engine.

Responsibilities:
    - Define page-level browser operations.
    - Create locators for interacting with page elements.
    - Expose page metadata.
    - Support navigation and screenshots.

Must NOT do:
    - Import Playwright.
    - Contain implementation logic.
    - Perform element interactions directly.
    - Handle logging, retries, or browser lifecycle.
"""

from __future__ import annotations
from pathlib import Path

from abc import ABC, abstractmethod
from pathlib import Path

from app.browser_engine.interfaces.locator import Locator
from app.browser_engine.models.load_state import LoadState
from app.browser_engine.models.navigation_options import NavigationOptions
from app.browser_engine.models.screenshot_options import ScreenshotOptions


class Page(ABC):
    """
    Abstract interface representing a single browser page or tab.

    Concrete implementations must completely hide the underlying
    browser automation library from the rest of AgentForge.
    """

    @abstractmethod
    async def goto(
        self,
        url: str,
        options: NavigationOptions | None = None,
    ) -> None:
        """
        Navigate to the specified URL.

        Args:
            url:
                Destination URL.

            options:
                Optional navigation configuration.
        """
        raise NotImplementedError

    @abstractmethod
    async def title(self) -> str:
        """
        Retrieve the current page title.

        Returns:
            The current page title.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def url(self) -> str:
        """
        Retrieve the current page URL.

        Returns:
            The current page URL.
        """
        raise NotImplementedError

    @abstractmethod
    def locator(self, selector: str) -> Locator:
        """
        Create a locator for the given selector.

        Args:
            selector:
                CSS, XPath, text, or other supported selector.

        Returns:
            A browser-agnostic Locator instance.
        """
        raise NotImplementedError

    @abstractmethod
    async def screenshot(
    self,
    options: ScreenshotOptions,
    )    -> Path:
        """
        Capture a screenshot of the current page.

        Returns:
            Path:
                The filesystem path where the screenshot
                was successfully saved.
        """
        raise NotImplementedError

    @abstractmethod
    async def wait_for_load(
        self,
        state: LoadState = LoadState.LOAD,
        timeout: int | None = None,
    ) -> None:
        """
        Wait until the page reaches the specified load state.

        Args:
            state:
                Desired page load state.

            timeout:
                Maximum wait time in milliseconds.
        """
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        """
        Close the page.
        """
        raise NotImplementedError