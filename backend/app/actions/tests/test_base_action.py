"""
Tests for BaseAction.
"""

import asyncio

from app.actions.base_action import BaseAction


class DummyPage:
    """Dummy page used for testing."""
    pass


class DummyAction(BaseAction):

    async def execute(self, page):

        print("Executing Dummy Action")

        return "SUCCESS"


async def run_test():

    print("\n==============================")
    print(" Base Action Test ")
    print("==============================\n")

    action = DummyAction()

    page = DummyPage()

    result = await action.execute(page)

    print(f"Action Name : {action.name}")
    print(f"Result      : {result}")

    assert action.name == "DummyAction"

    assert result == "SUCCESS"

    print("\n✅ Base Action Test Passed!")


if __name__ == "__main__":
    asyncio.run(run_test())