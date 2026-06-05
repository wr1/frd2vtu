#!/usr/bin/env python3
"""Regenerate the README FRD coverage table from test/frds."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "test"))

import frd2vtu  # noqa: E402
from frd_cases import FRD_FILES, FRDS_DIR, SKIPPED_FRDS  # noqa: E402

MARKERS = ("<!-- coverage-table:start -->", "<!-- coverage-table:end -->")


def conversion_status(frd_name: str) -> str:
    if frd_name in SKIPPED_FRDS:
        return "—"
    try:
        grid = frd2vtu.frdbin2vtu(str(FRDS_DIR / frd_name))
    except Exception:
        return "❌"
    return "✅" if grid is not None else "❌"


def build_table() -> str:
    n = len(FRD_FILES)
    lines = [
        f"<summary>{n} files</summary>",
        "",
        "| File | Status |",
        "|------|--------|",
    ]
    for name in FRD_FILES:
        stem = name.removesuffix(".frd")
        lines.append(f"| {stem} | {conversion_status(name)} |")
    return "\n".join(lines)


def main() -> None:
    readme = ROOT / "README.md"
    text = readme.read_text()
    start, end = MARKERS
    pattern = re.compile(
        re.escape(start) + r".*?" + re.escape(end),
        re.DOTALL,
    )
    if not pattern.search(text):
        raise SystemExit(f"README missing {start} / {end} markers")
    replacement = f"{start}\n\n<details>\n{build_table()}\n</details>\n\n{end}"
    readme.write_text(pattern.sub(replacement, text))
    print(f"Updated {readme} ({len(FRD_FILES)} files)")


if __name__ == "__main__":
    main()
