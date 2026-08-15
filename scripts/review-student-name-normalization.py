#!/usr/bin/env python3
"""Generate a maintainer QA report for public student display-name normalization."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PEOPLE_DIR = ROOT / "src" / "content" / "people"
THESIS_DIR = ROOT / "src" / "content" / "student-research"
OUTPUT = ROOT / "data-maintenance" / "student-name-normalization-review.csv"

LOWERCASE_PARTICLES = {
    "de",
    "del",
    "dela",
    "la",
    "las",
    "los",
    "van",
    "von",
    "y",
}


def frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return ""
    parts = re.split(r"^---\s*$", text, maxsplit=2, flags=re.MULTILINE)
    return parts[1] if len(parts) > 2 else ""


def scalar(frontmatter_text: str, field: str) -> str:
    match = re.search(rf"^{re.escape(field)}:\s*(.+?)\s*$", frontmatter_text, re.MULTILINE)
    if not match:
        return ""
    return match.group(1).strip().strip("\"'")


def list_field(frontmatter_text: str, field: str) -> list[str]:
    match = re.search(
        rf"^{re.escape(field)}:\s*\n((?:  - .+\n)+)",
        frontmatter_text,
        re.MULTILINE,
    )
    if not match:
        return []
    return [
        line.split("-", 1)[1].strip().strip("\"'")
        for line in match.group(1).splitlines()
        if line.strip().startswith("-")
    ]


def normalize_spaces(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip())


def format_name_part(part: str, index: int) -> str:
    if re.fullmatch(r"[A-Z]\.", part):
        return part
    lower = part.lower()
    if index > 0 and lower in LOWERCASE_PARTICLES:
        return lower
    return re.sub(
        r"(^|[-'])([A-Za-z])",
        lambda match: f"{match.group(1)}{match.group(2).upper()}",
        lower,
    )


def title_case_name(name: str) -> str:
    return " ".join(format_name_part(part, index) for index, part in enumerate(name.split(" ")))


def format_person_display_name(name: str) -> str:
    cleaned = normalize_spaces(name.strip("\"'"))
    if "," in cleaned and cleaned.count(",") == 1:
        last, first = [part.strip() for part in cleaned.split(",", 1)]
        if last and first:
            return title_case_name(f"{first} {last}")
    return title_case_name(cleaned)


def normalization_rule(original: str, normalized: str) -> str:
    if "," in original and original.count(",") == 1:
        return "comma-format"
    if re.search(r"\b[A-Z]{2,}\b", original):
        return "all-caps-normalization"
    if original != normalized:
        return "title-case-particles"
    return "unchanged"


def review_status(original: str) -> str:
    if re.search(r"\b[A-Z]\s+[A-Z]\b", original):
        return "review-initial-spacing"
    if len(original.split(",")) > 2:
        return "review-comma-structure"
    return "pending-maintainer-review"


def main() -> None:
    rows: list[dict[str, str]] = []
    people_names_by_slug: dict[str, str] = {}

    for path in sorted(PEOPLE_DIR.glob("*.md")):
        metadata = frontmatter(path.read_text())
        slug = scalar(metadata, "slug") or path.stem
        name = scalar(metadata, "name")
        if slug and name:
            people_names_by_slug[slug] = name

    for path in sorted(THESIS_DIR.glob("*.md")):
        metadata = frontmatter(path.read_text())
        if scalar(metadata, "visibility") != "public":
            continue

        students = list_field(metadata, "students")
        student_people = list_field(metadata, "studentPeople")

        for index, original in enumerate(students):
            person_id = student_people[index] if index < len(student_people) else ""
            stored_name = people_names_by_slug.get(person_id, original)
            normalized = format_person_display_name(stored_name)
            if stored_name == normalized:
                continue

            rows.append(
                {
                    "person_id": person_id,
                    "original_name": stored_name,
                    "normalized_display_name": normalized,
                    "normalization_rule": normalization_rule(stored_name, normalized),
                    "thesis_record_id": scalar(metadata, "recordId") or path.stem,
                    "review_status": review_status(stored_name),
                    "review_notes": "",
                }
            )

    with OUTPUT.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "person_id",
                "original_name",
                "normalized_display_name",
                "normalization_rule",
                "thesis_record_id",
                "review_status",
                "review_notes",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} name normalization review rows to {OUTPUT}")


if __name__ == "__main__":
    main()
