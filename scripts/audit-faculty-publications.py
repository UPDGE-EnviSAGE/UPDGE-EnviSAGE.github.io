#!/usr/bin/env python3
"""Generate faculty publication QA review files and repository-only audits."""

from __future__ import annotations

import argparse
import csv
import importlib.util
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data-maintenance"
PUBLICATION_DIR = ROOT / "src" / "content" / "publications"
REVIEW_CSV = DATA_DIR / "faculty-publications-review.csv"
EXCEPTIONS_CSV = DATA_DIR / "faculty-publications-exceptions.csv"
MULTIFACULTY_CSV = DATA_DIR / "faculty-publications-multifaculty-review.csv"
DUPLICATES_CSV = DATA_DIR / "faculty-publications-duplicate-candidates.csv"
FACULTY_SUMMARY_CSV = DATA_DIR / "faculty-publications-faculty-summary.csv"
RECONCILIATION_CSV = DATA_DIR / "faculty-publications-deduplication-reconciliation.csv"
TAXONOMY_AUDIT_CSV = DATA_DIR / "faculty-publications-taxonomy-audit.csv"
MAINTENANCE_CSV = DATA_DIR / "faculty-publications.csv"
DEFAULT_SOURCE = (
    ROOT.parent
    / "imports"
    / "publications"
    / "EnviSAGE_Faculty_Publications_Verified_Source_Register_2026-08-18.csv"
)

REVIEW_FIELDS = [
    "publication_decision",
    "year",
    "title",
    "faculty",
    "authors_preview",
    "source_or_venue",
    "doi",
    "research_themes",
    "geomatics_approaches",
    "duplicate_status",
    "bibliographic_status",
    "review_notes",
    "publication_id",
]

MULTIFACULTY_FIELDS = [
    "publication_id",
    "year",
    "title",
    "faculty_count",
    "faculty",
    "authors_preview",
    "source_or_venue",
    "doi",
    "relationship_status",
    "review_notes",
]

MANUAL_DECISIONS = {"approve", "hold", "needs-fix"}


