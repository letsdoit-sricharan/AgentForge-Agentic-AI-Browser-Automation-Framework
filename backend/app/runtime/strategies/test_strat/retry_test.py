"""
Tests for RetryStrategy.
"""

from app.runtime.strategies.retry_strategy import RetryStrategy


def test_retry_strategy():
    strategy = RetryStrategy(
        max_retries=3,
        initial_delay=1.0,
        backoff_factor=2.0,
        max_delay=10.0,
    )

    print("\nCreating RetryStrategy...")

    assert strategy.current_attempt == 0
    assert strategy.retries_remaining == 3
    assert strategy.should_retry()

    print("Recording first retry...")

    strategy.record_retry()

    assert strategy.current_attempt == 1
    assert strategy.retries_remaining == 2
    assert strategy.next_delay() == 2.0

    print("Recording second retry...")

    strategy.record_retry()

    assert strategy.current_attempt == 2
    assert strategy.retries_remaining == 1
    assert strategy.next_delay() == 4.0

    print("Recording third retry...")

    strategy.record_retry()

    assert strategy.current_attempt == 3
    assert strategy.retries_remaining == 0
    assert not strategy.should_retry()

    print("Resetting strategy...")

    strategy.reset()

    assert strategy.current_attempt == 0
    assert strategy.retries_remaining == 3

    print("✅ RetryStrategy test passed!")


if __name__ == "__main__":
    test_retry_strategy()