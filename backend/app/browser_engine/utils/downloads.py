"""
Purpose:
    Provide utilities for managing and tracking downloaded files.

Responsibilities:
    - Helper functions to verify, move, and rename downloaded files.
    - Check file sizes and mime-types.

Must NOT do:
    - Store state about active download sessions (this belongs in managers).
"""

from __future__ import annotations
import shutil
from pathlib import Path


def move_downloaded_file(source_path: str, target_dir: str, filename: str) -> str:
    """
    Move a downloaded file from its temporary source path to a structured target directory.

    Args:
        source_path: The absolute path of the downloaded file.
        target_dir: The directory where the file should be moved.
        filename: The desired name for the file.

    Returns:
        The new absolute path of the moved file.
    """
    source = Path(source_path)
    if not source.exists():
        raise FileNotFoundError(f"Source file does not exist: {source_path}")

    target_path = Path(target_dir) / filename
    target_path.parent.mkdir(parents=True, exist_ok=True)

    shutil.move(str(source), str(target_path))
    return str(target_path.resolve())
