"""
Metrics collector for AgentForge.
Tracks timing, success/failure counts, and general execution statistics.
"""

import time
from functools import wraps
from typing import Callable, Any
from app.core.logger import contextual_logger


class MetricsCollector:
    """
    In-memory metrics collector.
    In a production system, this could export to Datadog, Prometheus, etc.
    """
    def __init__(self):
        self.counters = {}
        self.timers = {}
        self.histograms = {}

    def increment(self, name: str, value: int = 1, tags: dict = None):
        key = self._make_key(name, tags)
        self.counters[key] = self.counters.get(key, 0) + value
        contextual_logger().debug(f"Metrics: Increment {name} by {value} (Tags: {tags})")

    def timer(self, name: str, duration_sec: float, tags: dict = None):
        key = self._make_key(name, tags)
        if key not in self.timers:
            self.timers[key] = []
        self.timers[key].append(duration_sec)
        contextual_logger().debug(f"Metrics: Timer {name} took {duration_sec:.4f}s (Tags: {tags})")

    def _make_key(self, name: str, tags: dict) -> str:
        if not tags:
            return name
        tag_str = ",".join(f"{k}={v}" for k, v in sorted(tags.items()))
        return f"{name}[{tag_str}]"


# Global singleton
metrics = MetricsCollector()


def track_time(metric_name: str, tags: dict = None):
    """
    Decorator to track the execution time of a function/method.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                return await func(*args, **kwargs)
            finally:
                duration = time.perf_counter() - start
                metrics.timer(metric_name, duration, tags)
                
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                return func(*args, **kwargs)
            finally:
                duration = time.perf_counter() - start
                metrics.timer(metric_name, duration, tags)

        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator
