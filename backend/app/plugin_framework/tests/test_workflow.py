"""
Tests for Workflow.

Run:
    python -m app.plugin_framework.tests.test_workflow
"""

from app.plugin_framework.workflow import Workflow


class DummyWorkflow(Workflow):

    @property
    def name(self) -> str:
        return "dummy_workflow"

    @property
    def steps(self):
        return []

    def execute(self, context):
        return None


def test_workflow_name():

    workflow = DummyWorkflow()

    assert workflow.name == "dummy_workflow"

    print("✓ Workflow name test passed.")


def test_steps():

    workflow = DummyWorkflow()

    assert workflow.steps == []

    print("✓ Workflow steps test passed.")


def run_tests():

    print("\n" + "=" * 60)
    print("Running Workflow Tests")
    print("=" * 60)

    test_workflow_name()
    test_steps()

    print("-" * 60)
    print("✅ All Workflow tests passed!")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()