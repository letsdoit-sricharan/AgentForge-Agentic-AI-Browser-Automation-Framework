"""
Tests for WaitStrategy.
"""

import asyncio
import time

from app.runtime.strategies.wait_strategy import WaitStrategy


async def test_wait_strategy():
    strategy = WaitStrategy(delay=0.5)

    print("\nCreating WaitStrategy...")

    assert strategy.delay == 0.5

    print("Waiting for 0.5 seconds...")

    start = time.perf_counter()

    await strategy.wait()

    elapsed = time.perf_counter() - start

    assert elapsed >= 0.5

    print(f"Elapsed: {elapsed:.2f} seconds")

    print("Changing delay...")

    strategy.set_delay(1.0)

    assert strategy.delay == 1.0

    print("Resetting strategy...")

    strategy.reset()

    assert strategy.delay == 1.0

    print("✅ WaitStrategy test passed!")


if __name__ == "__main__":
    asyncio.run(test_wait_strategy())
