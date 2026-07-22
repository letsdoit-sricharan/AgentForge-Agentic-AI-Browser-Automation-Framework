from abc import ABC, abstractmethod
from typing import List

from app.planner.models import Intent, Entity, Goal, PlanningResult
from app.runtime.execution.execution_request import ExecutionRequest

class IntentRecognizer(ABC):
    @abstractmethod
    async def recognize(self, prompt: str) -> Intent:
        """Determines the primary intent of the user's natural language prompt."""
        raise NotImplementedError

class ParameterExtractor(ABC):
    @abstractmethod
    async def extract(self, prompt: str, intent: Intent) -> List[Entity]:
        """Extracts required variables/entities based on the recognized intent."""
        raise NotImplementedError

class TaskPlanner(ABC):
    @abstractmethod
    async def plan_task(self, goal: Goal) -> ExecutionRequest:
        """Converts a formulated Goal into a single ExecutionRequest."""
        raise NotImplementedError

class WorkflowPlanner(ABC):
    @abstractmethod
    async def plan_workflow(self, goal: Goal) -> List[ExecutionRequest]:
        """Converts a formulated Goal into a sequence of ExecutionRequests."""
        raise NotImplementedError

class Planner(ABC):
    @abstractmethod
    async def generate_plan(self, prompt: str) -> PlanningResult:
        """End-to-end translation from natural language prompt to a PlanningResult."""
        raise NotImplementedError
