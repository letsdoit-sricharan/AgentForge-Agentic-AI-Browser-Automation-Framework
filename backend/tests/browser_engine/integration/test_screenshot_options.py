from pathlib import Path

from pydantic import ValidationError

from app.browser_engine.models.screenshot_options import ScreenshotOptions


print("=" * 60)
print("ScreenshotOptions Validation Test")
print("=" * 60)

try:

    ScreenshotOptions(
        path=Path("image.png"),
        quality=90,
    )

    print("❌ Validation failed")

except ValidationError:

    print("✓ PNG correctly rejected quality option")