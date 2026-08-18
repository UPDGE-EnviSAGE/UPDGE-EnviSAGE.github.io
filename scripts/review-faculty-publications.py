#!/usr/bin/env python3
"""Summarize faculty publication review decisions before publication sync."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW_CSV = ROOT / "data-maintenance" / "faculty-publications-review.csv"


def main() -> int:
    with REVIEW_CSV.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    decisions = Counter((row.get("reviewDecision") or "").strip() or "(blank)" for row in rows)
    visibility = Counter((row.get("visibilityAfterPublish") or "").strip() or "(blank)" for row in rows)
    public_ready = sum(
        1
        for row in rows
        if (row.get("reviewDecision") or "").strip() == "approve-public"
        and (row.get("visibilityAfterPublish") or "").strip() == "public"
    )
    print(f"review_rows={len(rows)}")
    print(f"review_decisions={dict(decisions)}")
    print(f"visibility_after_publish={dict(visibility)}")
    print(f"public_ready={public_ready}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
