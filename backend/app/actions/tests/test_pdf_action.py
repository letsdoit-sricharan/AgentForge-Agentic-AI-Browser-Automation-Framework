"""
Tests for PdfAction.
"""

import asyncio
from pathlib import Path

from app.actions.page.pdf import PdfAction


class DummyPage:

    async def pdf(
        self,
        path: Path,
    ) -> Path:

        print(f"Generating PDF at {path}")

        return path


async def run_test():

    print("\n==============================")
    print(" PDF Action Test ")
    print("==============================\n")

    page = DummyPage()

    action = PdfAction(
        path=Path("artifacts/report.pdf"),
    )

    pdf_path = await action.execute(page)

    print(pdf_path)

    print(f"✓ {action.name}")

    print("\n✅ PDF Action Test Passed!")


if __name__ == "__main__":
    asyncio.run(run_test())