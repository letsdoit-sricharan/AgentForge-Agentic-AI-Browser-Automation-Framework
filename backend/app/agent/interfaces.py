from abc import ABC, abstractmethod
from typing import Any

from app.agent.models import AgentSession, EvaluationResult, Observation
from app.planner.models import PlanningResult
from app.runtime.execution.execution_request import ExecutionRequest


class Executor(ABC):
    @abstractmethod
    async def execute(self, request: ExecutionRequest) -> Any:
        """Executes a single planned request and returns a raw result/error."""
        raise NotImplementedError

class ObservationCollector(ABC):
    @abstractmethod
    async def collect(self, execution_result: Any) -> Observation:
        """Translates raw execution results into a standardized Observation."""
        raise NotImplementedError

class GoalMonitor(ABC):
    @abstractmethod
    async def is_goal_achieved(self, session: AgentSession, observation: Observation) -> bool:
        """Determines if the overarching Goal has been met based on current state."""
        raise NotImplementedError

class StateEvaluator(ABC):
    @abstractmethod
    async def evaluate(self, session: AgentSession, observation: Observation) -> EvaluationResult:
        """Analyzes the observation and decides whether to CONTINUE, RETRY, REPLAN, or TERMINATE."""
        raise NotImplementedError

class Replanner(ABC):
    @abstractmethod
    async def replan(self, session: AgentSession) -> PlanningResult:
        """Generates a revised execution strategy after failures or unexpected observations."""
        raise NotImplementedError

class TerminationStrategy(ABC):
    @abstractmethod
    def should_terminate(self, session: AgentSession) -> bool:
        """Checks if the agent loop should forcibly exit (e.g., timeout, max retries, cancellation)."""
        raise NotImplementedError

class Agent(ABC):
    @abstractmethod
    async def run(self, prompt: str) -> AgentSession:
        """The primary entrypoint that runs the Observe-Evaluate-Plan-Execute cycle."""
        raise NotImplementedError
