import pytest
from typing import Any

from app.agent.loop import DefaultAgent
from app.agent.interfaces import (
    Executor, GoalMonitor, ObservationCollector, 
    Replanner, StateEvaluator, TerminationStrategy
)
from app.agent.models import AgentSession, EvaluationAction, EvaluationResult, Observation
from app.planner.interfaces import Planner
from app.planner.models import Goal, Intent, Plan, PlanningResult
from app.runtime.execution.execution_request import ExecutionRequest
from app.agent.exceptions import TerminatedError

class MockPlanner(Planner):
    async def generate_plan(self, prompt: str) -> PlanningResult:
        req = ExecutionRequest(plugin="test", workflow="test")
        plan = Plan(goal=Goal(original_prompt=prompt, intent=Intent("Test")), execution_requests=[req])
        return PlanningResult(plan=plan, is_successful=True)

class MockExecutor(Executor):
    def __init__(self):
        self.call_count = 0
    async def execute(self, request: ExecutionRequest) -> Any:
        self.call_count += 1
        return "Executed"

class MockObservationCollector(ObservationCollector):
    async def collect(self, execution_result: Any) -> Observation:
        return Observation(is_success=True, message=str(execution_result))

class MockGoalMonitor(GoalMonitor):
    def __init__(self, achieve_on_call=2):
        self.call_count = 0
        self.achieve_on_call = achieve_on_call
        
    async def is_goal_achieved(self, session: AgentSession, observation: Observation) -> bool:
        self.call_count += 1
        return self.call_count >= self.achieve_on_call

class MockStateEvaluator(StateEvaluator):
    def __init__(self, actions):
        self.actions = actions
        self.call_count = 0
        
    async def evaluate(self, session: AgentSession, observation: Observation) -> EvaluationResult:
        action = self.actions[self.call_count] if self.call_count < len(self.actions) else EvaluationAction.CONTINUE
        self.call_count += 1
        return EvaluationResult(action=action, reasoning="Mock evaluation")

class MockReplanner(Replanner):
    async def replan(self, session: AgentSession) -> PlanningResult:
        req = ExecutionRequest(plugin="test", workflow="replanned")
        plan = Plan(goal=session.goal, execution_requests=[req])
        return PlanningResult(plan=plan, is_successful=True)

class MockTerminationStrategy(TerminationStrategy):
    def __init__(self, max_calls=10):
        self.call_count = 0
        self.max_calls = max_calls
        
    def should_terminate(self, session: AgentSession) -> bool:
        self.call_count += 1
        return self.call_count > self.max_calls

@pytest.fixture
def base_mocks():
    return {
        "planner": MockPlanner(),
        "executor": MockExecutor(),
        "observation_collector": MockObservationCollector(),
        "goal_monitor": MockGoalMonitor(),
        "state_evaluator": MockStateEvaluator([EvaluationAction.CONTINUE]),
        "replanner": MockReplanner(),
        "termination_strategy": MockTerminationStrategy()
    }

@pytest.mark.asyncio
async def test_agent_successful_completion(base_mocks):
    base_mocks["goal_monitor"] = MockGoalMonitor(achieve_on_call=2) # Achieved after execute + check
    agent = DefaultAgent(**base_mocks)
    
    session = await agent.run("do something")
    
    assert session.status == "COMPLETED"
    assert base_mocks["executor"].call_count == 1
    assert len(session.observation_history) == 1

@pytest.mark.asyncio
async def test_agent_evaluator_terminate(base_mocks):
    base_mocks["state_evaluator"] = MockStateEvaluator([EvaluationAction.TERMINATE])
    base_mocks["goal_monitor"] = MockGoalMonitor(achieve_on_call=99)
    agent = DefaultAgent(**base_mocks)
    
    with pytest.raises(TerminatedError):
        await agent.run("do something")

@pytest.mark.asyncio
async def test_agent_replan(base_mocks):
    base_mocks["state_evaluator"] = MockStateEvaluator([EvaluationAction.REPLAN, EvaluationAction.CONTINUE])
    base_mocks["goal_monitor"] = MockGoalMonitor(achieve_on_call=3) # initial check, replan check, finish check
    agent = DefaultAgent(**base_mocks)
    
    session = await agent.run("do something")
    
    assert session.status == "COMPLETED"
    assert base_mocks["executor"].call_count == 2
    assert len(session.observation_history) == 2
    assert session.current_plan.execution_requests == [] # Exhausted
