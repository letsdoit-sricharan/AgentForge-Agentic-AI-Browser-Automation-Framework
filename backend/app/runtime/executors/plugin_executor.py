"""
Plugin executor.

Bridges the Agent Runtime and the Plugin Framework.

Responsibilities:
    - Acquire a browser page from the session.
    - Build a WorkflowContext.
    - Execute a plugin.
    - Keep browser lifecycle outside the plugin.
"""

from __future__ import annotations

from typing import Any

from app.browser_engine.interfaces.session import Session
from app.plugin_framework.workflow.workflow_context import WorkflowContext
from app.plugins.interfaces.plugin import Plugin
from app.plugins.interfaces.plugin_context import PluginContext
from app.runtime.execution.execution_context import ExecutionContext


class PluginExecutor:
    """
    Executes a plugin inside an active browser session.
    """

    async def execute(
        self,
        execution_context: ExecutionContext,
        plugin: Plugin,
        plugin_context: PluginContext,
        session: Session,
        task: Any,
    ) -> Any:
        """
        Execute a plugin using the supplied browser session.
        """

        page = await session.new_page()

        workflow_context = WorkflowContext(
            plugin_context=plugin_context,
            page=page,
            session=session,
            input_data={
                "booking_request": task,
            },
        )

        return await plugin.execute(
            workflow_context,
        )