"""
Tests for the Mouse package public API.
"""

from app.actions.mouse import (
    MoveMouseAction,
    DragAction,
    DragAndDropAction,
    MouseWheelAction,
)


def test_mouse_imports():

    print("\n==============================")
    print(" Mouse Package Import Test ")
    print("==============================\n")

    exports = [
        MoveMouseAction,
        DragAction,
        DragAndDropAction,
        MouseWheelAction,
    ]

    for export in exports:
        print(f"✓ {export.__name__}")

    print("\n✅ Mouse Package Import Test Passed!")


if __name__ == "__main__":
    test_mouse_imports()