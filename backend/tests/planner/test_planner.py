import pytest
from typing import List

from app.planner.models import Intent, Entity, Goal, Plan, PlanningResult
from app.planner.interfaces import IntentRecognizer, ParameterExtractor, TaskPlanner
from app.planner.default_planner import DefaultPlanner
from app.planner.exceptions import IntentRecognitionError
from app.runtime.execution.execution_request import ExecutionRequest

class MockIntentRecognizer(IntentRecognizer):
    async def recognize(self, prompt: str) -> Intent:
        if "error" in prompt.lower():
            raise IntentRecognitionError("Could not understand intent.")
        return Intent(name="BookTickets", confidence=0.95)

class MockParameterExtractor(ParameterExtractor):
    async def extract(self, prompt: str, intent: Intent) -> List[Entity]:
        return [
            Entity(name="movie", value="Inception"),
            Entity(name="city", value="Mumbai")
        ]

class MockTaskPlanner(TaskPlanner):
    async def plan_task(self, goal: Goal) -> ExecutionRequest:
        inputs = {e.name: e.value for e in goal.entities}
        return ExecutionRequest(
            plugin="bookmyshow",
            workflow="book_ticket",
            inputs=inputs
        )

@pytest.fixture
def planner():
    return DefaultPlanner(
        intent_recognizer=MockIntentRecognizer(),
        parameter_extractor=MockParameterExtractor(),
        task_planner=MockTaskPlanner()
    )

@pytest.mark.asyncio
async def test_generate_plan_success(planner):
    prompt = "Book 2 tickets for Inception in Mumbai"
    result = await planner.generate_plan(prompt)
    
    assert result.is_successful is True
    assert result.plan is not None
    assert result.error_message is None
    
    # Check Goal Formulation
    goal = result.plan.goal
    assert goal.original_prompt == prompt
    assert goal.intent.name == "BookTickets"
    assert len(goal.entities) == 2
    assert goal.entities[0].name == "movie"
    assert goal.entities[0].value == "Inception"
    
    # Check ExecutionRequest translation
    assert len(result.plan.execution_requests) == 1
    req = result.plan.execution_requests[0]
    assert req.plugin == "bookmyshow"
    assert req.workflow == "book_ticket"
    assert req.inputs["city"] == "Mumbai"

@pytest.mark.asyncio
async def test_generate_plan_failure(planner):
    prompt = "This should trigger an error intent."
    result = await planner.generate_plan(prompt)
    
    assert result.is_successful is False
    assert result.plan is None
    assert "Could not understand intent" in result.error_message
