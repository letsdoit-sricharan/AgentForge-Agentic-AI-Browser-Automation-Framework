"""
Tests for DragAction.
"""

import asyncio

from app.actions.mouse.drag import DragAction


class DummyPage:

    async def drag(
        self,
        start_x: float,
        start_y: float,
        end_x: float,
        end_y: float,
    ):
        print(
            f"Dragging from "
            f"({start_x}, {start_y}) "
            f"to ({end_x}, {end_y})"
        )


async def run_test():

    print("\n==============================")
    print(" Drag Action Test ")
    print("==============================\n")

    page = DummyPage()

    action = DragAction(
        start_x=100,
        start_y=200,
        end_x=450,
        end_y=300,
    )

    await action.execute(page)

    print(f"✓ {action.name}")

    print("\n✅ Drag Action Test Passed!")


if __name__ == "__main__":
    asyncio.run(run_test())
