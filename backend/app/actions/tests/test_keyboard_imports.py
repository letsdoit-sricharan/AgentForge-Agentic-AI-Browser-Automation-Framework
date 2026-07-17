"""
Tests for the Keyboard package public API.
"""

from app.actions.keyboard import (
    HotkeyAction,
    PressKeyAction,
    ShortcutAction,
    TypeTextAction,
)


def test_keyboard_imports():

    print("\n==============================")
    print(" Keyboard Package Import Test ")
    print("==============================\n")

    exports = [
        PressKeyAction,
        TypeTextAction,
        HotkeyAction,
        ShortcutAction,
    ]

    for export in exports:
        print(f"✓ {export.__name__}")

    print("\n✅ Keyboard Package Import Test Passed!")


if __name__ == "__main__":
    test_keyboard_imports()