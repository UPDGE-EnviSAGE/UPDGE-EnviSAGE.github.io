#!/usr/bin/env python3
"""Import selected BS Geodetic Engineering thesis records into Astro content.

This script intentionally uses only the Python standard library so the website
does not gain a runtime or development dependency just to read a one-time Excel
administrative source.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import unicodedata
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
PEOPLE_DIR = ROOT / "src/content/people"
THESIS_DIR = ROOT / "src/content/student-research"
AUDIT_PATH = ROOT / "docs/imports/UNDERGRAD_THESIS_IMPORT_2026.md"

NS = {
    "a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}

EXPECTED_COLUMNS = [
    "Year",
    "Author 1",
    "Author 2",
    "Main Adviser",
    "Co-advisers",
    "Title",
    "Abstract",
    "Key Words",
    "Matched Adviser(s)",
    "Role(s)",
]

FACULTY = {
    "ariel-c-blanco": "Ariel C. Blanco",
    "ayin-m-tamondong": "Ayin M. Tamondong",
    "jommer-m-medina": "Jommer M. Medina",
    "erica-erin-e-elazegui": "Erica Erin E. Elazegui",
    "margaux-angelica-a-cruz": "Margaux Angelica A. Cruz",
    "john-emmanuel-d-escoto": "John Emmanuel D. Escoto",
}

IMPORT_BATCH = "undergrad-thesis-selected-advisers-2026"

TOPIC_KEYWORDS = {
    "water quality": "water-quality",
    "mangrove": "mangroves",
    "mangroves": "mangroves",
    "seagrass": "seagrass",
    "coral reef": "coral-reefs",
    "coral reefs": "coral-reefs",
    "flooding": "flooding",
    "flood": "flooding",
    "air quality": "air-quality",
    "pm2.5": "pm2-5",
    "bathymetry": "bathymetry",
    "lidar": "lidar",
    "biodiversity": "biodiversity",
    "agriculture": "agriculture",
    "fisheries": "fisheries",
    "aquaculture": "aquaculture",
    "land cover": "land-cover",
    "climate change": "climate-change",
}


@dataclass
class FacultyMatch:
    original: str
    normalized: str
    slug: str | None = None
    ambiguous: list[str] = field(default_factory=list)


@dataclass
class Student:
    display_name: str
    normalized: str
    slug: str
    affiliated: bool = False
    thesis_slugs: set[str] = field(default_factory=set)


@dataclass
class Thesis:
    source_row: int
    year: int | None
    title: str
    slug: str
    students: list[str]
    student_people: list[str]
    adviser: str
    main_adviser_person: str | None
    co_advisers: list[str]
    co_adviser_people: list[str]
    abstract: str | None
    keywords: list[str]
    research_topics: list[str]
    envisage_associated: bool
    association_basis: str
    envisage_main_adviser: str | None
    envisage_co_advisers: list[str]
    adviser_roles: list[str]


def column_index(cell_ref: str) -> int:
    letters = re.sub(r"[^A-Z]", "", cell_ref.upper())
    index = 0
    for letter in letters:
        index = index * 26 + (ord(letter) - ord("A") + 1)
    return index - 1


def normalize_space(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").replace("\u00a0", " ")).strip()


def normalize_text(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = value.lower()
    value = re.sub(r"\b(dr|prof|asst|assoc|assistant|associate|engr|eng|ms|mr|mrs|phd)\.?\b", " ", value)
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return normalize_space(value)


def is_blankish(value: str) -> bool:
    return not normalize_space(value) or normalize_text(value) in {
        "n a",
        "na",
        "none",
        "not applicable",
    }


def remove_middle_initials(normalized: str) -> str:
    parts = [part for part in normalized.split() if len(part) > 1]
    return " ".join(parts)


def faculty_keys(name: str) -> set[str]:
    normalized = normalize_text(name)
    keys = {normalized, remove_middle_initials(normalized)}
    parts = remove_middle_initials(normalized).split()
    if len(parts) >= 2:
        keys.add(f"{parts[0]} {parts[-1]}")
        keys.add(f"{parts[-1]} {parts[0]}")
        keys.add(f"{parts[-1]} {' '.join(parts[:-1])}")
        keys.add(f"{parts[-1]} {parts[0]}")
    return {key for key in keys if key}


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "untitled"


def yaml_scalar(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def yaml_block(key: str, value: str | None) -> list[str]:
    if not value:
        return []
    lines = [f"{key}: |-"]
    lines.extend(f"  {line.rstrip()}" if line.strip() else "" for line in value.splitlines())
    return lines


def yaml_list(key: str, values: list[str]) -> list[str]:
    if not values:
        return [f"{key}: []"]
    return [f"{key}:"] + [f"  - {yaml_scalar(value)}" for value in values]


def yaml_slug_list(key: str, values: list[str]) -> list[str]:
    if not values:
        return [f"{key}: []"]
    return [f"{key}:"] + [f"  - {value}" for value in values]


def read_shared_strings(zip_file: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in zip_file.namelist():
        return []
    root = ET.fromstring(zip_file.read("xl/sharedStrings.xml"))
    strings = []
    for item in root.findall("a:si", NS):
        strings.append("".join(text.text or "" for text in item.findall(".//a:t", NS)))
    return strings


def sheet_path(zip_file: zipfile.ZipFile, sheet_name: str) -> str:
    workbook = ET.fromstring(zip_file.read("xl/workbook.xml"))
    rels = ET.fromstring(zip_file.read("xl/_rels/workbook.xml.rels"))
    relmap = {rel.attrib["Id"]: rel.attrib["Target"] for rel in rels}
    for sheet in workbook.findall("a:sheets/a:sheet", NS):
        if sheet.attrib["name"] != sheet_name:
            continue
        rel_id = sheet.attrib["{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"]
        target = relmap[rel_id].lstrip("/")
        if not target.startswith("xl/"):
            target = f"xl/{target}"
        return target
    available = [sheet.attrib["name"] for sheet in workbook.findall("a:sheets/a:sheet", NS)]
    raise SystemExit(f"Worksheet '{sheet_name}' not found. Available sheets: {available}")


def cell_value(cell: ET.Element, shared_strings: list[str]) -> str:
    cell_type = cell.attrib.get("t")
    if cell_type == "inlineStr":
        return normalize_space("".join(text.text or "" for text in cell.findall(".//a:t", NS)))
    value = cell.find("a:v", NS)
    if value is None or value.text is None:
        return ""
    raw = value.text
    if cell_type == "s":
        return normalize_space(shared_strings[int(raw)])
    return normalize_space(raw)


def read_sheet_rows(source: Path, sheet_name: str) -> list[dict[str, str]]:
    with zipfile.ZipFile(source) as zip_file:
        shared_strings = read_shared_strings(zip_file)
        root = ET.fromstring(zip_file.read(sheet_path(zip_file, sheet_name)))
    rows: list[list[str]] = []
    for row in root.findall("a:sheetData/a:row", NS):
        values: dict[int, str] = {}
        for cell in row.findall("a:c", NS):
            values[column_index(cell.attrib["r"])] = cell_value(cell, shared_strings)
        width = max(values.keys(), default=-1) + 1
        rows.append([values.get(index, "") for index in range(width)])

    if not rows:
        return []
    headers = [normalize_space(header) for header in rows[0]]
    missing = [column for column in EXPECTED_COLUMNS if column not in headers]
    if missing:
        raise SystemExit(f"Missing expected columns in source worksheet: {missing}")

    records = []
    for offset, row in enumerate(rows[1:], start=2):
        padded = row + [""] * (len(headers) - len(row))
        record = {headers[index]: padded[index] for index in range(len(headers))}
        record["_row"] = str(offset)
        if any(normalize_space(value) for key, value in record.items() if key != "_row"):
            records.append(record)
    return records


def parse_year(value: str) -> int | None:
    value = normalize_space(value)
    if not value:
        return None
    try:
        year = int(float(value))
    except ValueError:
        match = re.search(r"\b(19|20)\d{2}\b", value)
        return int(match.group(0)) if match else None
    return year


def split_people(value: str) -> list[str]:
    value = normalize_space(value)
    if is_blankish(value):
        return []
    pieces = re.split(r"\s*(?:;|\n|\r|/|\band\b|&)\s*", value)
    return [normalize_space(piece) for piece in pieces if normalize_space(piece)]


def split_keywords(value: str) -> list[str]:
    value = normalize_space(value)
    if not value:
        return []
    pieces = re.split(r"\s*(?:;|,|\n|\r)\s*", value)
    seen: set[str] = set()
    keywords: list[str] = []
    for piece in pieces:
        keyword = normalize_space(piece)
        key = keyword.lower()
        if keyword and key not in seen:
            seen.add(key)
            keywords.append(keyword)
    return keywords


def map_topics(keywords: list[str]) -> tuple[list[str], list[str]]:
    topics: list[str] = []
    unmapped: list[str] = []
    for keyword in keywords:
        normalized = normalize_text(keyword).replace(" ", " ")
        topic = TOPIC_KEYWORDS.get(normalized)
        if topic and topic not in topics:
            topics.append(topic)
        elif not topic:
            unmapped.append(keyword)
    return topics, unmapped


def faculty_matcher() -> dict[str, list[str]]:
    index: dict[str, list[str]] = defaultdict(list)
    for slug, name in FACULTY.items():
        for key in faculty_keys(name):
            index[key].append(slug)
    return index


def match_faculty(name: str, index: dict[str, list[str]]) -> FacultyMatch:
    normalized = normalize_text(name)
    candidates: list[str] = []
    for key in faculty_keys(name):
        candidates.extend(index.get(key, []))
    unique = sorted(set(candidates))
    if len(unique) == 1:
        return FacultyMatch(name, normalized, slug=unique[0])
    if len(unique) > 1:
        return FacultyMatch(name, normalized, ambiguous=unique)
    return FacultyMatch(name, normalized)


def tracked_content_slugs(directory: Path) -> set[str]:
    relative_directory = directory.relative_to(ROOT)
    result = subprocess.run(
        ["git", "ls-files", str(relative_directory)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    reserved: set[str] = set()
    for line in result.stdout.splitlines():
        path = ROOT / line
        if path.suffix not in {".md", ".mdx"}:
            continue
        text = path.read_text(encoding="utf-8") if path.exists() else ""
        if f"importBatch: {IMPORT_BATCH}" in text:
            continue
        reserved.add(path.stem)
    return reserved


def make_unique_slug(base: str, used: set[str], salt: str) -> tuple[str, bool]:
    slug = base
    if slug not in used:
        used.add(slug)
        return slug, False
    suffix = hashlib.sha1(salt.encode("utf-8")).hexdigest()[:8]
    slug = f"{base}-{suffix}"
    counter = 2
    while slug in used:
        slug = f"{base}-{suffix}-{counter}"
        counter += 1
    used.add(slug)
    return slug, True


def build_import(rows: list[dict[str, str]]) -> tuple[list[Thesis], dict[str, Student], dict[str, Any]]:
    faculty_index = faculty_matcher()
    used_thesis_slugs = tracked_content_slugs(THESIS_DIR)
    used_person_slugs = tracked_content_slugs(PEOPLE_DIR)
    students_by_name: dict[str, Student] = {}
    theses: list[Thesis] = []
    audit: dict[str, Any] = {
        "sourceRows": len(rows),
        "skipped": [],
        "slugCollisions": [],
        "studentSlugCollisions": [],
        "duplicateNameIssues": [],
        "unmatchedAdviserNames": Counter(),
        "ambiguousFacultyMatches": [],
        "facultyMatches": [],
        "unmappedKeywords": Counter(),
        "blankTitles": 0,
        "blankYears": 0,
        "blankMainAdvisers": 0,
        "missingAbstracts": 0,
        "missingKeywords": 0,
    }

    for row in rows:
        source_row = int(row["_row"])
        title = normalize_space(row.get("Title"))
        year = parse_year(row.get("Year", ""))
        author_names = [normalize_space(row.get("Author 1")), normalize_space(row.get("Author 2"))]
        author_names = [name for name in author_names if name]
        author_names = [name for name in author_names if not is_blankish(name)]
        adviser = normalize_space(row.get("Main Adviser"))
        co_advisers = split_people(row.get("Co-advisers", ""))
        abstract = normalize_space(row.get("Abstract")) or None
        keywords = split_keywords(row.get("Key Words", ""))
        topics, unmapped = map_topics(keywords)
        for keyword in unmapped:
            audit["unmappedKeywords"][keyword] += 1

        if not title:
            audit["blankTitles"] += 1
        if year is None:
            audit["blankYears"] += 1
        if not adviser:
            audit["blankMainAdvisers"] += 1
        if not abstract:
            audit["missingAbstracts"] += 1
        if not keywords:
            audit["missingKeywords"] += 1

        if not title or not author_names:
            audit["skipped"].append({"row": source_row, "reason": "missing title or author"})
            continue
        if len(author_names) > 2:
            audit["skipped"].append({"row": source_row, "reason": "more than two undergraduate authors"})
            continue

        main_match = match_faculty(adviser, faculty_index) if adviser else FacultyMatch("", "")
        co_matches = [match_faculty(name, faculty_index) for name in co_advisers]
        all_matches = [main_match, *co_matches]
        for match in all_matches:
            if not match.original:
                continue
            audit["facultyMatches"].append(
                {
                    "source": match.original,
                    "normalized": match.normalized,
                    "match": match.slug,
                    "ambiguous": match.ambiguous,
                }
            )
            if match.ambiguous:
                audit["ambiguousFacultyMatches"].append(
                    {"row": source_row, "name": match.original, "candidates": match.ambiguous}
                )
            elif not match.slug:
                audit["unmatchedAdviserNames"][match.original] += 1

        main_faculty = main_match.slug
        co_faculty = [match.slug for match in co_matches if match.slug]
        if not main_faculty and not co_faculty:
            audit["skipped"].append({"row": source_row, "reason": "no EnviSAGE faculty main/co-adviser match"})
            continue

        base_slug = slugify(title)
        thesis_slug, collided = make_unique_slug(
            base_slug,
            used_thesis_slugs,
            f"{year or 'no-year'} {' '.join(author_names)} {title}",
        )
        if collided:
            audit["slugCollisions"].append({"row": source_row, "base": base_slug, "resolved": thesis_slug})

        student_slugs: list[str] = []
        for display_name in author_names:
            normalized = normalize_text(display_name)
            student = students_by_name.get(normalized)
            if student is None:
                base_student_slug = slugify(display_name)
                student_slug, student_collided = make_unique_slug(
                    base_student_slug,
                    used_person_slugs,
                    display_name,
                )
                if student_collided:
                    audit["studentSlugCollisions"].append(
                        {"row": source_row, "base": base_student_slug, "resolved": student_slug}
                    )
                student = Student(display_name, normalized, student_slug)
                students_by_name[normalized] = student
            elif student.display_name != display_name:
                audit["duplicateNameIssues"].append(
                    {
                        "normalized": normalized,
                        "kept": student.display_name,
                        "variant": display_name,
                        "row": source_row,
                    }
                )
            student.thesis_slugs.add(thesis_slug)
            if main_faculty:
                student.affiliated = True
            student_slugs.append(student.slug)

        basis = "main-adviser" if main_faculty else "co-adviser-only"
        adviser_roles = []
        if main_faculty:
            adviser_roles.append("main-adviser")
        if co_faculty:
            adviser_roles.append("co-adviser")

        theses.append(
            Thesis(
                source_row=source_row,
                year=year,
                title=title,
                slug=thesis_slug,
                students=author_names,
                student_people=student_slugs,
                adviser=adviser,
                main_adviser_person=main_faculty,
                co_advisers=co_advisers,
                co_adviser_people=co_faculty,
                abstract=abstract,
                keywords=keywords,
                research_topics=topics,
                envisage_associated=True,
                association_basis=basis,
                envisage_main_adviser=main_faculty,
                envisage_co_advisers=co_faculty,
                adviser_roles=adviser_roles,
            )
        )

    audit["unmatchedAdviserNames"] = dict(audit["unmatchedAdviserNames"].most_common())
    audit["unmappedKeywords"] = dict(audit["unmappedKeywords"].most_common())
    return theses, students_by_name, audit


def person_markdown(student: Student) -> str:
    roles = ["undergraduate-researcher", "alumni"] if student.affiliated else ["thesis-author"]
    categories = ["undergraduate-researcher", "alumni"] if student.affiliated else ["thesis-author"]
    lines = [
        "---",
        f"name: {yaml_scalar(student.display_name)}",
        f"slug: {student.slug}",
        f"importBatch: {IMPORT_BATCH}",
    ]
    lines.extend(yaml_slug_list("envisageRoles", roles))
    lines.extend(yaml_slug_list("categories", categories))
    lines.append(f"membershipStatus: {'alumni' if student.affiliated else 'inactive'}")
    lines.append('academicProgram: "BS Geodetic Engineering"')
    lines.extend(yaml_slug_list("researchAreas", []))
    lines.extend(yaml_slug_list("researchInterests", []))
    lines.extend(yaml_slug_list("researchTopics", []))
    lines.extend(yaml_slug_list("projects", []))
    lines.extend(yaml_slug_list("theses", []))
    lines.extend(yaml_slug_list("publications", []))
    lines.extend(yaml_slug_list("datasets", []))
    lines.extend(yaml_slug_list("tools", []))
    lines.extend(yaml_slug_list("grants", []))
    lines.extend(yaml_slug_list("studentResearch", sorted(student.thesis_slugs)))
    lines.append("visibility: internal")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def thesis_markdown(thesis: Thesis) -> str:
    lines = [
        "---",
        f"thesisTitle: {yaml_scalar(thesis.title)}",
        f"slug: {thesis.slug}",
        f"importBatch: {IMPORT_BATCH}",
        f"sourceRow: {thesis.source_row}",
        "thesisType: bs-geodetic-engineering-thesis",
        'program: "BS Geodetic Engineering"',
        "status: completed",
    ]
    lines.extend(yaml_list("students", thesis.students))
    lines.extend(yaml_slug_list("studentPeople", thesis.student_people))
    lines.append(f"adviser: {yaml_scalar(thesis.adviser)}")
    if thesis.main_adviser_person:
        lines.append(f"mainAdviserPerson: {thesis.main_adviser_person}")
    lines.extend(yaml_list("coAdvisers", thesis.co_advisers))
    lines.extend(yaml_slug_list("coAdviserPeople", thesis.co_adviser_people))
    if thesis.year is not None:
        lines.append(f"year: {thesis.year}")
    lines.extend(yaml_block("abstract", thesis.abstract))
    lines.extend(yaml_list("keywords", thesis.keywords))
    lines.extend(yaml_slug_list("researchTopics", thesis.research_topics))
    lines.extend(yaml_slug_list("researchAreas", []))
    lines.append("envisageAssociated: true")
    lines.append(f"envisageAssociationBasis: {thesis.association_basis}")
    if thesis.envisage_main_adviser:
        lines.append(f"envisageMainAdviser: {thesis.envisage_main_adviser}")
    lines.extend(yaml_slug_list("envisageCoAdvisers", thesis.envisage_co_advisers))
    lines.extend(yaml_slug_list("envisageAdviserRoles", thesis.adviser_roles))
    lines.extend(yaml_slug_list("projects", []))
    lines.extend(yaml_slug_list("publications", []))
    lines.extend(yaml_slug_list("datasets", []))
    lines.extend(yaml_slug_list("tools", []))
    lines.extend(yaml_slug_list("notebooks", []))
    lines.extend(yaml_slug_list("sampleData", []))
    lines.extend(yaml_slug_list("exampleOutputs", []))
    lines.extend(yaml_slug_list("mapsOrFigures", []))
    lines.append("reviewStatus: under-review")
    lines.append("visibility: internal")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def audit_markdown(source: Path, sheet_name: str, theses: list[Thesis], students: dict[str, Student], audit: dict[str, Any]) -> str:
    main_count = sum(1 for thesis in theses if thesis.association_basis == "main-adviser")
    co_only_count = sum(1 for thesis in theses if thesis.association_basis == "co-adviser-only")
    affiliated_students = sum(1 for student in students.values() if student.affiliated)
    non_affiliated_students = len(students) - affiliated_students
    one_author = sum(1 for thesis in theses if len(thesis.students) == 1)
    two_author = sum(1 for thesis in theses if len(thesis.students) == 2)
    faculty_matches = audit["facultyMatches"]
    unique_matches = sorted(
        {
            (item["source"], item["normalized"], item["match"] or "unmatched")
            for item in faculty_matches
            if item["match"]
        }
    )

    def bullet_dict(items: dict[str, Any], empty: str = "None") -> list[str]:
        if not items:
            return [f"- {empty}"]
        return [f"- {key}: {value}" for key, value in items.items()]

    def bullet_list(items: list[Any], empty: str = "None") -> list[str]:
        if not items:
            return [f"- {empty}"]
        return [f"- `{json.dumps(item, ensure_ascii=False)}`" for item in items[:100]]

    lines = [
        "# Undergraduate Thesis Import Audit 2026",
        "",
        "Status: Internal maintainer audit",
        "",
        "This audit summarizes the Phase 6C staging import. It intentionally does not reproduce the raw spreadsheet, full abstracts, or all row contents.",
        "",
        "## Source",
        "",
        f"- Source filename: `{source.name}`",
        f"- Source path: `{source}`",
        f"- Worksheet: `{sheet_name}`",
        f"- Import date: {date.today().isoformat()}",
        "- Source workbook copied into repository: No",
        "- Source workbook modified: No",
        "",
        "## Summary Counts",
        "",
        f"- Source thesis rows examined: {audit['sourceRows']}",
        f"- EnviSAGE-associated theses imported: {len(theses)}",
        f"- EnviSAGE Faculty as main adviser: {main_count}",
        f"- EnviSAGE Faculty as co-adviser only: {co_only_count}",
        f"- Total unique student authors: {len(students)}",
        f"- EnviSAGE-affiliated alumni: {affiliated_students}",
        f"- Associated but non-affiliated student authors: {non_affiliated_students}",
        f"- One-author theses: {one_author}",
        f"- Two-author theses: {two_author}",
        "",
        "## Faculty Match Audit",
        "",
    ]
    lines.extend(
        f"- {source_name} -> {match} (`{normalized}`)"
        for source_name, normalized, match in unique_matches
    )
    if not unique_matches:
        lines.append("- None")
    lines.extend(
        [
            "",
            "## QA Findings",
            "",
            f"- Blank titles: {audit['blankTitles']}",
            f"- Blank years: {audit['blankYears']}",
            f"- Blank main advisers: {audit['blankMainAdvisers']}",
            f"- Missing abstracts: {audit['missingAbstracts']}",
            f"- Missing keywords: {audit['missingKeywords']}",
            "",
            "### Duplicate-Name Issues",
            "",
        ]
    )
    lines.extend(bullet_list(audit["duplicateNameIssues"]))
    lines.extend(["", "### Thesis Slug Collisions", ""])
    lines.extend(bullet_list(audit["slugCollisions"]))
    lines.extend(["", "### Student Slug Collisions", ""])
    lines.extend(bullet_list(audit["studentSlugCollisions"]))
    lines.extend(["", "### Unmatched Adviser Names", ""])
    lines.extend(bullet_dict(audit["unmatchedAdviserNames"]))
    lines.extend(["", "### Ambiguous Faculty Matches", ""])
    lines.extend(bullet_list(audit["ambiguousFacultyMatches"]))
    lines.extend(["", "### Unmapped Keywords", ""])
    lines.extend(bullet_dict(audit["unmappedKeywords"]))
    lines.extend(["", "### Records Skipped", ""])
    lines.extend(bullet_list(audit["skipped"]))
    lines.extend(
        [
            "",
            "## Visibility Confirmation",
            "",
            "- All imported student Person records are `visibility: internal`.",
            "- All imported Student Research records are `visibility: internal`.",
            "- Imported records are a staging import and are not approved for publication.",
        ]
    )
    return "\n".join(lines) + "\n"


def validate(theses: list[Thesis], students: dict[str, Student]) -> list[str]:
    errors: list[str] = []
    thesis_slugs = [thesis.slug for thesis in theses]
    student_slugs = [student.slug for student in students.values()]
    if len(thesis_slugs) != len(set(thesis_slugs)):
        errors.append("Duplicate thesis slugs detected.")
    if len(student_slugs) != len(set(student_slugs)):
        errors.append("Duplicate student slugs detected.")
    for thesis in theses:
        if not thesis.students:
            errors.append(f"{thesis.slug}: no authors")
        if len(thesis.students) > 2:
            errors.append(f"{thesis.slug}: more than two BS thesis authors")
        if not thesis.title:
            errors.append(f"{thesis.slug}: blank title")
        if not thesis.adviser:
            errors.append(f"{thesis.slug}: blank main adviser")
        missing_people = [slug for slug in thesis.student_people if slug not in student_slugs]
        if missing_people:
            errors.append(f"{thesis.slug}: unresolved student person references {missing_people}")
        if thesis.association_basis == "main-adviser" and not thesis.envisage_main_adviser:
            errors.append(f"{thesis.slug}: main-adviser association without faculty slug")
        if thesis.association_basis == "co-adviser-only" and not thesis.envisage_co_advisers:
            errors.append(f"{thesis.slug}: co-adviser-only association without faculty slug")
    return errors


def write_outputs(source: Path, sheet_name: str, theses: list[Thesis], students: dict[str, Student], audit: dict[str, Any]) -> None:
    expected_people = {PEOPLE_DIR / f"{student.slug}.md" for student in students.values()}
    expected_theses = {THESIS_DIR / f"{thesis.slug}.md" for thesis in theses}
    for directory, expected in ((PEOPLE_DIR, expected_people), (THESIS_DIR, expected_theses)):
        for path in directory.glob("*.md"):
            if path in expected:
                continue
            if f"importBatch: {IMPORT_BATCH}" in path.read_text(encoding="utf-8"):
                path.unlink()

    for student in students.values():
        (PEOPLE_DIR / f"{student.slug}.md").write_text(person_markdown(student), encoding="utf-8")
    for thesis in theses:
        (THESIS_DIR / f"{thesis.slug}.md").write_text(thesis_markdown(thesis), encoding="utf-8")
    AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    AUDIT_PATH.write_text(audit_markdown(source, sheet_name, theses, students, audit), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Import EnviSAGE-associated undergraduate theses.")
    parser.add_argument("source", type=Path, help="Path to the source .xlsx workbook.")
    parser.add_argument("--sheet", default="Selected Advisers", help="Worksheet name to import.")
    parser.add_argument("--write", action="store_true", help="Write generated content and audit files.")
    args = parser.parse_args()

    if not args.source.exists():
        print(f"Source workbook not found: {args.source}", file=sys.stderr)
        return 1

    rows = read_sheet_rows(args.source, args.sheet)
    theses, students, audit = build_import(rows)
    errors = validate(theses, students)
    summary = {
        "source": str(args.source),
        "sheet": args.sheet,
        "rowsExamined": audit["sourceRows"],
        "thesesImported": len(theses),
        "mainAdvised": sum(1 for thesis in theses if thesis.association_basis == "main-adviser"),
        "coAdvisedOnly": sum(1 for thesis in theses if thesis.association_basis == "co-adviser-only"),
        "uniqueStudents": len(students),
        "affiliatedAlumni": sum(1 for student in students.values() if student.affiliated),
        "nonAffiliatedAuthors": sum(1 for student in students.values() if not student.affiliated),
        "oneAuthorTheses": sum(1 for thesis in theses if len(thesis.students) == 1),
        "twoAuthorTheses": sum(1 for thesis in theses if len(thesis.students) == 2),
        "blankTitles": audit["blankTitles"],
        "blankYears": audit["blankYears"],
        "blankMainAdvisers": audit["blankMainAdvisers"],
        "missingAbstracts": audit["missingAbstracts"],
        "missingKeywords": audit["missingKeywords"],
        "slugCollisions": len(audit["slugCollisions"]),
        "studentSlugCollisions": len(audit["studentSlugCollisions"]),
        "duplicateNameIssues": len(audit["duplicateNameIssues"]),
        "unmatchedAdviserNames": len(audit["unmatchedAdviserNames"]),
        "ambiguousFacultyMatches": len(audit["ambiguousFacultyMatches"]),
        "unmappedKeywords": len(audit["unmappedKeywords"]),
        "skipped": len(audit["skipped"]),
        "validationErrors": errors,
        "write": args.write,
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    if errors:
        return 1
    if args.write:
        write_outputs(args.source, args.sheet, theses, students, audit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
