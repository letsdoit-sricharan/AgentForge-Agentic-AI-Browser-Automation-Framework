"""
Keyboard actions.

Provides reusable keyboard-related browser actions.
"""

from .hotkey import HotkeyAction
from .press_key import PressKeyAction
from .shortcut import ShortcutAction
from .type_text import TypeTextAction

__all__ = [
    "PressKeyAction",
    "TypeTextAction",
    "HotkeyAction",
    "ShortcutAction",
]
