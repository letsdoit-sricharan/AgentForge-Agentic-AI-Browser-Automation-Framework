"""
Purpose:
    Playwright implementation of the Page interface.

Responsibilities:
    - Perform page-level browser operations.
    - Hide the Playwright Page object.
    - Translate Playwright exceptions into AgentForge exceptions.

Must NOT do:
    - Launch browsers.
    - Manage browser sessions.
    - Contain business logic.
"""

from __future__ import annotations
from pathlib import Path

from playwright.async_api import (
    Page as PlaywrightPageInstance,
    TimeoutError as PlaywrightTimeoutError,
)

from app.browser_engine.exceptions.browser_errors import PageError
from app.browser_engine.exceptions.navigation_errors import NavigationError
from app.browser_engine.exceptions.timeout_errors import BrowserTimeoutError
from app.browser_engine.implementations.playwright.playwright_locator import (
    PlaywrightLocator,
)
from app.browser_engine.interfaces.locator import Locator
from app.browser_engine.interfaces.page import Page
from app.browser_engine.models.load_state import LoadState
from app.browser_engine.models.navigation_options import NavigationOptions
from app.browser_engine.models.screenshot_options import ScreenshotOptions
from app.browser_engine.javascript.bridge import JavaScriptBridge
from app.browser_engine.implementations.playwright.playwright_javascript_bridge import PlaywrightJavaScriptBridge


