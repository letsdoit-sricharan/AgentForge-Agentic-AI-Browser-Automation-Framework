"""
Integration test for the Plugin Framework.

Run:
    python -m app.plugin_framework.tests.test_plugin_framework_integration
"""

from __future__ import annotations

from typing import Any

from app.plugin_framework.steps.workflow_step import WorkflowStep
from app.plugin_framework.steps.step_result import StepResult
from app.plugin_framework.validators.validator import Validator
from app.plugin_framework.validators.validation_result import ValidationResult
from app.plugin_framework.workflow.workflow import Workflow
from app.plugin_framework.workflow.workflow_context import WorkflowContext
from app.plugin_framework.workflow.workflow_result import WorkflowResult
from app.plugins.interfaces import PluginContext


# ------------------------------------------------------------------
# Dummy Plugin Context
# ------------------------------------------------------------------


def create_plugin_context() -> PluginContext:
    return PluginContext(
        runtime=None,
        actions=None,
        configuration=None,
        memory=None,
        logger=None,
    )


# ------------------------------------------------------------------
# Dummy Validator
# ------------------------------------------------------------------


class DummyValidator(Validator):

    @property
    def name(self) -> str:
        return "dummy_validator"

    def validate(self, data: Any) -> ValidationResult:

        if data.get("movie"):
            return ValidationResult(
                valid=True,
                message="Movie validated.",
            )

        return ValidationResult(
            valid=False,
            message="Movie missing.",
        )


# ------------------------------------------------------------------
# Dummy Steps
# ------------------------------------------------------------------


class SearchMovieStep(WorkflowStep):

    @property
    def name(self) -> str:
        return "SearchMovie"

    def execute(
        self,
        context: WorkflowContext,
    ) -> StepResult:

        context.state["movie_found"] = True

        print("✓ SearchMovieStep executed.")

        return StepResult(
            success=True,
            message="Movie searched.",
        )


class SelectSeatsStep(WorkflowStep):

    @property
    def name(self) -> str:
        return "SelectSeats"

    def execute(
        self,
        context: WorkflowContext,
    ) -> StepResult:

        context.state["seats_selected"] = True

        print("✓ SelectSeatsStep executed.")

        return StepResult(
            success=True,
            message="Seats selected.",
        )


# ------------------------------------------------------------------
# Dummy Workflow
# ------------------------------------------------------------------


class DummyWorkflow(Workflow):

    def __init__(self) -> None:
        super().__init__()

        self.add_step(SearchMovieStep())
        self.add_step(SelectSeatsStep())

        self.validator = DummyValidator()

    @property
    def name(self) -> str:
        return "dummy_workflow"

    def execute(
        self,
        context: WorkflowContext,
    ) -> WorkflowResult:

        validation = self.validator.validate(context.input_data)

        assert validation.valid

        print("✓ Validator executed.")

        for step in self.steps:

            result = step.execute(context)

            assert result.success

        return WorkflowResult(
            success=True,
            message="Workflow completed successfully.",
        )


# ------------------------------------------------------------------
# Integration Test
# ------------------------------------------------------------------


def run_integration_test() -> None:

    print("\n" + "=" * 65)
    print("Plugin Framework Integration Test")
    print("=" * 65)

    workflow = DummyWorkflow()

    print("✓ Workflow created.")

    context = WorkflowContext(
        plugin_context=create_plugin_context(),
        input_data={
            "movie": "Coolie",
            "tickets": 2,
        },
    )

    print("✓ WorkflowContext created.")

    result = workflow.execute(context)

    assert result.success

    assert context.state["movie_found"] is True
    assert context.state["seats_selected"] is True

    print("✓ Workflow executed successfully.")

    print("-" * 65)
    print("✅ Plugin Framework Integration Test Passed!")
    print("=" * 65)


if __name__ == "__main__":
    run_integration_test()