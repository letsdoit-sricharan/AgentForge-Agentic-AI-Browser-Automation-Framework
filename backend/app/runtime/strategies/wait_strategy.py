"""
Wait strategy.

Defines waiting behavior for the Agent Runtime.

Responsibilities:
    - Provide configurable delays.
    - Perform asynchronous waits.
    - Support future waiting policies.

This strategy does NOT:
    - Retry executions.
    - Handle browser waits.
    - Poll elements.
    - Know about workflows.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass


@dataclass(slots=True)
class WaitStrategy:
    """
    Generic wait strategy.

    Provides a configurable asynchronous delay.
    """

    delay: float = 1.0

    async def wait(self) -> None:
        """
        Wait asynchronously for the configured delay.
        """
        await asyncio.sleep(self.delay)

    def set_delay(self, delay: float) -> None:
        """
        Update the wait delay.

        Args:
            delay:
                Delay in seconds.

        Raises:
            ValueError:
                If delay is negative.
        """
        if delay < 0:
            raise ValueError("Delay cannot be negative.")

        self.delay = delay

    def reset(self) -> None:
        """
        Reset delay to the default value.
        """
        self.delay = 1.0