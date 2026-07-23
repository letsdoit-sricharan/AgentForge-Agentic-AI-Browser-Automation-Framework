"""
Browser executor.

Coordinates browser resources for runtime executions.

The BrowserExecutor is responsible for acquiring browser
resources, invoking browser-based tasks, and ensuring proper
resource cleanup. It remains completely browser-independent
by relying only on Browser Engine interfaces.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from app.browser_engine.interfaces.browser import Browser
from app.browser_engine.interfaces.session import Session
from app.runtime.exceptions.execution_error import ExecutionError
from app.runtime.execution.execution_context import ExecutionContext

# Type alias for a browser task
BrowserTask = Callable[
    [ExecutionContext, Session],
    Awaitable[Any],
]


class BrowserExecutor:
    """
    Coordinates browser execution.

    This class owns no browser logic itself. It simply manages
    the lifecycle of a browser session for a single execution.
    """

    def __init__(self, browser: Browser) -> None:
        """
        Initialize the executor.

        Args:
            browser:
                Browser Engine browser abstraction.
        """
        self._browser = browser

    async def execute(
        self,
        context: ExecutionContext,
        task: BrowserTask,
    ) -> Any:
        """
        Execute a browser task.

        Args:
            context:
                Runtime execution context.

            task:
                Async callable receiving the execution context
                and a browser session.

        Returns:
            Result produced by the task.

        Raises:
            ExecutionError:
                If browser execution fails.
        """
        session: Session | None = None

        try:
            session = await self._browser.new_session()

            return await task(
                context,
                session,
            )

        except Exception as exc:
            raise ExecutionError(
                f"Browser execution failed: {exc}"
            ) from exc

        finally:
            if session is not None:
                await session.close()