def load_sync_module():
    spec = importlib.util.spec_from_file_location(
        "sync_faculty_publications",
        ROOT / "scripts" / "sync-faculty-publications.py",
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load sync-faculty-publications.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SYNC = load_sync_module()
FACULTY_BY_SLUG = {slug: name for name, slug in SYNC.FACULTY_SLUGS.items()}
THEME_SLUGS = set(SYNC.THEME_SLUGS.values())
APPROACH_SLUGS = set(SYNC.APPROACH_SLUGS.values())


def split_pipe(value: str | None) -> list[str]:
    return [part for part in (value or "").split("|") if part]


def normalize_title(value: str | None) -> str:
    return SYNC.normalized_title(value or "")


def loose_title(value: str | None) -> str:
    return re.sub(r"[^a-z0-9]+", "", (value or "").casefold())


def normalize_doi(value: str | None) -> str:
    return re.sub(r"\s+", "", (value or "").strip()).lower()


def load_existing_decisions() -> dict[str, str]:
    if not REVIEW_CSV.exists():
        return {}
    with REVIEW_CSV.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    decisions: dict[str, str] = {}
    for row in rows:
        publication_id = (
            row.get("publication_id")
            or row.get("publicationId")
            or row.get("identifier")
            or ""
        ).strip()
        if not publication_id:
            continue
        decision = (row.get("publication_decision") or row.get("reviewDecision") or "").strip()
        if decision == "approve-public":
            decision = "approve"
        elif decision == "pending-review":
            decision = "pending-review"
        elif decision not in {"approve", "hold", "needs-fix"}:
            decision = "pending-review"
        decisions[publication_id] = decision
    return decisions


def read_maintenance_rows() -> list[dict[str, str]]:
    with MAINTENANCE_CSV.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def group_source_rows(source_rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    groups: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for index, row in enumerate(source_rows, start=1):
        row["_source_row"] = str(index)
        title = SYNC.clean(row.get("title_for_website")) or SYNC.clean(row.get("title_as_supplied"))
        year = SYNC.clean_year(row.get("year_for_website"))
        groups[(normalize_title(title), year)].append(row)

    by_rows: dict[str, list[dict[str, str]]] = {}
    for group in groups.values():
        key = ",".join(row["_source_row"] for row in group)
        by_rows[key] = group
    return by_rows


def source_support(group: list[dict[str, str]]) -> dict[str, object]:
    statuses = sorted({SYNC.clean(row.get("publication_review_status")) for row in group if SYNC.clean(row.get("publication_review_status"))})
    titles = {
        SYNC.clean(row.get("title_for_website")) or SYNC.clean(row.get("title_as_supplied"))
        for row in group
    }
    years = {SYNC.clean_year(row.get("year_for_website")) for row in group}
    dois = {normalize_doi(row.get("doi_for_website")) for row in group if normalize_doi(row.get("doi_for_website"))}
    doi_statuses = {
        SYNC.clean(row.get("doi_verification_status"))
        for row in group
        if normalize_doi(row.get("doi_for_website"))
    }
    return {
        "statuses": statuses,
        "ready": bool(statuses) and all(status.startswith("READY") for status in statuses),
        "title_count": len(titles),
        "year_count": len(years),
        "doi_count": len(dois),
        "doi_statuses": sorted(status for status in doi_statuses if status),
    }


def deduplication_rows(publications: list[dict[str, str]], source_groups: dict[str, list[dict[str, str]]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for publication in publications:
        group = source_groups.get(publication["sourceRows"], [])
        if len(group) <= 1:
            continue
        first_faculty = SYNC.clean(group[0].get("faculty"))
        seen_faculty: set[str] = {first_faculty} if first_faculty else set()
        canonical_source = group[0].get("_source_row", "")
        for source in group[1:]:
            faculty = SYNC.clean(source.get("faculty"))
            if faculty in seen_faculty:
                category = "A"
                reason = "Repeated title/year source row for a faculty already represented in the canonical record."
            elif faculty and faculty != first_faculty:
                category = "B"
                reason = "Same title/year record supports a multi-faculty relationship."
            else:
                category = "C"
                reason = "Same title/year row represented by the canonical publication record."
            seen_faculty.add(faculty)
            rows.append(
                {
                    "publication_id": publication["publicationId"],
                    "canonical_source_row": canonical_source,
                    "duplicate_source_row": source.get("_source_row", ""),
                    "deduplication_category": category,
                    "faculty": faculty,
                    "title": publication["title"],
                    "year": publication["year"],
                    "reason": reason,
                }
            )
    return rows


def duplicate_candidates(publications: list[dict[str, str]]) -> dict[str, str]:
    duplicate_status: dict[str, str] = {row["publicationId"]: "none" for row in publications}
    exact_groups: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    loose_groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for publication in publications:
        exact_groups[(normalize_title(publication["title"]), publication["year"])].append(publication)
        loose_groups[loose_title(publication["title"])].append(publication)

    for group in exact_groups.values():
        if len(group) > 1:
            for publication in group:
                duplicate_status[publication["publicationId"]] = "exact-duplicate"

    for group in loose_groups.values():
        if len(group) <= 1:
            continue
        years = {publication["year"] for publication in group}
        for publication in group:
            if duplicate_status[publication["publicationId"]] != "none":
                continue
            duplicate_status[publication["publicationId"]] = (
                "probable-duplicate" if len(years) == 1 else "possible-duplicate"
            )
    return duplicate_status


def build_audit(source_register: Path) -> dict[str, object]:
    source_rows = SYNC.read_rows(source_register)
    canonical, sync_audit = SYNC.canonicalize(source_rows)
    publications = read_maintenance_rows()
    source_groups = group_source_rows(source_rows)
    existing_decisions = load_existing_decisions()
    duplicate_statuses = duplicate_candidates(publications)

    review_rows: list[dict[str, str]] = []
    exceptions: list[dict[str, str]] = []
    multifaculty: list[dict[str, str]] = []
    taxonomy_rows: list[dict[str, str]] = []
    faculty_summary: dict[str, Counter[str]] = defaultdict(Counter)

    for publication in publications:
        publication_id = publication["publicationId"]
        faculty_slugs = split_pipe(publication["facultyRelationships"])
        faculty_names = [FACULTY_BY_SLUG.get(slug, slug) for slug in faculty_slugs]
        themes = split_pipe(publication["researchThemes"])
        approaches = split_pipe(publication["geomaticsApproaches"])
        group = source_groups.get(publication["sourceRows"], [])
        support = source_support(group)
        duplicate_status = duplicate_statuses[publication_id]
        reasons: list[str] = []

        if not support["ready"]:
            reasons.append("source status is not READY")
        if not publication["title"]:
            reasons.append("missing title_for_website support")
        if not publication["year"]:
            reasons.append("missing year_for_website support")
        if support["title_count"] > 1:
            reasons.append("conflicting source titles")
        if support["year_count"] > 1:
            reasons.append("conflicting source years")
        if support["doi_count"] > 1:
            reasons.append("conflicting DOI values")
        if duplicate_status != "none":
            reasons.append(f"unresolved {duplicate_status}")
        if not faculty_slugs:
            reasons.append("missing faculty relationship")
        if not publication["authors"]:
            reasons.append("missing author statement")
        if publication["doi"] and not re.fullmatch(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", publication["doi"], flags=re.I):
            reasons.append("implausible DOI format")

        invalid_themes = sorted(set(themes) - THEME_SLUGS)
        invalid_approaches = sorted(set(approaches) - APPROACH_SLUGS)
        taxonomy_note: list[str] = []
        if invalid_themes:
            taxonomy_note.append("invalid theme")
        if invalid_approaches:
            taxonomy_note.append("invalid approach")
        if not themes:
            taxonomy_note.append("no theme")
        if len(themes) > 1:
            taxonomy_note.append("multiple themes")
        if taxonomy_note:
            taxonomy_rows.append(
                {
                    "publication_id": publication_id,
                    "title": publication["title"],
                    "year": publication["year"],
                    "research_themes": "|".join(themes),
                    "geomatics_approaches": "|".join(approaches),
                    "taxonomy_status": "; ".join(taxonomy_note),
                    "review_notes": "",
                }
            )

        is_exception = bool(reasons)
        clean_note = "clean-for-review" if not is_exception else "; ".join(reasons)
        decision = existing_decisions.get(publication_id, "pending-review")
        if is_exception and decision not in MANUAL_DECISIONS:
            decision = "hold" if not support["ready"] else "pending-review"

        row = {
            "publication_decision": decision,
            "year": publication["year"],
            "title": publication["title"],
            "faculty": "|".join(faculty_names),
            "authors_preview": publication["authors"][:220],
            "source_or_venue": publication["sourceOrVenue"],
            "doi": publication["doi"],
            "research_themes": publication["researchThemes"],
            "geomatics_approaches": publication["geomaticsApproaches"],
            "duplicate_status": duplicate_status,
            "bibliographic_status": publication["bibliographicStatus"],
            "review_notes": clean_note,
            "publication_id": publication_id,
        }
        review_rows.append(row)

        if is_exception:
            exceptions.append(
                row
                | {
                    "exception_reasons": "; ".join(reasons),
                    "recommended_action": "keep held for source-register correction"
                    if not support["ready"]
                    else "review before any approval",
                }
            )

        if len(faculty_slugs) > 1:
            multifaculty.append(
                {
                    "publication_id": publication_id,
                    "year": publication["year"],
                    "title": publication["title"],
                    "faculty_count": str(len(faculty_slugs)),
                    "faculty": "|".join(faculty_names),
                    "authors_preview": publication["authors"][:220],
                    "source_or_venue": publication["sourceOrVenue"],
                    "doi": publication["doi"],
                    "relationship_status": "one-canonical-record-with-multiple-faculty-relationships",
                    "review_notes": "Verify public display credits the shared publication without duplicating records.",
                }
            )

        for faculty in faculty_names:
            faculty_summary[faculty]["canonical_publications"] += 1
            faculty_summary[faculty]["clean_for_review"] += 0 if is_exception else 1
            faculty_summary[faculty]["exceptions"] += 1 if is_exception else 0
            faculty_summary[faculty]["doi_bearing"] += 1 if publication["doi"] else 0
            faculty_summary[faculty]["multi_faculty"] += 1 if len(faculty_slugs) > 1 else 0
            faculty_summary[faculty]["source_linked_rows"] += len(group)

    duplicate_rows = []
    for status in ("exact-duplicate", "probable-duplicate", "possible-duplicate"):
        for publication in publications:
            if duplicate_statuses[publication["publicationId"]] == status:
                duplicate_rows.append(
                    {
                        "publication_id": publication["publicationId"],
                        "duplicate_status": status,
                        "year": publication["year"],
                        "title": publication["title"],
                        "faculty": "|".join(FACULTY_BY_SLUG.get(slug, slug) for slug in split_pipe(publication["facultyRelationships"])),
                        "doi": publication["doi"],
                        "review_notes": "Candidate only; do not auto-merge without maintainer review.",
                    }
                )

    no_duplicate_sentinel = {
        "publication_id": "",
        "duplicate_status": "not-duplicate",
        "year": "",
        "title": "",
        "faculty": "",
        "doi": "",
        "review_notes": "No exact, probable, or possible duplicate candidates found among canonical records by conservative title/year normalization.",
    }

    source_record_counter: Counter[str] = Counter()
    for source in source_rows:
        faculty = SYNC.clean(source.get("faculty"))
        if faculty:
            source_record_counter[faculty] += 1

    summary_rows = []
    for faculty in sorted(FACULTY_BY_SLUG.values()):
        summary_rows.append(
            {
                "faculty": faculty,
                "source_linked_records": str(source_record_counter[faculty]),
                "canonical_publications": str(faculty_summary[faculty]["canonical_publications"]),
                "clean_for_review": str(faculty_summary[faculty]["clean_for_review"]),
                "exceptions": str(faculty_summary[faculty]["exceptions"]),
                "doi_bearing": str(faculty_summary[faculty]["doi_bearing"]),
                "multi_faculty": str(faculty_summary[faculty]["multi_faculty"]),
            }
        )

    return {
        "sync_audit": sync_audit,
        "canonical": canonical,
        "review_rows": review_rows,
        "exceptions": exceptions,
        "multifaculty": multifaculty,
        "duplicates": duplicate_rows or [no_duplicate_sentinel],
        "duplicate_candidate_count": len(duplicate_rows),
        "faculty_summary": summary_rows,
        "reconciliation": deduplication_rows(publications, source_groups),
        "taxonomy_rows": taxonomy_rows,
    }


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def privacy_audit() -> int:
    dist = ROOT / "dist"
    if not dist.exists():
        print("privacy_audit=missing_dist")
        return 1
    forbidden = [
        "READY",
        "REVIEW -",
        "HOLD -",
        "bibliographicStatus",
        "sourceProvenance",
        "internalNotes",
        "source rows",
        "canonical publication",
        "duplicate",
        "import count",
        "verification count",
    ]
    hits: list[str] = []
    for path in dist.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".html", ".js", ".css", ".json"}:
            text = path.read_text(encoding="utf-8", errors="ignore")
            for token in forbidden:
                if token in text:
                    hits.append(f"{path.relative_to(dist)}:{token}")
    maintenance_hits = [path for path in dist.rglob("*") if "faculty-publications" in path.name]
    if hits or maintenance_hits:
        print(f"privacy_audit=fail hits={hits} maintenance_files={[str(path.relative_to(dist)) for path in maintenance_hits]}")
        return 1
    print("privacy_audit=pass")
    return 0


def broken_link_audit() -> int:
    dist = ROOT / "dist"
    if not dist.exists():
        print("broken_link_audit=missing_dist")
        return 1
    html_files = list(dist.rglob("*.html"))
    hrefs: set[str] = set()
    for path in html_files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        hrefs.update(re.findall(r'href="([^"#][^"]*)"', text))
    missing: list[str] = []
    for href in sorted(hrefs):
        if href.startswith(("http://", "https://", "mailto:", "tel:")):
            continue
        target = href.split("?", 1)[0]
        if not target.startswith("/"):
            continue
        candidate = dist / target.lstrip("/")
        if target.endswith("/"):
            ok = (candidate / "index.html").exists()
        elif candidate.suffix:
            ok = candidate.exists()
        else:
            ok = (candidate / "index.html").exists() or candidate.exists()
        if not ok:
            missing.append(target)
    if missing:
        print(f"broken_link_audit=fail missing={missing}")
        return 1
    print(f"broken_link_audit=pass checked_internal_hrefs={len(hrefs)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-register", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--write", action="store_true", help="Write QA maintenance CSVs.")
    parser.add_argument("--privacy-audit", action="store_true", help="Audit built public files for maintenance metadata.")
    parser.add_argument("--broken-link-audit", action="store_true", help="Audit built internal links.")
    args = parser.parse_args()

    exit_code = 0
    if args.privacy_audit:
        exit_code |= privacy_audit()
    if args.broken_link_audit:
        exit_code |= broken_link_audit()
    if args.privacy_audit or args.broken_link_audit:
        return exit_code

    audit = build_audit(args.source_register)
    review_rows = audit["review_rows"]
    exceptions = audit["exceptions"]
    print(f"canonical_publications={len(review_rows)}")
    print(f"clean_for_review={sum(1 for row in review_rows if row['review_notes'] == 'clean-for-review')}")
    print(f"exceptions={len(exceptions)}")
    print(f"multi_faculty_records={len(audit['multifaculty'])}")
    print(f"duplicate_candidates={audit['duplicate_candidate_count']}")
    print(f"taxonomy_review_rows={len(audit['taxonomy_rows'])}")
    print(f"write={'complete' if args.write else 'dry-run'}")

    if args.write:
        write_csv(REVIEW_CSV, REVIEW_FIELDS, audit["review_rows"])
        write_csv(EXCEPTIONS_CSV, REVIEW_FIELDS + ["exception_reasons", "recommended_action"], audit["exceptions"])
        write_csv(MULTIFACULTY_CSV, MULTIFACULTY_FIELDS, audit["multifaculty"])
        write_csv(
            DUPLICATES_CSV,
            ["publication_id", "duplicate_status", "year", "title", "faculty", "doi", "review_notes"],
            audit["duplicates"],
        )
        write_csv(
            FACULTY_SUMMARY_CSV,
            [
                "faculty",
                "source_linked_records",
                "canonical_publications",
                "clean_for_review",
                "exceptions",
                "doi_bearing",
                "multi_faculty",
            ],
            audit["faculty_summary"],
        )
        write_csv(
            RECONCILIATION_CSV,
            [
                "publication_id",
                "canonical_source_row",
                "duplicate_source_row",
                "deduplication_category",
                "faculty",
                "title",
                "year",
                "reason",
            ],
            audit["reconciliation"],
        )
        write_csv(
            TAXONOMY_AUDIT_CSV,
            [
                "publication_id",
                "title",
                "year",
                "research_themes",
                "geomatics_approaches",
                "taxonomy_status",
                "review_notes",
            ],
            audit["taxonomy_rows"],
        )

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
