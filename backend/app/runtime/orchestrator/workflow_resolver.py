"""
Workflow Resolver

Resolves which workflow should execute inside a plugin.

Responsibilities:
    - Locate workflow within a plugin
    - Validate workflow existence
    - Prepare workflow execution configuration
    - Return workflow resolution result

Does NOT:
    - Execute workflows
    - Know about specific workflows (BookingWorkflow, etc.)
    - Manage browser lifecycle
    - Import Playwright
"""

from __future__ import annotations

import inspect
import logging
from typing import TYPE_CHECKING, Any

from app.runtime.orchestrator.exceptions import WorkflowResolutionError
from app.runtime.orchestrator.models import WorkflowResolution

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


class WorkflowResolver:
    """
    Resolves workflows within plugins.
    """

    def __init__(self) -> None:
        """
        Initialize the workflow resolver.
        """
        self._logger = logger

    def resolve(
        self,
        plugin: Any,
        workflow_name: str,
    ) -> WorkflowResolution:
        """
        Resolve a workflow within a plugin.

        Args:
            plugin: Plugin instance to search
            workflow_name: Name of the workflow to resolve

        Returns:
            WorkflowResolution with workflow instance or error

        Raises:
            WorkflowResolutionError: If resolution fails critically
        """
        plugin_name = plugin.metadata.name
        self._logger.debug(
            f"Resolving workflow '{workflow_name}' in plugin '{plugin_name}'"
        )

        try:
            # Try to find workflow attribute on plugin
            workflow = self._find_workflow_attribute(plugin, workflow_name)

            if workflow is None:
                error_msg = (
                    f"Workflow '{workflow_name}' not found in plugin '{plugin_name}'"
                )
                self._logger.error(error_msg)
                return WorkflowResolution(
                    workflow_name=workflow_name,
                    found=False,
                    error=error_msg,
                )

            # Validate workflow has execute method
            if not self._validate_workflow(workflow):
                error_msg = (
                    f"Workflow '{workflow_name}' does not have required 'execute' method"
                )
                self._logger.error(error_msg)
                return WorkflowResolution(
                    workflow_name=workflow_name,
                    found=True,
                    workflow=workflow,
                    error=error_msg,
                )

            # Successfully resolved
            self._logger.info(
                f"Successfully resolved workflow '{workflow_name}' "
                f"in plugin '{plugin_name}'"
            )
            return WorkflowResolution(
                workflow_name=workflow_name,
                found=True,
                workflow=workflow,
            )

        except Exception as e:
            error_msg = f"Error resolving workflow: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise WorkflowResolutionError(workflow_name, plugin_name, str(e)) from e

    def _find_workflow_attribute(
        self,
        plugin: Any,
        workflow_name: str,
    ) -> Any:
        """
        Find workflow attribute in plugin.

        Searches for:
        1. Direct attribute: plugin.workflow_name
        2. Workflows dict: plugin.workflows[workflow_name]
        3. Private attribute: plugin._workflow_name

        Args:
            plugin: Plugin instance
            workflow_name: Name of workflow

        Returns:
            Workflow instance or None
        """
        # Try direct attribute
        if hasattr(plugin, workflow_name):
            return getattr(plugin, workflow_name)

        # Try workflows dict
        if hasattr(plugin, "workflows"):
            workflows = getattr(plugin, "workflows")
            if isinstance(workflows, dict) and workflow_name in workflows:
                return workflows[workflow_name]

        # Try private attribute
        private_name = f"_{workflow_name}"
        if hasattr(plugin, private_name):
            return getattr(plugin, private_name)

        # Try with _workflow suffix
        workflow_attr = f"_{workflow_name}_workflow"
        if hasattr(plugin, workflow_attr):
            return getattr(plugin, workflow_attr)

        return None

    def _validate_workflow(
        self,
        workflow: Any,
    ) -> bool:
        """
        Validate that workflow has required methods.

        Args:
            workflow: Workflow instance to validate

        Returns:
            True if valid, False otherwise
        """
        # Check for execute method
        if not hasattr(workflow, "execute"):
            return False

        # Check that execute is callable
        execute = getattr(workflow, "execute")
        if not callable(execute):
            return False

        return True

    def list_workflows(
        self,
        plugin: Any,
    ) -> list[str]:
        """
        List all available workflows in a plugin.

        Args:
            plugin: Plugin instance

        Returns:
            List of workflow names
        """
        workflow_names = []

        # Check for workflows dict
        if hasattr(plugin, "workflows"):
            workflows = getattr(plugin, "workflows")
            if isinstance(workflows, dict):
                workflow_names.extend(workflows.keys())

        # Scan plugin attributes for workflow-like objects
        for attr_name in dir(plugin):
            if attr_name.startswith("_"):
                continue

            attr = getattr(plugin, attr_name, None)
            if attr is None:
                continue

            # Check if it has execute method
            if self._validate_workflow(attr):
                if attr_name not in workflow_names:
                    workflow_names.append(attr_name)

        return workflow_names

    def get_workflow_info(
        self,
        workflow: Any,
    ) -> dict[str, Any]:
        """
        Get information about a workflow.

        Args:
            workflow: Workflow instance

        Returns:
            Dictionary with workflow information
        """
        info = {
            "name": getattr(workflow, "__class__", type(workflow)).__name__,
            "has_execute": hasattr(workflow, "execute"),
            "is_async": False,
            "parameters": [],
        }

        # Check if execute is async
        if hasattr(workflow, "execute"):
            execute = getattr(workflow, "execute")
            info["is_async"] = inspect.iscoroutinefunction(execute)

            # Get execute method signature
            try:
                sig = inspect.signature(execute)
                info["parameters"] = list(sig.parameters.keys())
            except Exception:
                pass

        return info
