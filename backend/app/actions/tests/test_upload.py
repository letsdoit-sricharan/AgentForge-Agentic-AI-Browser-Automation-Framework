"""
Tests for UploadAction.
"""

import asyncio
from pathlib import Path

from app.actions.file.upload import UploadAction


class DummyPage:

    async def upload_file(
        self,
        selector: str,
        file_path: Path,
    ):

        print(
            f"Uploading '{file_path}' "
            f"to '{selector}'"
        )


async def run_test():

    print("\n==============================")
    print(" Upload Action Test ")
    print("==============================\n")

    page = DummyPage()

    action = UploadAction(
        selector="#resume",
        file_path=Path("resume.pdf"),
    )

    await action.execute(page)

    print(f"✓ {action.name}")

    print("\n✅ Upload Action Test Passed!")


if __name__ == "__main__":
    asyncio.run(run_test())
