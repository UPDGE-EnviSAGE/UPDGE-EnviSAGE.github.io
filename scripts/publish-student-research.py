#!/usr/bin/env python3
"""Apply approved student research publication decisions.

Dry-run is the default. Use --write to update canonical content records.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Any

from student_research_publication import (
    PEOPLE_DIR,
    REVIEW_CSV,
    THESIS_DIR,
    load_people_by_slug,
    load_theses,
    normalize_decision,
    normalize_public_flag,
    print_json,
    update_frontmatter_value,
    validate_review_rows,
)


def read_review_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"Review CSV not found: {path}. Run scripts/review-student-research.py first.")
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def should_publish_thesis(row: dict[str, str]) -> bool:
    return (
        normalize_decision(row.get("publication_decision", "")) == "approve"
        and normalize_public_flag(row.get("public_thesis", "")) != "no"
    )


def should_publish_student(row: dict[str, str], index: int) -> bool:
    flag = normalize_public_flag(row.get(f"public_student_{index + 1}", ""))
    affiliated = row.get(f"student_{index + 1}_envisage_affiliated") == "yes"
    return should_publish_thesis(row) and affiliated and flag != "no"


def desired_thesis_visibility(row: dict[str, str]) -> str:
    return "public" if should_publish_thesis(row) else "internal"


def summarize(review_csv: Path, write: bool) -> tuple[dict[str, Any], int]:
    rows = read_review_rows(review_csv)
    warnings, errors = validate_review_rows(rows)
    rows_by_id = {row.get("record_id", ""): row for row in rows}
    theses_by_id = {
        str(thesis.frontmatter.get("recordId")): thesis
        for thesis in load_theses()
        if thesis.frontmatter.get("recordId")
    }
    people_by_slug = load_people_by_slug()

    theses_to_publish: list[str] = []
    theses_to_keep_internal: list[str] = []
    students_to_promote: set[str] = set()
    students_remaining_internal: set[str] = set()
    public_alumni_to_add: set[str] = set()
    co_advised_only_authors_internal: set[str] = set()
    thesis_changes = 0
    person_changes = 0

    for record_id, row in rows_by_id.items():
        thesis = theses_by_id.get(record_id)
        if not thesis:
            errors.append(f"{record_id}: no canonical thesis record found.")
            continue
        desired_visibility = desired_thesis_visibility(row)
        title = str(thesis.frontmatter.get("thesisTitle", record_id))
        if desired_visibility == "public":
            theses_to_publish.append(record_id)
        else:
            theses_to_keep_internal.append(record_id)
        if write:
            thesis_changes += int(update_frontmatter_value(thesis.path, "visibility", desired_visibility))
            thesis_changes += int(
                update_frontmatter_value(
                    thesis.path,
                    "reviewStatus",
                    "public" if desired_visibility == "public" else "under-review",
                )
            )

        student_people = thesis.frontmatter.get("studentPeople") or []
        student_names = thesis.frontmatter.get("students") or []
        for index, student_slug in enumerate(student_people):
            person = people_by_slug.get(student_slug)
            student_name = student_names[index] if index < len(student_names) else student_slug
            if not person:
                errors.append(f"{record_id}: missing Person record for student slug '{student_slug}'.")
                continue
            affiliated = row.get(f"student_{index + 1}_envisage_affiliated") == "yes"
            if should_publish_student(row, index):
                students_to_promote.add(student_slug)
                if "alumni" in (person.frontmatter.get("categories") or []):
                    public_alumni_to_add.add(student_slug)
                if write:
                    person_changes += int(update_frontmatter_value(person.path, "visibility", "public"))
            else:
                students_remaining_internal.add(student_slug)
                if write:
                    person_changes += int(update_frontmatter_value(person.path, "visibility", "internal"))
            if should_publish_thesis(row) and not affiliated:
                co_advised_only_authors_internal.add(student_name)
        if (
            should_publish_thesis(row)
            and row.get("abstract_present") == "yes"
            and not thesis.frontmatter.get("abstract")
        ):
            warnings.append(f"{record_id}: approved thesis '{title}' is missing an abstract.")

    if not write:
        thesis_changes = 0
        person_changes = 0

    payload: dict[str, Any] = {
        "write": write,
        "reviewCsv": str(review_csv),
        "thesesToPublish": len(theses_to_publish),
        "thesesToKeepInternal": len(theses_to_keep_internal),
        "studentsToPromotePublic": len(students_to_promote),
        "studentsRemainingInternal": len(students_remaining_internal),
        "publicAlumniToAdd": len(public_alumni_to_add),
        "coAdvisedOnlyAuthorsRemainingNonMember": len(co_advised_only_authors_internal),
        "thesisRecordsChanged": thesis_changes,
        "personRecordsChanged": person_changes,
        "validationWarnings": warnings,
        "errors": errors,
        "sampleThesesToPublish": theses_to_publish[:10],
    }
    return payload, 1 if errors else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish explicitly approved student research records.")
    parser.add_argument(
        "--review-csv",
        type=Path,
        default=REVIEW_CSV,
        help="Review CSV path. Defaults to data-maintenance/student-research-publication-review.csv.",
    )
    parser.add_argument("--write", action="store_true", help="Apply approved publication changes.")
    parser.add_argument(
        "--approve-all-reviewed",
        action="store_true",
        help="Documented convenience flag; only rows already marked publication_decision=approve are ever affected, and --write is still required to apply changes.",
    )
    args = parser.parse_args()
    payload, status = summarize(args.review_csv, args.write)
    if args.approve_all_reviewed:
        payload["bulkApprovalMode"] = "approve-marked-rows-only"
    print_json(payload)
    return status


if __name__ == "__main__":
    raise SystemExit(main())
