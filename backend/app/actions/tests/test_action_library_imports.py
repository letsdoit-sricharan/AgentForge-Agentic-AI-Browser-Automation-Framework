"""
Tests the complete public API of the Action Library.

Verifies that every expected class is importable from the top-level
``app.actions`` package, ensuring the public surface is stable.
"""

from app.actions import (  # noqa: F401
    BackAction,
    BlurAction,
    CheckAction,
    ClearAction,
    ClickAction,
    DoubleClickAction,
    DownloadAction,
    DragAction,
    DragAndDropAction,
    EvaluateAction,
    FillAction,
    FindAction,
    FocusAction,
    ForwardAction,
    HotkeyAction,
    HoverAction,
    MouseWheelAction,
    MoveMouseAction,
    NavigateAction,
    PdfAction,
    PressKeyAction,
    RefreshAction,
    RightClickAction,
    ScreenshotAction,
    ScrollAction,
    ScrollIntoViewAction,
    ScrollToAction,
    SelectOptionAction,
    ShortcutAction,
    TypeTextAction,
    UncheckAction,
    UploadAction,
    WaitAction,
    WaitForElementAction,
    WaitUntilHiddenAction,
)


def test_action_library_imports():
    """Verify all expected actions are importable from the top-level package."""
    expected = [
        # Navigation
        NavigateAction, BackAction, ForwardAction, RefreshAction, WaitAction,
        # Element
        ClickAction, DoubleClickAction, RightClickAction, HoverAction,
        FillAction, ClearAction, FocusAction, BlurAction, CheckAction,
        UncheckAction, SelectOptionAction,
        # Locator
        FindAction, WaitForElementAction, WaitUntilHiddenAction,
        # Keyboard
        PressKeyAction, TypeTextAction, HotkeyAction, ShortcutAction,
        # Mouse
        MoveMouseAction, DragAction, DragAndDropAction, MouseWheelAction,
        # Page
        ScrollAction, ScrollToAction, ScrollIntoViewAction,
        ScreenshotAction, EvaluateAction, PdfAction,
        # File
        UploadAction, DownloadAction,
    ]

    for action_cls in expected:
        assert callable(action_cls), (
            f"Expected {action_cls!r} to be callable/importable from app.actions"
        )
