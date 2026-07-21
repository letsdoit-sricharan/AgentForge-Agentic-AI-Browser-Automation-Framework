"""
Runtime working memory.
"""

from __future__ import annotations

from typing import Any

from .variables import RuntimeVariable


class RuntimeMemory:
    """
    Simple in-memory key-value storage used during execution.
    """

    def __init__(self) -> None:
        self._storage: dict[str, Any] = {}

    def set(
        self,
        key: str | RuntimeVariable,
        value: Any,
    ) -> None:
        self._storage[str(key)] = value

    def get(
        self,
        key: str | RuntimeVariable,
        default: Any = None,
    ) -> Any:
        return self._storage.get(str(key), default)

    def remove(
        self,
        key: str | RuntimeVariable,
    ) -> None:
        self._storage.pop(str(key), None)

    def contains(
        self,
        key: str | RuntimeVariable,
    ) -> bool:
        return str(key) in self._storage

    def clear(self) -> None:
        self._storage.clear()

    def snapshot(self) -> dict[str, Any]:
        """
        Returns a shallow copy of runtime memory.
        """
        return dict(self._storage)

    @property
    def size(self) -> int:
        return len(self._storage)
