"""Shared helpers for student research review and publication scripts."""

from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PEOPLE_DIR = ROOT / "src/content/people"
THESIS_DIR = ROOT / "src/content/student-research"
REVIEW_CSV = ROOT / "data-maintenance/student-research-publication-review.csv"
EXCEPTIONS_CSV = ROOT / "data-maintenance/student-research-publication-exceptions.csv"
IMPORT_EXCEPTIONS_CSV = ROOT / "docs/imports/review/UNDERGRAD_THESIS_IMPORT_EXCEPTIONS_2026.csv"

DECISIONS = {"pending-review", "approve", "hold", "needs-fix"}
PUBLIC_FLAGS = {"auto", "yes", "no"}
AFFILIATED_ROLES = {"undergraduate-researcher", "alumni"}

REVIEW_COLUMNS = [
    "record_id",
    "year",
    "thesis_title",
    "student_1",
    "student_2",
    "main_adviser",
    "co_advisers",
    "association_basis",
    "student_1_envisage_affiliated",
    "student_2_envisage_affiliated",
    "abstract_preview",
    "abstract_present",
    "keywords",
    "keywords_present",
    "thesis_status",
    "thesis_slug",
    "current_visibility",
    "publication_decision",
    "public_thesis",
    "public_student_1",
    "public_student_2",
    "review_notes",
]

PRESERVED_REVIEW_COLUMNS = [
    "publication_decision",
    "public_thesis",
    "public_student_1",
    "public_student_2",
    "review_notes",
]


@dataclass
class ContentRecord:
    path: Path
    frontmatter: dict[str, Any]
    body: str

    @property
    def slug(self) -> str:
        return str(self.frontmatter.get("slug", self.path.stem))


