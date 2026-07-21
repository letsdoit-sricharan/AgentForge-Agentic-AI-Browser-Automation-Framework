"""
Execution queue.

Provides a simple FIFO queue for execution contexts.
"""

from __future__ import annotations

from collections import deque

from app.runtime.execution.execution_context import ExecutionContext


class ExecutionQueue:
    """
    FIFO queue for execution contexts.

    The queue is intentionally simple. It manages only the
    ordering of execution contexts and does not perform any
    scheduling or execution.
    """

    def __init__(self) -> None:
        self._queue: deque[ExecutionContext] = deque()

    def enqueue(
        self,
        context: ExecutionContext,
    ) -> None:
        """
        Add an execution context to the end of the queue.
        """
        self._queue.append(context)

    def dequeue(self) -> ExecutionContext | None:
        """
        Remove and return the next execution context.

        Returns:
            ExecutionContext | None:
                The next execution context, or None if empty.
        """
        if self.is_empty:
            return None

        return self._queue.popleft()

    def peek(self) -> ExecutionContext | None:
        """
        Return the next execution context without removing it.
        """
        if self.is_empty:
            return None

        return self._queue[0]

    def clear(self) -> None:
        """
        Remove all queued execution contexts.
        """
        self._queue.clear()

    @property
    def size(self) -> int:
        """
        Number of queued execution contexts.
        """
        return len(self._queue)

    @property
    def is_empty(self) -> bool:
        """
        True if the queue contains no items.
        """
        return len(self._queue) == 0

    def __len__(self) -> int:
        """
        Return the number of execution contexts currently in the queue.
        """
        return len(self._queue)
