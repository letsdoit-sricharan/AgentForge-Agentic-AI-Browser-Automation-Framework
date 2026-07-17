"""
Tests for TypeTextAction.
"""

import asyncio

from app.actions.keyboard.type_text import TypeTextAction


class DummyPage:

    async def type_text(
        self,
        text: str,
        delay: float | None = None,
    ):
        print(f"Typing: {text}")
        print(f"Delay : {delay}")


async def run_test():

    print("\n==============================")
    print(" Type Text Action Test ")
    print("==============================\n")

    page = DummyPage()

    action = TypeTextAction(
        text="Hello AgentForge",
        delay=0.05,
    )

    await action.execute(page)

    print(f"✓ {action.name}")

    print("\n✅ Type Text Action Test Passed!")


if __name__ == "__main__":
    asyncio.run(run_test())