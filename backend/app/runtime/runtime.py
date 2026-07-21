"""
Public runtime API.

Coordinates the complete execution lifecycle of an AgentForge request.
"""

from __future__ import annotations

from app.runtime.execution.execution_request import ExecutionRequest


class Runtime:
    """
    Public entry point into the Agent Runtime.
    """

    async def execute(
        self,
        request: ExecutionRequest,
    ):
        """
        Execute an AgentForge request.

        Implementation added incrementally.
        """
        raise NotImplementedError
