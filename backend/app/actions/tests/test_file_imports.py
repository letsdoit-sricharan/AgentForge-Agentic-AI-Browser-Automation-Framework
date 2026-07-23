"""
Tests for the File package public API.
"""

from app.actions.file import (
    DownloadAction,
    UploadAction,
)


def test_file_imports():

    print("\n==============================")
    print(" File Package Import Test ")
    print("==============================\n")

    exports = [
        UploadAction,
        DownloadAction,
    ]

    for export in exports:
        print(f"✓ {export.__name__}")

    print("\n✅ File Package Import Test Passed!")


if __name__ == "__main__":
    test_file_imports()