class PlaywrightPage(Page):
    """
    Playwright implementation of the Page interface.
    """

    def __init__(self, page: PlaywrightPageInstance) -> None:
        self._page = page
        self._js_bridge = PlaywrightJavaScriptBridge(self._page)

    @property
    def js_bridge(self) -> JavaScriptBridge:
        return self._js_bridge

    async def goto(
        self,
        url: str,
        options: NavigationOptions | None = None,
    ) -> None:
        """
        Navigate to a URL.
        """
        try:
            kwargs = {}

            if options is not None:
                kwargs["wait_until"] = options.wait_until.value
                kwargs["timeout"] = options.timeout

            await self._page.goto(url, **kwargs)

        except PlaywrightTimeoutError as exc:
            raise BrowserTimeoutError(
                f"Navigation to '{url}' timed out."
            ) from exc

        except Exception as exc:
            raise NavigationError(
                f"Failed to navigate to '{url}'."
            ) from exc

    async def title(self) -> str:
        """
        Return the current page title.
        """
        try:
            return await self._page.title()

        except Exception as exc:
            raise PageError(
                "Failed to retrieve page title."
            ) from exc

    @property
    def url(self) -> str:
        """
        Return the current page URL.
        """
        return self._page.url

    def locator(self, selector: str) -> Locator:
        # Avoid circular import
        from app.browser_engine.implementations.playwright.playwright_locator import (
            PlaywrightLocator,
        )

        pw_locator = self._page.locator(selector)
        return PlaywrightLocator(pw_locator)

    def canvas(self, engine_type: str, dom_selector: str):
        from app.actions.locator.canvas_locator import CanvasLocatorBuilder
        return CanvasLocatorBuilder(self, engine_type, dom_selector)

    async def screenshot(
        self,
        options: ScreenshotOptions,
    ) -> Path:
        """
        Capture a screenshot of the current page.

        Returns:
            Path to the saved screenshot.
        """
        try:
            await self._page.screenshot(
                path=str(options.path),
                full_page=options.full_page,
                type=options.image_type.value,
                quality=options.quality,
            )

            return options.path

        except Exception as exc:
            raise PageError(
                "Failed to capture screenshot."
            ) from exc

    async def wait_for_load(
        self,
        state: LoadState = LoadState.LOAD,
        timeout: int | None = None,
    ) -> None:
        """
        Wait until the page reaches the specified load state.
        """
        try:
            await self._page.wait_for_load_state(
                state=state.value,
                timeout=timeout,
            )

        except PlaywrightTimeoutError as exc:
            raise BrowserTimeoutError(
                "Timed out while waiting for page load."
            ) from exc

    async def close(self) -> None:
        """
        Close the page.
        """
        try:
            await self._page.close()

        except Exception as exc:
            raise PageError(
                "Failed to close page."
            ) from exc

    async def reload(self) -> None:
        """
        Reload the current page.

        Note:
            This is an implementation convenience method and is
            not currently part of the Page interface.
        """
        try:
            await self._page.reload()

        except PlaywrightTimeoutError as exc:
            raise BrowserTimeoutError(
                "Page reload timed out."
            ) from exc

        except Exception as exc:
            raise PageError(
                "Failed to reload page."
            ) from exc

    async def press_key(
        self,
        key: str,
    ) -> None:
        """
        Press a single keyboard key.
        """
        try:
            await self._page.keyboard.press(key)
        except Exception as exc:
            raise PageError(
                f"Failed to press key '{key}'."
            ) from exc

    async def type_text(
        self,
        text: str,
        delay: float | None = None,
    ) -> None:
        """
        Type text into the page (unfocused).
        """
        try:
            kwargs = {}
            if delay is not None:
                kwargs["delay"] = delay
            await self._page.keyboard.type(text, **kwargs)
        except Exception as exc:
            raise PageError(
                "Failed to type text."
            ) from exc

    async def hotkey(
        self,
        *keys: str,
    ) -> None:
        """
        Press a combination of keyboard keys (hotkey).
        """
        try:
            shortcut = "+".join(keys)
            await self._page.keyboard.press(shortcut)
        except Exception as exc:
            raise PageError(
                f"Failed to press hotkey combination {keys}."
            ) from exc

    async def move_mouse(
        self,
        x: float,
        y: float,
    ) -> None:
        """
        Move the mouse cursor to the specified coordinates.
        """
        try:
            await self._page.mouse.move(x, y)
        except Exception as exc:
            raise PageError(
                f"Failed to move mouse to ({x}, {y})."
            ) from exc

    async def mouse_click(
        self,
        x: float,
        y: float,
    ) -> None:
        """
        Click at the specified coordinates.
        """
        try:
            await self._page.mouse.click(x, y)
        except Exception as exc:
            raise PageError(
                f"Failed to click at ({x}, {y})."
            ) from exc

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
        try:
            await self._page.mouse.move(start_x, start_y)
            await self._page.mouse.down()
            await self._page.mouse.move(end_x, end_y)
            await self._page.mouse.up()
        except Exception as exc:
            raise PageError(
                f"Failed to drag from ({start_x}, {start_y}) to ({end_x}, {end_y})."
            ) from exc

    async def drag_and_drop(
        self,
        source_selector: str,
        target_selector: str,
    ) -> None:
        """
        Drag an element from the source selector to the target selector.
        """
        try:
            await self._page.drag_and_drop(source_selector, target_selector)
        except Exception as exc:
            raise PageError(
                f"Failed to drag and drop from '{source_selector}' to '{target_selector}'."
            ) from exc

    async def mouse_wheel(
        self,
        delta_x: float,
        delta_y: float,
    ) -> None:
        """
        Scroll the mouse wheel.
        """
        try:
            await self._page.mouse.wheel(delta_x, delta_y)
        except Exception as exc:
            raise PageError(
                "Failed to scroll mouse wheel."
            ) from exc

    async def scroll(
        self,
        delta_x: float = 0,
        delta_y: float = 0,
    ) -> None:
        """
        Scroll the current page.
        """
        try:
            await self._page.evaluate(
                f"window.scrollBy({delta_x}, {delta_y})"
            )
        except Exception as exc:
            raise PageError(
                f"Failed to scroll page by ({delta_x}, {delta_y})."
            ) from exc

    async def scroll_to(
        self,
        x: float,
        y: float,
    ) -> None:
        """
        Scroll to the specified page coordinates.
        """
        try:
            await self._page.evaluate(
                f"window.scrollTo({x}, {y})"
            )
        except Exception as exc:
            raise PageError(
                f"Failed to scroll to ({x}, {y})."
            ) from exc

    async def evaluate(
        self,
        script: str,
        argument: object | None = None,
    ) -> object:
        """
        Execute JavaScript in the page context.
        """
        try:
            return await self._page.evaluate(script, argument)
        except Exception as exc:
            raise PageError(
                "Failed to evaluate script in page context."
            ) from exc

    async def pdf(
        self,
        path: Path,
    ) -> Path:
        """
        Save the current page as a PDF.
        """
        try:
            await self._page.pdf(path=str(path))
            return path
        except Exception as exc:
            raise PageError(
                "Failed to generate PDF from page."
            ) from exc

    async def upload_file(
        self,
        selector: str,
        file_path: Path,
    ) -> None:
        """
        Upload a file using the specified file input selector.
        """
        try:
            await self._page.locator(selector).set_input_files(str(file_path))
        except Exception as exc:
            raise PageError(
                f"Failed to upload file '{file_path}' using selector '{selector}'."
            ) from exc

    async def expect_download(self) -> Path:
        """
        Wait for the next browser download.
        """
        try:
            download = await self._page.wait_for_event("download")
            path = await download.path()
            return Path(path)
        except Exception as exc:
            raise PageError(
                "Failed to wait for download."
            ) from exc