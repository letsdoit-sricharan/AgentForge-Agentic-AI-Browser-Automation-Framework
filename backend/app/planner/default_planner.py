from typing import Optional

from app.planner.models import Goal, Plan, PlanningResult
from app.planner.interfaces import Planner, IntentRecognizer, ParameterExtractor, TaskPlanner
from app.planner.exceptions import PlannerError

class DefaultPlanner(Planner):
    """
    Orchestrates the IntentRecognizer, ParameterExtractor, and TaskPlanner
    to generate an ExecutionRequest plan from a natural language prompt.
    """
    def __init__(
        self, 
        intent_recognizer: IntentRecognizer, 
        parameter_extractor: ParameterExtractor,
        task_planner: TaskPlanner
    ):
        self.intent_recognizer = intent_recognizer
        self.parameter_extractor = parameter_extractor
        self.task_planner = task_planner

    async def generate_plan(self, prompt: str) -> PlanningResult:
        try:
            # 1. Recognize Intent
            intent = await self.intent_recognizer.recognize(prompt)
            
            # 2. Extract Entities
            entities = await self.parameter_extractor.extract(prompt, intent)
            
            # 3. Formulate Goal
            goal = Goal(original_prompt=prompt, intent=intent, entities=entities)
            
            # 4. Generate Execution Request(s)
            execution_request = await self.task_planner.plan_task(goal)
            
            # 5. Build Result
            plan = Plan(goal=goal, execution_requests=[execution_request])
            return PlanningResult(plan=plan, is_successful=True)
            
        except PlannerError as e:
            return PlanningResult(plan=None, is_successful=False, error_message=str(e))
        except Exception as e:
            return PlanningResult(plan=None, is_successful=False, error_message=f"Unexpected error: {str(e)}")
