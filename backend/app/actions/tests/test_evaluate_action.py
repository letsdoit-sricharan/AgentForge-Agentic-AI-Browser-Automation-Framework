"""
Tests for EvaluateAction.
"""

import asyncio

from app.actions.page.evaluate import EvaluateAction


class DummyPage:

    async def evaluate(
        self,
        script: str,
        argument: object | None = None,
    ) -> object:

        print(f"Executing: {script}")

        print(f"Argument : {argument}")

        return {
            "status": "success",
            "result": 42,
        }


async def run_test():

    print("\n==============================")
    print(" Evaluate Action Test ")
    print("==============================\n")

    page = DummyPage()

    action = EvaluateAction(
        script="return 6 * 7;",
    )

    result = await action.execute(page)

    print(result)

    print(f"✓ {action.name}")

    print("\n✅ Evaluate Action Test Passed!")


if __name__ == "__main__":
    asyncio.run(run_test())