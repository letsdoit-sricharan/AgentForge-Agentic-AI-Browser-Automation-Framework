"""
Tests the complete public API of the
Action Library.
"""

from app.actions import *


def test_action_library_imports():

    print("\n==============================")
    print(" Action Library Import Test ")
    print("==============================\n")

    exports = [
        # Navigation
        NavigateAction,
        BackAction,
        ForwardAction,
        RefreshAction,
        WaitAction,

        # Element
        ClickAction,
        DoubleClickAction,
        RightClickAction,
        HoverAction,
        FillAction,
        ClearAction,
        FocusAction,
        BlurAction,
        CheckAction,
        UncheckAction,
        SelectOptionAction,

        # Locator
        FindAction,
        WaitForElementAction,
        WaitUntilHiddenAction,

        # Keyboard
        PressKeyAction,
        TypeTextAction,
        HotkeyAction,
        ShortcutAction,

        # Mouse
        MoveMouseAction,
        DragAction,
        DragAndDropAction,
        MouseWheelAction,

        # Page
        ScrollAction,
        ScrollToAction,
        ScrollIntoViewAction,
        ScreenshotAction,
        EvaluateAction,
        PdfAction,

        # File
        UploadAction,
        DownloadAction,
    ]

    for action in exports:
        print(f"✓ {action.__name__}")

    print("\n🎉 Action Library Version 1.0 Complete!")


if __name__ == "__main__":
    test_action_library_imports()