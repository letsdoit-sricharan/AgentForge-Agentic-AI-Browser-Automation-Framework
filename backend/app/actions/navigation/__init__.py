"""
Navigation actions.

Provides reusable actions for browser navigation.
"""

from .back import BackAction
from .forward import ForwardAction
from .navigate import NavigateAction
from .refresh import RefreshAction
from .wait import WaitAction

__all__ = [
    "BackAction",
    "ForwardAction",
    "NavigateAction",
    "RefreshAction",
    "WaitAction",
]