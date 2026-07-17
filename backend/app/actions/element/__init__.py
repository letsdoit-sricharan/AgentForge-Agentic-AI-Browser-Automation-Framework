"""
Element actions.

Provides reusable actions for interacting with
browser elements.
"""

from .blur import BlurAction
from .check import CheckAction
from .clear import ClearAction
from .click import ClickAction
from .double_click import DoubleClickAction
from .fill import FillAction
from .focus import FocusAction
from .hover import HoverAction
from .right_click import RightClickAction
from .select_option import SelectOptionAction
from .uncheck import UncheckAction

__all__ = [
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
]