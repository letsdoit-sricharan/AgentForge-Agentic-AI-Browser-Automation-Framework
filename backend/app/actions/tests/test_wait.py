"""
Tests for WaitAction.
"""

import asyncio

from app.actions.navigation.wait import WaitAction
from app.browser_engine.models.load_state import LoadState


class DummyPage:
    """
    Fake Browser Engine page.
    """

    async def wait_for_load_state(
        self,
        load_state,
        timeout=None,
    ):
        print(
            f"Waiting for {load_state.name} "
            f"(timeout={timeout})"
        )


async def run_test():

    print("\n==============================")
    print(" Wait Action Test ")
    print("==============================\n")

    page = DummyPage()

    action = WaitAction(
        load_state=LoadState.LOAD,
        timeout=10,
    )

    await action.execute(page)

    print(f"Action Name : {action.name}")
    print(f"Load State  : {action.load_state.name}")

    print("\n✅ Wait Action Test Passed!")


if __name__ == "__main__":
    asyncio.run(run_test())
