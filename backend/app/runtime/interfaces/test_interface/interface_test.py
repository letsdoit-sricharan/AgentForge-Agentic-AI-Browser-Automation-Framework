"""
Tests for runtime interface contracts.
"""

from app.runtime.interfaces import (
    EventBus,
    ExecutionEngine,
    Executor,
    Strategy,
)


# ---------------------------------------------------------------------
# Dummy Implementations
# ---------------------------------------------------------------------


class DummyExecutor(Executor):
    async def execute(self, *args, **kwargs):
        return "executor-ok"


class DummyStrategy(Strategy):
    async def apply(self, *args, **kwargs):
        return "strategy-ok"


class DummyExecutionEngine(ExecutionEngine):
    async def start(self, *args, **kwargs):
        return "started"

    async def pause(self, execution_id: str):
        return None

    async def resume(self, execution_id: str):
        return None

    async def cancel(self, execution_id: str):
        return None


class DummyEventBus(EventBus):
    def subscribe(self, event_type: str, handler):
        pass

    def unsubscribe(self, event_type: str, handler):
        pass

    async def publish(self, event):
        return None


# ---------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------


def test_executor_instantiation():
    executor = DummyExecutor()

    assert isinstance(executor, Executor)


def test_strategy_instantiation():
    strategy = DummyStrategy()

    assert isinstance(strategy, Strategy)


def test_execution_engine_instantiation():
    engine = DummyExecutionEngine()

    assert isinstance(engine, ExecutionEngine)


def test_event_bus_instantiation():
    bus = DummyEventBus()

    assert isinstance(bus, EventBus)