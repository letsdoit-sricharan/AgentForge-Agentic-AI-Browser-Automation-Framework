"""
Tests for DragAndDropAction.
"""

import asyncio

from app.actions.mouse.drag_and_drop import DragAndDropAction


class DummyPage:

    async def drag_and_drop(
        self,
        source_selector: str,
        target_selector: str,
    ):
        print(
            f"Dragging '{source_selector}' "
            f"to '{target_selector}'"
        )


async def run_test():

    print("\n==============================")
    print(" Drag And Drop Action Test ")
    print("==============================\n")

    page = DummyPage()

    action = DragAndDropAction(
        source_selector="#task-1",
        target_selector="#done-column",
    )

    await action.execute(page)

    print(f"✓ {action.name}")

    print("\n✅ Drag And Drop Action Test Passed!")


if __name__ == "__main__":
    asyncio.run(run_test())