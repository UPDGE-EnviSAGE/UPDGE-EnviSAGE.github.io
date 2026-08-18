#!/usr/bin/env python3
"""Summarize and safely update faculty publication review decisions."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW_CSV = ROOT / "data-maintenance" / "faculty-publications-review.csv"
EXCEPTIONS_CSV = ROOT / "data-maintenance" / "faculty-publications-exceptions.csv"
MANUAL_DECISIONS = {"approve", "hold", "needs-fix"}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def decision(row: dict[str, str]) -> str:
    return (row.get("publication_decision") or row.get("reviewDecision") or "").strip() or "pending-review"


def publication_id(row: dict[str, str]) -> str:
    return (row.get("publication_id") or row.get("publicationId") or "").strip()


def is_clean(row: dict[str, str], exception_ids: set[str]) -> bool:
    return (
        publication_id(row) not in exception_ids
        and (row.get("duplicate_status") or "").strip() in {"", "none"}
        and (row.get("review_notes") or "").strip() == "clean-for-review"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--approve-clean", action="store_true", help="Approve only clean, non-exception records.")
    parser.add_argument("--write", action="store_true", help="Write approval changes. Defaults to dry-run.")
    args = parser.parse_args()

    rows = read_rows(REVIEW_CSV)
    exceptions = read_rows(EXCEPTIONS_CSV) if EXCEPTIONS_CSV.exists() else []
    exception_ids = {publication_id(row) for row in exceptions if publication_id(row)}

    decisions = Counter(decision(row) for row in rows)
    clean_rows = [row for row in rows if is_clean(row, exception_ids)]
    would_approve = [
        row
        for row in clean_rows
        if decision(row) not in MANUAL_DECISIONS and decision(row) != "approve"
    ]
    preserved = [
        row
        for row in rows
        if decision(row) in MANUAL_DECISIONS or publication_id(row) in exception_ids
    ]
    held = [row for row in rows if decision(row) == "hold" or publication_id(row) in exception_ids]

    print(f"review_rows={len(rows)}")
    print(f"review_decisions={dict(decisions)}")
    print(f"clean_for_review={len(clean_rows)}")
    print(f"exceptions={len(exception_ids)}")

    if args.approve_clean:
        print(f"would_approve={len(would_approve)}")
        print(f"would_leave_pending={len(rows) - len(would_approve) - len(preserved)}")
        print(f"would_hold_or_preserve={len(held)}")
        if not args.write:
            print("write=dry-run")
            return 0
        for row in would_approve:
            row["publication_decision"] = "approve"
        write_rows(REVIEW_CSV, rows)
        print("write=complete")
    else:
        print("write=dry-run")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
