"""
Retry Flow Integration Test.

Verifies that RetryStrategy correctly tracks retries,
calculates delays, and stops after the retry limit.
"""

from app.runtime.strategies.retry_strategy import RetryStrategy


def test_retry_flow():

    print("\n==============================")
    print(" Retry Flow Test ")
    print("==============================\n")

    strategy = RetryStrategy(
        max_retries=3,
        initial_delay=1.0,
        backoff_factor=2.0,
    )

    while strategy.should_retry():

        print(f"Attempt : {strategy.current_attempt + 1}")

        delay = strategy.next_delay()

        print(f"Delay   : {delay} seconds")

        strategy.record_retry()

    print("\nRetry limit reached.")

    print(f"Current Attempts : {strategy.current_attempt}")
    print(f"Retries Remaining: {strategy.retries_remaining}")

    assert strategy.current_attempt == 3
    assert strategy.exhausted
    assert strategy.retries_remaining == 0

    # ----------------------------------------
    # Verify exception after exhaustion
    # ----------------------------------------

    print("\nVerifying retry exhaustion...")

    try:
        strategy.record_retry()

    except RuntimeError as error:

        print(error)

        print("\nException correctly raised.")

    else:

        raise AssertionError(
            "Expected RuntimeError was not raised."
        )

    # ----------------------------------------
    # Verify reset
    # ----------------------------------------

    strategy.reset()

    print("\nStrategy reset.")

    print(f"Current Attempts : {strategy.current_attempt}")

    assert strategy.current_attempt == 0
    assert strategy.should_retry()

    print("\n✅ Retry Flow Test Passed!")


if __name__ == "__main__":
    test_retry_flow()
