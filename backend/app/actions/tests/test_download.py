"""
Tests for DownloadAction.
"""

import asyncio
from pathlib import Path

from app.actions.file.download import DownloadAction


class DummyPage:

    async def expect_download(self) -> Path:

        path = Path("downloads/report.pdf")

        print(f"Downloaded: {path}")

        return path


async def run_test():

    print("\n==============================")
    print(" Download Action Test ")
    print("==============================\n")

    page = DummyPage()

    action = DownloadAction()

    path = await action.execute(page)

    print(path)

    print(f"✓ {action.name}")

    print("\n✅ Download Action Test Passed!")


if __name__ == "__main__":
    asyncio.run(run_test())
