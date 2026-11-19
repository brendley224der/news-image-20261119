#!/usr/bin/env python3
"""Write the finished front page to the grader's output directory.

Standard library only, no network. The PNG is fixed at build time, so every
run writes exactly the same bytes.
"""
import os
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"


def main():
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / "entry.png").write_bytes(SOURCE.read_bytes())


if __name__ == "__main__":
    main()
