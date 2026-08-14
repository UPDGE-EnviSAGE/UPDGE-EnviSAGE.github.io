#!/usr/bin/env python3
"""Synchronize undergraduate thesis maintenance CSV rows into canonical content.

Dry-run is the default. Use --write only after reviewing the summary.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PEOPLE_DIR = ROOT / "src/content/people"
THESIS_DIR = ROOT / "src/content/student-research"
IMPORTER_PATH = ROOT / "scripts/import-undergraduate-theses.py"
IMPORT_BATCH = "undergrad-thesis-maintenance"
HISTORICAL_IMPORT_BATCH = "undergrad-thesis-selected-advisers-2026"
THESIS_TYPE = "bs-geodetic-engineering-thesis"
PROGRAM = "BS Geodetic Engineering"


spec = importlib.util.spec_from_file_location("undergrad_importer", IMPORTER_PATH)
if spec is None or spec.loader is None:
    raise SystemExit(f"Unable to load importer module: {IMPORTER_PATH}")
importer = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = importer
spec.loader.exec_module(importer)


REQUIRED_COLUMNS = [
    "record_id",
    "academic_year",
    "thesis_status",
    "thesis_title",
    "student_1",
    "student_2",
    "main_adviser",
    "co_advisers",
    "abstract",
    "keywords",
    "visibility",
    "review_status",
    "review_notes",
]

VALID_STATUSES = {"ongoing", "completed", "archived"}
VALID_VISIBILITY = {"internal", "private", "archived"}


@dataclass
class ExistingRecord:
    path: Path
    slug: str
    frontmatter: dict[str, Any]


@dataclass
class SyncSummary:
    thesis_added: int = 0
    thesis_updated: int = 0
    thesis_unchanged: int = 0
    people_added: int = 0
    people_updated: int = 0
    people_unchanged: int = 0
    affiliation_changes: list[str] = field(default_factory=list)
    alumni_transitions: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def parse_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    lines = text.splitlines()
    data: dict[str, Any] = {}
    index = 1
    while index < len(lines):
        line = lines[index]
        if line == "---":
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
            data[key] = "\n".join(block).strip()
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            value = value.strip()
            if value == "[]":
                data[key] = []
            elif value == "":
                values: list[str] = []
                index += 1
                while index < len(lines) and lines[index].startswith("  - "):
                    values.append(lines[index][4:].strip().strip('"'))
                    index += 1
                data[key] = values
                continue
            else:
                data[key] = value.strip('"')
        index += 1
    return data


def load_existing_theses() -> dict[str, ExistingRecord]:
    records: dict[str, ExistingRecord] = {}
    for path in THESIS_DIR.glob("*.md"):
        frontmatter = parse_frontmatter(path)
        record_id = frontmatter.get("recordId")
        if not record_id:
            continue
        records[str(record_id)] = ExistingRecord(path, str(frontmatter.get("slug", path.stem)), frontmatter)
    return records


def load_existing_people() -> dict[str, ExistingRecord]:
    records: dict[str, ExistingRecord] = {}
    for path in PEOPLE_DIR.glob("*.md"):
        frontmatter = parse_frontmatter(path)
        name = str(frontmatter.get("name", "")).strip()
        if not name:
            continue
        records[importer.normalize_text(name)] = ExistingRecord(path, str(frontmatter.get("slug", path.stem)), frontmatter)
    return records


def read_rows(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = [column for column in REQUIRED_COLUMNS if column not in (reader.fieldnames or [])]
        if missing:
            raise SystemExit(f"Maintenance CSV is missing required columns: {missing}")
        return [{key: importer.normalize_space(value) for key, value in row.items()} for row in reader]


def canonical_review_status(value: str, thesis_status: str) -> str:
    normalized = importer.slugify(value)
    if normalized == "public":
        return "under-review"
    if normalized in {"under-review", "ongoing-private"}:
        return normalized
    return "ongoing-private" if thesis_status == "ongoing" else "under-review"


def unique_slug(base: str, used: set[str], salt: str) -> str:
    slug, _ = importer.make_unique_slug(base, used, salt)
    return slug


def thesis_from_row(
    row: dict[str, str],
    existing_theses: dict[str, ExistingRecord],
    existing_people: dict[str, ExistingRecord],
    used_thesis_slugs: set[str],
    used_person_slugs: set[str],
    summary: SyncSummary,
) -> tuple[Any, dict[str, Any]]:
    record_id = importer.slugify(row["record_id"])
    status = importer.slugify(row["thesis_status"])
    visibility = importer.slugify(row.get("visibility") or "internal")
    if not record_id:
        summary.errors.append("A row has a blank record_id.")
    if status not in VALID_STATUSES:
        summary.errors.append(f"{record_id}: thesis_status must be ongoing, completed, or archived.")
    if visibility == "public":
        summary.warnings.append(f"{record_id}: public visibility requested; forcing internal for Phase 6C.1.")
        visibility = "internal"
    if visibility not in VALID_VISIBILITY:
        summary.warnings.append(f"{record_id}: unsupported visibility '{visibility}'; forcing internal.")
        visibility = "internal"

    title = importer.normalize_space(row["thesis_title"])
    students = [importer.normalize_space(row["student_1"]), importer.normalize_space(row["student_2"])]
    students = [student for student in students if student and not importer.is_blankish(student)]
    if not title:
        summary.errors.append(f"{record_id}: thesis_title is required.")
    if len(students) not in {1, 2}:
        summary.errors.append(f"{record_id}: BS Geodetic Engineering theses require one or two students.")

    year = importer.parse_year(row.get("academic_year", ""))
    faculty_index = importer.faculty_matcher()
    adviser = importer.normalize_space(row["main_adviser"])
    co_advisers = importer.split_people(row.get("co_advisers", ""))
    main_match = importer.match_faculty(adviser, faculty_index) if adviser else importer.FacultyMatch("", "")
    co_matches = [importer.match_faculty(name, faculty_index) for name in co_advisers]
    main_faculty = main_match.slug
    co_faculty = [match.slug for match in co_matches if match.slug]
    if not main_faculty and not co_faculty:
        summary.warnings.append(f"{record_id}: no EnviSAGE faculty adviser match; record remains internal.")
    for match in [main_match, *co_matches]:
        if match.ambiguous:
            summary.errors.append(f"{record_id}: ambiguous adviser match for '{match.original}': {match.ambiguous}")

    existing = existing_theses.get(record_id)
    if existing:
        slug = existing.slug
    else:
        slug = unique_slug(importer.slugify(title), used_thesis_slugs, f"{record_id} {year or ''} {' '.join(students)} {title}")

    student_people: list[str] = []
    generated_students: dict[str, Any] = {}
    for display_name in students:
        normalized = importer.normalize_text(display_name)
        existing_person = existing_people.get(normalized)
        if existing_person:
            existing_batch = existing_person.frontmatter.get("importBatch")
            if existing_batch not in {HISTORICAL_IMPORT_BATCH, IMPORT_BATCH}:
                summary.errors.append(
                    f"{record_id}: student name '{display_name}' matches non-import Person record '{existing_person.slug}'; manual review required."
                )
        if existing_person:
            student_slug = existing_person.slug
        else:
            student_slug = unique_slug(importer.slugify(display_name), used_person_slugs, display_name)
        student_people.append(student_slug)
        affiliated = bool(main_faculty)
        student = importer.Student(display_name, normalized, student_slug, affiliated=affiliated)
        student.thesis_slugs.add(slug)
        generated_students[normalized] = student
        previous = existing_person.frontmatter if existing_person else {}
        previous_status = previous.get("membershipStatus")
        desired_status = "active" if affiliated and status == "ongoing" else "alumni" if affiliated and status == "completed" else "inactive"
        if previous_status and previous_status != desired_status:
            summary.affiliation_changes.append(f"{display_name}: {previous_status} -> {desired_status}")
            if previous_status == "active" and desired_status == "alumni":
                summary.alumni_transitions.append(display_name)

    topics, _unmapped = importer.map_topics(importer.split_keywords(row.get("keywords", "")))
    thesis = importer.Thesis(
        record_id=record_id,
        source_row=0,
        year=year,
        title=title,
        slug=slug,
        students=students,
        student_people=student_people,
        adviser=adviser,
        main_adviser_person=main_faculty,
        co_advisers=co_advisers,
        co_adviser_people=co_faculty,
        abstract=importer.normalize_space(row.get("abstract", "")) or None,
        keywords=importer.split_keywords(row.get("keywords", "")),
        research_topics=topics,
        envisage_associated=bool(main_faculty or co_faculty),
        association_basis="main-adviser" if main_faculty else "co-adviser-only" if co_faculty else "none",
        envisage_main_adviser=main_faculty,
        envisage_co_advisers=co_faculty,
        adviser_roles=(["main-adviser"] if main_faculty else []) + (["co-adviser"] if co_faculty else []),
    )
    return thesis, generated_students


def person_markdown(student: Any, thesis_status: str, import_batch: str = IMPORT_BATCH) -> str:
    original_affiliated = student.affiliated
    desired_membership = getattr(student, "desired_membership", None)
    if desired_membership == "active" or (original_affiliated and thesis_status == "ongoing"):
        roles = ["undergraduate-researcher"]
        categories = ["undergraduate-researcher"]
        membership = "active"
    elif desired_membership == "alumni" or (original_affiliated and thesis_status == "completed"):
        roles = ["undergraduate-researcher", "alumni"]
        categories = ["undergraduate-researcher", "alumni"]
        membership = "alumni"
    else:
        roles = ["thesis-author"]
        categories = ["thesis-author"]
        membership = "inactive"
    lines = [
        "---",
        f"name: {importer.yaml_scalar(student.display_name)}",
        f"slug: {student.slug}",
        f"importBatch: {import_batch}",
    ]
    lines.extend(importer.yaml_slug_list("envisageRoles", roles))
    lines.extend(importer.yaml_slug_list("categories", categories))
    lines.append(f"membershipStatus: {membership}")
    lines.append(f'academicProgram: "{PROGRAM}"')
    for key in ("researchAreas", "researchInterests", "researchTopics", "projects", "theses", "publications", "datasets", "tools", "grants"):
        lines.extend(importer.yaml_slug_list(key, []))
    lines.extend(importer.yaml_slug_list("studentResearch", sorted(student.thesis_slugs)))
    lines.append("visibility: internal")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def thesis_markdown(thesis: Any, row: dict[str, str], existing: ExistingRecord | None = None) -> str:
    text = importer.thesis_markdown(thesis)
    source_row = existing.frontmatter.get("sourceRow") if existing else None
    if source_row:
        text = text.replace("sourceRow: 0\n", f"sourceRow: {source_row}\n")
    else:
        text = text.replace("sourceRow: 0\n", "")
    text = text.replace("status: completed\n", f"status: {importer.slugify(row['thesis_status'])}\n")
    text = text.replace("reviewStatus: under-review\n", f"reviewStatus: {canonical_review_status(row.get('review_status', ''), row['thesis_status'])}\n")
    return text


def sync(csv_path: Path, write: bool) -> SyncSummary:
    rows = read_rows(csv_path)
    summary = SyncSummary()
    existing_theses = load_existing_theses()
    existing_people = load_existing_people()
    seen_ids: set[str] = set()
    used_thesis_slugs = {record.slug for record in existing_theses.values()}
    used_person_slugs = {record.slug for record in existing_people.values()}
    desired_thesis_ids: set[str] = set()
    desired_theses: list[tuple[dict[str, str], Any]] = []
    desired_people: dict[str, Any] = {}
    desired_people_status: dict[str, str] = {}

    for row in rows:
        if importer.slugify(row.get("sync_action", "")) in {"exclude", "skip"}:
            summary.warnings.append(f"{row.get('record_id', '<blank>')}: row excluded by sync_action.")
            continue
        record_id = importer.slugify(row["record_id"])
        if record_id in seen_ids:
            summary.errors.append(f"{record_id}: duplicate record_id in maintenance CSV.")
            continue
        seen_ids.add(record_id)
        desired_thesis_ids.add(record_id)
        thesis, generated_students = thesis_from_row(
            row,
            existing_theses,
            existing_people,
            used_thesis_slugs,
            used_person_slugs,
            summary,
        )
        if summary.errors:
            continue
        desired_theses.append((row, thesis))
        for student in generated_students.values():
            status = importer.slugify(row["thesis_status"])
            current = desired_people.get(student.normalized)
            if current is None:
                desired_people[student.normalized] = student
            else:
                current.thesis_slugs.update(student.thesis_slugs)
                current.affiliated = current.affiliated or student.affiliated
            desired_status = "active" if student.affiliated and status == "ongoing" else "alumni" if student.affiliated and status == "completed" else "inactive"
            previous_desired = desired_people_status.get(student.normalized)
            if previous_desired != "active":
                desired_people_status[student.normalized] = desired_status if previous_desired != "alumni" else previous_desired

    if summary.errors:
        return summary

    for row, thesis in desired_theses:
        record_id = importer.slugify(row["record_id"])
        existing_thesis = existing_theses.get(record_id)
        desired_text = thesis_markdown(thesis, row, existing_thesis)
        thesis_path = existing_thesis.path if existing_thesis else THESIS_DIR / f"{thesis.slug}.md"
        current_text = thesis_path.read_text(encoding="utf-8") if thesis_path.exists() else None
        if current_text is None:
            summary.thesis_added += 1
        elif current_text != desired_text:
            summary.thesis_updated += 1
        else:
            summary.thesis_unchanged += 1
        if write and current_text != desired_text:
            thesis_path.write_text(desired_text, encoding="utf-8")

    for normalized, student in desired_people.items():
        setattr(student, "desired_membership", desired_people_status.get(normalized, "inactive"))
        existing_person = existing_people.get(normalized)
        import_batch = str(existing_person.frontmatter.get("importBatch", IMPORT_BATCH)) if existing_person else IMPORT_BATCH
        desired_person_text = person_markdown(student, desired_people_status.get(normalized, "inactive"), import_batch)
        person_path = existing_person.path if existing_person else PEOPLE_DIR / f"{student.slug}.md"
        current_person_text = person_path.read_text(encoding="utf-8") if person_path.exists() else None
        if current_person_text is None:
            summary.people_added += 1
        elif current_person_text != desired_person_text:
            summary.people_updated += 1
        else:
            summary.people_unchanged += 1
        if write and current_person_text != desired_person_text:
            person_path.write_text(desired_person_text, encoding="utf-8")

    absent = sorted(set(existing_theses) - desired_thesis_ids)
    if absent:
        summary.warnings.append(
            f"{len(absent)} canonical thesis record(s) with recordId are absent from the maintenance CSV; no deletion performed."
        )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync undergraduate thesis maintenance CSV into canonical records.")
    parser.add_argument("csv_path", type=Path, help="Path to data-maintenance/undergraduate-theses.csv")
    parser.add_argument("--write", action="store_true", help="Write canonical content changes.")
    args = parser.parse_args()
    summary = sync(args.csv_path, args.write)
    payload = {
        "write": args.write,
        "thesisRecordsAdded": summary.thesis_added,
        "thesisRecordsUpdated": summary.thesis_updated,
        "thesisRecordsUnchanged": summary.thesis_unchanged,
        "personRecordsAdded": summary.people_added,
        "personRecordsUpdated": summary.people_updated,
        "personRecordsUnchanged": summary.people_unchanged,
        "affiliationChanges": summary.affiliation_changes,
        "alumniTransitions": summary.alumni_transitions,
        "validationWarnings": summary.warnings,
        "errors": summary.errors,
    }
    print(importer.json.dumps(payload, indent=2, ensure_ascii=False))
    return 1 if summary.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
