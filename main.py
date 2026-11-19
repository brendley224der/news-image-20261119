"""News-image entry: copy the finished front page to the output directory.

Pure standard library. The grader runs this with no network; it writes the
same bytes on every run because it only copies entry.png.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
# Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output.
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
OUT.mkdir(parents=True, exist_ok=True)
shutil.copyfile(HERE / "entry.png", OUT / "entry.png")
