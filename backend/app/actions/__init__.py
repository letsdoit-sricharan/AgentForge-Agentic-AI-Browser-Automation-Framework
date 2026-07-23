"""
AgentForge Action Library.

Provides reusable browser-independent actions
used by plugins and the Agent Runtime.
"""

# Navigation
# Element
from .element import (
    BlurAction,
    CheckAction,
    ClearAction,
    ClickAction,
    DoubleClickAction,
    FillAction,
    FocusAction,
    HoverAction,
    RightClickAction,
    SelectOptionAction,
    UncheckAction,
)

# File
from .file import (
    DownloadAction,
    UploadAction,
)

# Keyboard
from .keyboard import (
    HotkeyAction,
    PressKeyAction,
    ShortcutAction,
    TypeTextAction,
)

# Locator
from .locator import (
    FindAction,
    WaitForElementAction,
    WaitUntilHiddenAction,
    validate_selector,
)

# Mouse
from .mouse import (
    DragAction,
    DragAndDropAction,
    MouseWheelAction,
    MoveMouseAction,
)
from .navigation import (
    BackAction,
    ForwardAction,
    NavigateAction,
    RefreshAction,
    WaitAction,
)

# Page
from .page import (
    EvaluateAction,
    PdfAction,
    ScreenshotAction,
    ScrollAction,
    ScrollIntoViewAction,
    ScrollToAction,
)

__all__ = [
    # Navigation
    "BackAction",
    "ForwardAction",
    "NavigateAction",
    "RefreshAction",
    "WaitAction",

    # Element
    "BlurAction",
    "CheckAction",
    "ClearAction",
    "ClickAction",
    "DoubleClickAction",
    "FillAction",
    "FocusAction",
    "HoverAction",
    "RightClickAction",
    "SelectOptionAction",
    "UncheckAction",

    # Locator
    "FindAction",
    "WaitForElementAction",
    "WaitUntilHiddenAction",
    "validate_selector",

    # Keyboard
    "HotkeyAction",
    "PressKeyAction",
    "ShortcutAction",
    "TypeTextAction",

    # Mouse
    "MoveMouseAction",
    "DragAction",
    "DragAndDropAction",
    "MouseWheelAction",

    # Page
    "EvaluateAction",
    "PdfAction",
    "ScreenshotAction",
    "ScrollAction",
    "ScrollIntoViewAction",
    "ScrollToAction",

    # File
    "UploadAction",
    "DownloadAction",
]
