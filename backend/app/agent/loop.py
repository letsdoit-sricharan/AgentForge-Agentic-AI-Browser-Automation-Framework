import logging

from app.agent.exceptions import GoalFailedError, TerminatedError
from app.agent.interfaces import (
    Agent,
    Executor,
    GoalMonitor,
    ObservationCollector,
    Replanner,
    StateEvaluator,
    TerminationStrategy,
)
from app.agent.models import AgentSession, EvaluationAction, Observation
from app.planner.interfaces import Planner

logger = logging.getLogger(__name__)

class DefaultAgent(Agent):
    """
    Implements the core Agent Runtime Loop:
    Observe -> Evaluate -> Plan -> Execute.
    """

    def __init__(
        self,
        planner: Planner,
        executor: Executor,
        observation_collector: ObservationCollector,
        goal_monitor: GoalMonitor,
        state_evaluator: StateEvaluator,
        replanner: Replanner,
        termination_strategy: TerminationStrategy
    ):
        self.planner = planner
        self.executor = executor
        self.observation_collector = observation_collector
        self.goal_monitor = goal_monitor
        self.state_evaluator = state_evaluator
        self.replanner = replanner
        self.termination_strategy = termination_strategy

    async def run(self, prompt: str) -> AgentSession:
        session = AgentSession()
        session.status = "PLANNING"

        # 1. Initial Plan
        planning_result = await self.planner.generate_plan(prompt)
        if not planning_result.is_successful or not planning_result.plan:
            session.status = "FAILED_INITIAL_PLANNING"
            return session

        session.goal = planning_result.plan.goal
        session.current_plan = planning_result.plan
        session.status = "EXECUTING"

        # 2. Main Loop
        while not self.termination_strategy.should_terminate(session):
            if not session.current_plan.execution_requests:
                # If out of steps, verify goal
                achieved = await self.goal_monitor.is_goal_achieved(session, Observation(True, "Plan exhausted"))
                session.status = "COMPLETED" if achieved else "FAILED"
                break

            # Pop next step
            request = session.current_plan.execution_requests.pop(0)

            # Execute
            try:
                raw_result = await self.executor.execute(request)
            except Exception as e:
                raw_result = e

            # Observe
            observation = await self.observation_collector.collect(raw_result)
            session.record_observation(observation)

            # Monitor
            if await self.goal_monitor.is_goal_achieved(session, observation):
                session.status = "COMPLETED"
                break

            # Evaluate
            evaluation = await self.state_evaluator.evaluate(session, observation)

            if evaluation.action == EvaluationAction.CONTINUE:
                continue

            elif evaluation.action == EvaluationAction.RETRY:
                # Re-insert the failed task at the front
                session.current_plan.execution_requests.insert(0, request)
                continue

            elif evaluation.action == EvaluationAction.REPLAN:
                session.status = "REPLANNING"
                replanning_result = await self.replanner.replan(session)
                if not replanning_result.is_successful or not replanning_result.plan:
                    session.status = "FAILED_REPLANNING"
                    raise GoalFailedError(f"Replanning failed: {replanning_result.error_message}")

                session.current_plan = replanning_result.plan
                session.status = "EXECUTING"
                continue

            elif evaluation.action == EvaluationAction.TERMINATE:
                session.status = "TERMINATED"
                raise TerminatedError(f"Evaluator terminated execution: {evaluation.reasoning}")

        if self.termination_strategy.should_terminate(session) and session.status == "EXECUTING":
             session.status = "TERMINATED_STRATEGY"

        return session
