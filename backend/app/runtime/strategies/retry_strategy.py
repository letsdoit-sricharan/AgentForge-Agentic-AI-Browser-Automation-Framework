"""
Retry strategy.

Defines the retry policy used by the Agent Runtime.

Responsibilities:
    - Decide whether another retry is allowed.
    - Track retry attempts.
    - Calculate retry delays.

This class does NOT perform retries. It only provides
the policy that the execution engine follows.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass()
class RetryStrategy:
    """
    Generic retry strategy.

    Supports configurable retry limits and exponential
    backoff calculation.
    """

    max_retries: int = 3

    initial_delay: float = 1.0

    backoff_factor: float = 2.0

    max_delay: float = 30.0

    current_attempt: int = 0

    @property
    def retries_remaining(self) -> int:
        """
        Number of retries remaining.
        """
        return max(0, self.max_retries - self.current_attempt)

    @property
    def exhausted(self) -> bool:
        """
        Returns True when no retries remain.
        """
        return self.current_attempt >= self.max_retries

    def should_retry(self) -> bool:
        """
        Determine whether another retry is allowed.
        """
        return not self.exhausted

    def record_retry(self) -> None:
        """
        Record a retry attempt.

        Raises:
            RuntimeError:
                If retry limit has already been reached.
        """
        if self.exhausted:
            raise RuntimeError(
                "Maximum retry attempts exceeded."
            )

        self.current_attempt += 1

    def reset(self) -> None:
        """
        Reset retry state.
        """
        self.current_attempt = 0

    def next_delay(self) -> float:
        """
        Calculate the delay before the next retry.

        Uses exponential backoff.

        Returns:
            Delay in seconds.
        """
        delay = (
            self.initial_delay
            * (self.backoff_factor ** self.current_attempt)
        )

        return min(delay, self.max_delay)
