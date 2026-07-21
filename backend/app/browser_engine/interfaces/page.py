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

    @abstractmethod
    async def press_key(
        self,
        key: str,
    ) -> None:
        """
        Press a single keyboard key.

        Args:
            key:
                The key to press (e.g., "Enter", "Escape").
        """
        raise NotImplementedError

    @abstractmethod
    async def type_text(
        self,
        text: str,
        delay: float | None = None,
    ) -> None:
        """
        Type text into the page (unfocused).

        Args:
            text:
                The text to type.

            delay:
                Delay in milliseconds between keystrokes.
        """
        raise NotImplementedError

    @abstractmethod
    async def hotkey(
        self,
        *keys: str,
    ) -> None:
        """
        Press a combination of keyboard keys (hotkey).

        Args:
            keys:
                Sequence of keys to press (e.g., "Control", "A").
        """
        raise NotImplementedError

    @abstractmethod
    async def move_mouse(
        self,
        x: float,
        y: float,
    ) -> None:
        """
        Move the mouse cursor to the specified coordinates.
        """
        raise NotImplementedError

    @abstractmethod
    async def drag(
        self,
        start_x: float,
        start_y: float,
        end_x: float,
        end_y: float,
    ) -> None:
        """
        Drag the mouse from one coordinate to another.
        """
        raise NotImplementedError

    @abstractmethod
    async def drag_and_drop(
        self,
    source_selector: str,
        target_selector: str,
    ) -> None:
        """
        Drag an element from the source selector to the target selector.
        """
        raise NotImplementedError

    @abstractmethod
    async def mouse_wheel(
        self,
        delta_x: float,
        delta_y: float,
    ) -> None:
        """
        Scroll the mouse wheel.
        """
        raise NotImplementedError

    @abstractmethod
    async def scroll(
        self,
        delta_x: float = 0,
        delta_y: float = 0,
    ) -> None:
        """
        Scroll the current page.

        Args:
            delta_x:
                Horizontal scroll offset.
            delta_y:
                Vertical scroll offset.
        """
        raise NotImplementedError

    @abstractmethod
    async def scroll_to(
        self,
        x: float,
        y: float,
    ) -> None:
        """
        Scroll to the specified page coordinates.

        Args:
            x:
                Horizontal page coordinate.
            y:
                Vertical page coordinate.
        """
        raise NotImplementedError

    @abstractmethod
    async def evaluate(
    self,
    script: str,
    argument: object | None = None,
    ) -> object:
        """
        Execute JavaScript in the page context.

        Args:
            script:
                JavaScript source code.

            argument:
                Optional argument passed to the script.

        Returns:
            The value returned by the script.
        """
        raise NotImplementedError

    @abstractmethod
    async def pdf(
        self,
        path: Path,
    ) -> Path:
        """
        Save the current page as a PDF.

        Args:
            path:
                Destination path.

        Returns:
            Path to the generated PDF.
        """
        raise NotImplementedError

    @abstractmethod
    async def upload_file(
        self,
        selector: str,
        file_path: Path,
    ) -> None:
        """
        Upload a file using the specified file input selector.
        """
        raise NotImplementedError

    @abstractmethod
    async def expect_download(self) -> Path:
        """
        Wait for the next browser download.

        Returns:
            Path to the downloaded file.
        """
        raise NotImplementedError