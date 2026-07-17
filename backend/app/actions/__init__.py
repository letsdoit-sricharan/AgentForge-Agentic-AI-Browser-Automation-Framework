"""
AgentForge Action Library.

Provides reusable browser-independent actions
used by plugins and the Agent Runtime.
"""

# Navigation
from .navigation import (
    BackAction,
    ForwardAction,
    NavigateAction,
    RefreshAction,
    WaitAction,
)

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

# Locator
from .locator import (
    FindAction,
    WaitForElementAction,
    WaitUntilHiddenAction,
    validate_selector,
)

# Keyboard
from .keyboard import (
    HotkeyAction,
    PressKeyAction,
    ShortcutAction,
    TypeTextAction,
)

# Mouse
from .mouse import (
    MoveMouseAction,
    DragAction,
    DragAndDropAction,
    MouseWheelAction,
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

# File
from .file import (
    UploadAction,
    DownloadAction,
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