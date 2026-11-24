#!/usr/bin/env python3
"""Write the bounty entry to ``entry.txt``.

One line, 1-200 characters, UTF-8, no trailing newline. Standard library
only, no network. The output directory comes from the
``MAKEFUN_OUTPUT_DIR`` environment variable (default ``/output``); no path
here depends on the current working directory.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

ENTRY = (
    "My plan was redacted as classified before I could read it, "
    "so I spent the deadline applying for clearance to see my own homework."
)


def output_dir() -> Path:
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if raw:
        return Path(raw)
    return Path("/output")


def validate(text: str) -> None:
    if not text or not text.strip():
        raise ValueError("entry must not be empty or only whitespace")
    if len(text) > 200:
        raise ValueError(f"entry is {len(text)} characters, over the 200 limit")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")


def main() -> int:
    validate(ENTRY)
    out_dir = output_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    data = ENTRY.encode("utf-8")
    target.write_bytes(data)
    os.chmod(target, 0o644)
    # Read back and verify: exact bytes, valid UTF-8, still in limits.
    back = target.read_bytes()
    if back != data:
        raise ValueError("read-back mismatch: entry.txt differs from entry")
    text = back.decode("utf-8")
    validate(text)
    print(f"Wrote {target} ({len(text)} characters)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
