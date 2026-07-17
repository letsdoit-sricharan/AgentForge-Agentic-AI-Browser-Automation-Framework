"""
Tests for MouseWheelAction.
"""

import asyncio

from app.actions.mouse.wheel import MouseWheelAction


class DummyPage:

    async def mouse_wheel(
        self,
        delta_x: float,
        delta_y: float,
    ):
        print(
            f"Mouse wheel scrolled "
            f"(delta_x={delta_x}, delta_y={delta_y})"
        )


async def run_test():

    print("\n==============================")
    print(" Mouse Wheel Action Test ")
    print("==============================\n")

    page = DummyPage()

    action = MouseWheelAction(
        delta_x=0,
        delta_y=600,
    )

    await action.execute(page)

    print(f"✓ {action.name}")

    print("\n✅ Mouse Wheel Action Test Passed!")


if __name__ == "__main__":
    asyncio.run(run_test())