def normalize_space(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").replace("\u00a0", " ")).strip()


def parse_frontmatter(path: Path) -> ContentRecord:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return ContentRecord(path, {}, text)
    lines = text.splitlines()
    frontmatter: dict[str, Any] = {}
    index = 1
    body_start = len(lines)
    while index < len(lines):
        line = lines[index]
        if line == "---":
            body_start = index + 1
            break
        if not line or line.startswith("  - ") or line.startswith("  "):
            index += 1
            continue
        if ": |-" in line:
            key = line.split(":", 1)[0]
            block: list[str] = []
            index += 1
            while index < len(lines) and (lines[index].startswith("  ") or lines[index] == ""):
                block.append(lines[index][2:] if lines[index].startswith("  ") else "")
                index += 1
            frontmatter[key] = "\n".join(block).strip()
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            value = value.strip()
            if value == "[]":
                frontmatter[key] = []
            elif value == "":
                values: list[str] = []
                index += 1
                while index < len(lines) and lines[index].startswith("  - "):
                    values.append(lines[index][4:].strip().strip('"'))
                    index += 1
                frontmatter[key] = values
                continue
            else:
                frontmatter[key] = value.strip('"')
        index += 1
    return ContentRecord(path, frontmatter, "\n".join(lines[body_start:]))


def load_theses() -> list[ContentRecord]:
    records = [parse_frontmatter(path) for path in THESIS_DIR.glob("*.md")]
    return sorted(
        [record for record in records if record.frontmatter.get("thesisType")],
        key=lambda record: (
            -int(record.frontmatter.get("year") or 0),
            str(record.frontmatter.get("thesisTitle", "")),
        ),
    )


def load_people_by_slug() -> dict[str, ContentRecord]:
    return {
        record.slug: record
        for record in (parse_frontmatter(path) for path in PEOPLE_DIR.glob("*.md"))
        if record.frontmatter.get("name")
    }


def read_existing_review(path: Path = REVIEW_CSV) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8", newline="") as handle:
        return {
            row.get("record_id", ""): row
            for row in csv.DictReader(handle)
            if row.get("record_id")
        }


def write_csv(path: Path, rows: list[dict[str, str]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def abstract_preview(value: str, length: int = 260) -> str:
    preview = normalize_space(value)
    if len(preview) <= length:
        return preview
    return preview[: length - 1].rstrip() + "..."


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def normalize_decision(value: str) -> str:
    value = normalize_space(value) or "pending-review"
    return value if value in DECISIONS else value


def normalize_public_flag(value: str) -> str:
    value = normalize_space(value) or "auto"
    return value if value in PUBLIC_FLAGS else value


def is_affiliated_student(thesis: ContentRecord, index: int) -> bool:
    students = thesis.frontmatter.get("studentPeople") or []
    if index >= len(students):
        return False
    return thesis.frontmatter.get("envisageAssociationBasis") == "main-adviser"


def imported_exception_index() -> dict[str, list[str]]:
    if not IMPORT_EXCEPTIONS_CSV.exists():
        return {}
    exception_map: dict[str, list[str]] = {}
    with IMPORT_EXCEPTIONS_CSV.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            thesis_id = row.get("thesis_id", "")
            exception = row.get("exception_type", "")
            if thesis_id and exception:
                exception_map.setdefault(thesis_id, []).append(exception)
    return exception_map


def review_row_for_thesis(
    thesis: ContentRecord,
    preserved: dict[str, dict[str, str]],
) -> dict[str, str]:
    data = thesis.frontmatter
    record_id = str(data.get("recordId", ""))
    previous = preserved.get(record_id, {})
    students = data.get("students") or []
    co_advisers = data.get("coAdvisers") or []
    keywords = data.get("keywords") or []
    row = {
        "record_id": record_id,
        "year": str(data.get("year", "")),
        "thesis_title": str(data.get("thesisTitle", "")),
        "student_1": students[0] if students else "",
        "student_2": students[1] if len(students) > 1 else "",
        "main_adviser": str(data.get("adviser", "")),
        "co_advisers": "; ".join(co_advisers),
        "association_basis": str(data.get("envisageAssociationBasis", "")),
        "student_1_envisage_affiliated": yes_no(is_affiliated_student(thesis, 0)),
        "student_2_envisage_affiliated": yes_no(is_affiliated_student(thesis, 1)) if len(students) > 1 else "",
        "abstract_preview": abstract_preview(str(data.get("abstract", ""))),
        "abstract_present": yes_no(bool(data.get("abstract"))),
        "keywords": "; ".join(keywords),
        "keywords_present": yes_no(bool(keywords)),
        "thesis_status": str(data.get("status", "")),
        "thesis_slug": thesis.slug,
        "current_visibility": str(data.get("visibility", "")),
        "publication_decision": "pending-review",
        "public_thesis": "auto",
        "public_student_1": "auto",
        "public_student_2": "auto" if len(students) > 1 else "",
        "review_notes": "",
    }
    for column in PRESERVED_REVIEW_COLUMNS:
        if previous.get(column):
            row[column] = previous[column]
    return row


def generate_review_rows(path: Path = REVIEW_CSV) -> list[dict[str, str]]:
    preserved = read_existing_review(path)
    return [review_row_for_thesis(thesis, preserved) for thesis in load_theses() if thesis.frontmatter.get("recordId")]


def validate_review_rows(rows: list[dict[str, str]]) -> tuple[list[str], list[str]]:
    warnings: list[str] = []
    errors: list[str] = []
    seen: set[str] = set()
    for row in rows:
        record_id = row.get("record_id", "")
        if not record_id:
            errors.append("Review row has a blank record_id.")
        elif record_id in seen:
            errors.append(f"{record_id}: duplicate record_id in review CSV.")
        seen.add(record_id)
        decision = normalize_decision(row.get("publication_decision", ""))
        if decision not in DECISIONS:
            errors.append(f"{record_id}: invalid publication_decision '{decision}'.")
        for column in ("public_thesis", "public_student_1", "public_student_2"):
            value = row.get(column, "")
            if not value:
                continue
            flag = normalize_public_flag(value)
            if flag not in PUBLIC_FLAGS:
                errors.append(f"{record_id}: invalid {column} value '{flag}'.")
        if decision == "approve" and row.get("abstract_present") != "yes":
            warnings.append(f"{record_id}: approved thesis is missing an abstract.")
        if decision == "approve" and row.get("public_thesis") == "no":
            warnings.append(f"{record_id}: approved but public_thesis is no; thesis will remain internal.")
    return warnings, errors


def summary_for_rows(rows: list[dict[str, str]]) -> dict[str, Any]:
    counts = {decision: 0 for decision in DECISIONS}
    for row in rows:
        decision = normalize_decision(row.get("publication_decision", ""))
        if decision in counts:
            counts[decision] += 1
    return {
        "total": len(rows),
        "pendingReview": counts["pending-review"],
        "approved": counts["approve"],
        "hold": counts["hold"],
        "needsFix": counts["needs-fix"],
        "missingAbstracts": sum(1 for row in rows if row.get("abstract_present") != "yes"),
        "missingKeywords": sum(1 for row in rows if row.get("keywords_present") != "yes"),
        "mainAdvised": sum(1 for row in rows if row.get("association_basis") == "main-adviser"),
        "coAdvisedOnly": sum(1 for row in rows if row.get("association_basis") == "co-adviser-only"),
    }


def exception_rows(review_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    imported_exceptions = imported_exception_index()
    rows: list[dict[str, str]] = []
    for row in review_rows:
        reasons: list[str] = []
        if row.get("abstract_present") != "yes":
            reasons.append("missing abstract")
        if row.get("keywords_present") != "yes":
            reasons.append("missing keywords")
        if row.get("association_basis") == "co-adviser-only":
            reasons.append("co-adviser-only")
        if row.get("student_1_envisage_affiliated") == "no" or row.get("student_2_envisage_affiliated") == "no":
            reasons.append("non-affiliated authors")
        if row.get("publication_decision") in {"hold", "needs-fix"}:
            reasons.append(row["publication_decision"])
        reasons.extend(imported_exceptions.get(row.get("record_id", ""), []))
        if not reasons:
            continue
        rows.append(
            {
                "record_id": row["record_id"],
                "year": row["year"],
                "thesis_title": row["thesis_title"],
                "association_basis": row["association_basis"],
                "publication_decision": row["publication_decision"],
                "reasons": "; ".join(dict.fromkeys(reasons)),
                "review_notes": row["review_notes"],
            }
        )
    return rows


def update_frontmatter_value(path: Path, key: str, value: str) -> bool:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    changed = False
    in_frontmatter = False
    for index, line in enumerate(lines):
        if index == 0 and line == "---":
            in_frontmatter = True
            continue
        if in_frontmatter and line == "---":
            break
        if in_frontmatter and line.startswith(f"{key}:"):
            new_line = f"{key}: {value}"
            changed = line != new_line
            lines[index] = new_line
            break
    if changed:
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return changed


def print_json(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, indent=2, ensure_ascii=False))
