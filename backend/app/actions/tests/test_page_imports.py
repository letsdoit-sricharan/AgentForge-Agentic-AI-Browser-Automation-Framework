"""
Tests for the Page package public API.
"""

from app.actions.page import (
    EvaluateAction,
    PdfAction,
    ScreenshotAction,
    ScrollAction,
    ScrollIntoViewAction,
    ScrollToAction,
)


def test_page_imports():

    print("\n==============================")
    print(" Page Package Import Test ")
    print("==============================\n")

    exports = [
        ScrollAction,
        ScrollToAction,
        ScrollIntoViewAction,
        ScreenshotAction,
        EvaluateAction,
        PdfAction,
    ]

    for export in exports:
        print(f"✓ {export.__name__}")

    print("\n✅ Page Package Import Test Passed!")


if __name__ == "__main__":
    test_page_imports()
