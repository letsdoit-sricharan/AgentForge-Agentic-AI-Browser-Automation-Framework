from dataclasses import dataclass, field
from typing import Any, List, Optional
from app.runtime.execution.execution_request import ExecutionRequest

@dataclass
class Intent:
    name: str
    confidence: float = 1.0

@dataclass
class Entity:
    name: str
    value: Any
    type_hint: Optional[str] = None

@dataclass
class Goal:
    original_prompt: str
    intent: Intent
    entities: List[Entity] = field(default_factory=list)

@dataclass
class Plan:
    goal: Goal
    execution_requests: List[ExecutionRequest] = field(default_factory=list)

@dataclass
class PlanningResult:
    plan: Optional[Plan]
    is_successful: bool
    error_message: Optional[str] = None
