
import pytest

from app.agent.interfaces import (
    Executor,
    GoalMonitor,
    ObservationCollector,
    Replanner,
    StateEvaluator,
    TerminationStrategy,
)
from app.agent.loop import DefaultAgent
from app.agent.models import (
    AgentSession,
    EvaluationAction,
    EvaluationResult,
    Observation,
)
from app.planner.interfaces import Planner
from app.planner.models import Goal, Plan, PlanningResult
from app.runtime.execution.execution_request import ExecutionRequest

# Mocks specific for E2E validation

class E2EPlanner(Planner):
    async def generate_plan(self, prompt: str) -> PlanningResult:
        # Create execution requests for the full booking flow
        reqs = [
            ExecutionRequest(plugin="bookmyshow", workflow="booking", inputs={"show_date": "10", "count": 2})
        ]
        plan = Plan(goal=Goal(original_prompt=prompt, intent="BookTicket"), execution_requests=reqs)
        return PlanningResult(plan=plan, is_successful=True)

class E2EExecutor(Executor):
    def __init__(self):
        self.executed = []

    async def execute(self, request: ExecutionRequest) -> any:
        self.executed.append(request)
        return f"Executed {request.workflow} successfully."

class E2EObservationCollector(ObservationCollector):
    async def collect(self, execution_result: any) -> Observation:
        return Observation(is_success=True, message=str(execution_result))

class E2EGoalMonitor(GoalMonitor):
    def __init__(self):
        self.call_count = 0

    async def is_goal_achieved(self, session: AgentSession, observation: Observation) -> bool:
        self.call_count += 1
        # The goal is achieved after 1 execution cycle completes
        return self.call_count >= 1

class E2EStateEvaluator(StateEvaluator):
    async def evaluate(self, session: AgentSession, observation: Observation) -> EvaluationResult:
        return EvaluationResult(action=EvaluationAction.CONTINUE, reasoning="Continue execution")

class E2EReplanner(Replanner):
    async def replan(self, session: AgentSession) -> PlanningResult:
        plan = Plan(goal=session.goal, execution_requests=[])
        return PlanningResult(plan=plan, is_successful=True)

class E2ETerminationStrategy(TerminationStrategy):
    def should_terminate(self, session: AgentSession) -> bool:
        return len(session.observation_history) > 5


@pytest.fixture
def e2e_agent():
    return DefaultAgent(
        planner=E2EPlanner(),
        executor=E2EExecutor(),
        observation_collector=E2EObservationCollector(),
        goal_monitor=E2EGoalMonitor(),
        state_evaluator=E2EStateEvaluator(),
        replanner=E2EReplanner(),
        termination_strategy=E2ETerminationStrategy()
    )


@pytest.mark.asyncio
async def test_e2e_booking_workflow(e2e_agent):
    """
    Test that the agent can successfully plan and execute the BookMyShow workflow.
    """
    prompt = "Book 2 tickets for Inception on the 10th"

    session = await e2e_agent.run(prompt)

    assert session.status == "COMPLETED"
    assert len(session.observation_history) == 1
    assert session.observation_history[0].is_success is True

    executor = e2e_agent.executor
    assert len(executor.executed) == 1
    assert executor.executed[0].plugin == "bookmyshow"
    assert executor.executed[0].workflow == "booking"
