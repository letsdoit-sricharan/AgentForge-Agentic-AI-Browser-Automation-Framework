from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional

from app.planner.models import Goal, Plan

class EvaluationAction(Enum):
    CONTINUE = auto()
    RETRY = auto()
    REPLAN = auto()
    TERMINATE = auto()

@dataclass
class Observation:
    """Represents the environmental feedback after executing a task."""
    is_success: bool
    message: str
    data: Dict[str, Any] = field(default_factory=dict)

@dataclass
class EvaluationResult:
    """Represents the evaluator's decision on the next loop cycle."""
    action: EvaluationAction
    reasoning: str

@dataclass
class AgentSession:
    """
    Mutable state object tracking the lifecycle of a user request through the agent loop.
    """
    goal: Optional[Goal] = None
    current_plan: Optional[Plan] = None
    observation_history: List[Observation] = field(default_factory=list)
    status: str = "INITIALIZED"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def record_observation(self, observation: Observation):
        self.observation_history.append(observation)
