#!/usr/bin/env python3
"""Apply reviewed faculty publication visibility decisions to content files."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW_CSV = ROOT / "data-maintenance" / "faculty-publications-review.csv"
PUBLICATION_DIR = ROOT / "src" / "content" / "publications"


def update_visibility(path: Path, visibility: str) -> bool:
    text = path.read_text(encoding="utf-8")
    updated = re.sub(r"^visibility:\s+\w+\s*$", f"visibility: {visibility}", text, count=1, flags=re.MULTILINE)
    if updated == text:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="Write approved visibility decisions.")
    args = parser.parse_args()

    with REVIEW_CSV.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    approved = [
        row
        for row in rows
        if (row.get("reviewDecision") or "").strip() == "approve-public"
        and (row.get("visibilityAfterPublish") or "").strip() == "public"
    ]
    print(f"review_rows={len(rows)}")
    print(f"approved_public={len(approved)}")
    if not args.write:
        print("write=dry-run")
        return 0

    changed = 0
    for row in approved:
        path = PUBLICATION_DIR / f"{row['publicationId']}.md"
        if path.exists() and update_visibility(path, "public"):
            changed += 1
    print(f"changed_files={changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
