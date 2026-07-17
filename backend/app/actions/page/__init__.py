"""
Page actions.

Provides reusable page-level browser actions.
"""

from .evaluate import EvaluateAction
from .pdf import PdfAction
from .screenshot import ScreenshotAction
from .scroll import ScrollAction
from .scroll_into_view import ScrollIntoViewAction
from .scroll_to import ScrollToAction

__all__ = [
    "ScrollAction",
    "ScrollToAction",
    "ScrollIntoViewAction",
    "ScreenshotAction",
    "EvaluateAction",
    "PdfAction",
]