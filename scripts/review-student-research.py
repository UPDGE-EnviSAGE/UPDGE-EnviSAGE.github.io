#!/usr/bin/env python3
"""Generate and summarize the student research publication review CSV."""

from __future__ import annotations

import argparse
from pathlib import Path

from student_research_publication import (
    EXCEPTIONS_CSV,
    REVIEW_COLUMNS,
    REVIEW_CSV,
    exception_rows,
    generate_review_rows,
    print_json,
    summary_for_rows,
    validate_review_rows,
    write_csv,
)


EXCEPTION_COLUMNS = [
    "record_id",
    "year",
    "thesis_title",
    "association_basis",
    "publication_decision",
    "reasons",
    "review_notes",
]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Regenerate and summarize the student research publication review CSV."
    )
    parser.add_argument(
        "--review-csv",
        type=Path,
        default=REVIEW_CSV,
        help="Review CSV path. Defaults to data-maintenance/student-research-publication-review.csv.",
    )
    parser.add_argument(
        "--exceptions-csv",
        type=Path,
        default=EXCEPTIONS_CSV,
        help="Convenience exceptions CSV path.",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print summary after regenerating the review CSV.",
    )
    args = parser.parse_args()

    rows = generate_review_rows(args.review_csv)
    warnings, errors = validate_review_rows(rows)
    write_csv(args.review_csv, rows, REVIEW_COLUMNS)
    write_csv(args.exceptions_csv, exception_rows(rows), EXCEPTION_COLUMNS)
    payload = {
        "reviewCsv": str(args.review_csv),
        "exceptionsCsv": str(args.exceptions_csv),
        **summary_for_rows(rows),
        "validationWarnings": warnings,
        "errors": errors,
    }
    print_json(payload)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
