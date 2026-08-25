#!/usr/bin/env python3
"""Apply reviewed faculty publication visibility decisions to content files."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW_CSV = ROOT / "data-maintenance" / "faculty-publications-review.csv"
MAINTENANCE_CSV = ROOT / "data-maintenance" / "faculty-publications.csv"
PUBLICATION_DIR = ROOT / "src" / "content" / "publications"
PUBLIC_BODY = (
    "\nThis publication record is part of the EnviSAGE public scholarly catalog.\n"
)


def update_visibility(path: Path, visibility: str) -> bool:
    text = path.read_text(encoding="utf-8")
    updated = re.sub(r"^visibility:\s+\w+\s*$", f"visibility: {visibility}", text, count=1, flags=re.MULTILINE)
    if visibility == "public":
        frontmatter_match = re.match(r"^(---\n.*?\n---\n)(.*)$", updated, flags=re.DOTALL)
        if frontmatter_match:
            updated = f"{frontmatter_match.group(1)}{PUBLIC_BODY}"
    if updated == text:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def update_maintenance_visibility(publication_ids: set[str]) -> int:
    if not MAINTENANCE_CSV.exists():
        return 0
    with MAINTENANCE_CSV.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fields = reader.fieldnames
    if not rows or not fields or "visibility" not in fields:
        return 0

    changed = 0
    for row in rows:
        if row.get("publicationId") in publication_ids and row.get("visibility") != "public":
            row["visibility"] = "public"
            changed += 1

    if changed:
        with MAINTENANCE_CSV.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="Write approved visibility decisions.")
    args = parser.parse_args()

    with REVIEW_CSV.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    approved = []
    for row in rows:
        decision = (row.get("publication_decision") or row.get("reviewDecision") or "").strip()
        visibility_after_publish = (row.get("visibilityAfterPublish") or "").strip()
        if decision == "approve" or (
            decision == "approve-public" and visibility_after_publish == "public"
        ):
            approved.append(row)
    print(f"review_rows={len(rows)}")
    print(f"approved_public={len(approved)}")
    if not args.write:
        print("write=dry-run")
        return 0

    changed = 0
    approved_ids: set[str] = set()
    for row in approved:
        publication_id = row.get("publication_id") or row.get("publicationId")
        if not publication_id:
            continue
        approved_ids.add(publication_id)
        path = PUBLICATION_DIR / f"{publication_id}.md"
        if path.exists() and update_visibility(path, "public"):
            changed += 1
    maintenance_changed = update_maintenance_visibility(approved_ids)
    print(f"changed_files={changed}")
    print(f"changed_maintenance_rows={maintenance_changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
