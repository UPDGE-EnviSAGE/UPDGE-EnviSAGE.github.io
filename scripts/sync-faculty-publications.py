#!/usr/bin/env python3
"""Import the verified faculty publication register into reviewable site files."""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = (
    ROOT.parent
    / "imports"
    / "publications"
    / "EnviSAGE_Faculty_Publications_Verified_Source_Register_2026-08-18.csv"
)
PUBLICATION_DIR = ROOT / "src" / "content" / "publications"
MAINTENANCE_CSV = ROOT / "data-maintenance" / "faculty-publications.csv"
REVIEW_CSV = ROOT / "data-maintenance" / "faculty-publications-review.csv"
IMPORT_DOC = ROOT / "docs" / "imports" / "FACULTY_PUBLICATIONS_IMPORT_2026.md"

FACULTY_SLUGS = {
    "Ariel C. Blanco": "ariel-c-blanco",
    "Ayin M. Tamondong": "ayin-m-tamondong",
    "Jommer M. Medina": "jommer-m-medina",
    "Erica Erin E. Elazegui": "erica-erin-e-elazegui",
    "Margaux Angelica A. Cruz": "margaux-angelica-a-cruz",
    "John Emmanuel D. Escoto": "john-emmanuel-d-escoto",
}

THEME_SLUGS = {
    "Coastal & Marine Systems": "coastal-marine-systems",
    "Ecosystems, Biodiversity & Land Change": "ecosystems-biodiversity-land-change",
    "Water, Air & Environmental Quality": "water-air-environmental-quality",
    "Climate, Hazards & Resilience": "climate-hazards-resilience",
    "Urban & Sustainable Systems": "urban-sustainable-systems",
}

APPROACH_SLUGS = {
    "Earth Observation & Remote Sensing": "earth-observation-remote-sensing",
    "GIS & Spatial Analytics": "gis-spatial-analytics",
    "GeoAI & Spatial Data Science": "geoai-spatial-data-science",
    "LiDAR, Photogrammetry & 3D Geomatics": "lidar-photogrammetry-3d-geomatics",
    "Environmental & Spatial Modeling": "environmental-spatial-modeling",
    "Geovisualization & Decision Support": "geovisualization-decision-support",
}


def clean(value: str | None) -> str:
    return re.sub(r"\s+", " ", (value or "").strip())


def clean_year(value: str | None) -> str:
    value = clean(value)
    if not value:
        return ""
    if re.fullmatch(r"\d+(?:\.0+)?", value):
        return str(int(float(value)))
    return value


def slugify(value: str) -> str:
    value = value.casefold()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return re.sub(r"-+", "-", value).strip("-") or "publication"


def normalized_title(value: str) -> str:
    return clean(value).casefold()


def split_mapped(value: str, mapping: dict[str, str]) -> tuple[list[str], list[str]]:
    slugs: list[str] = []
    unmapped: list[str] = []
    for item in [clean(part) for part in re.split(r"[;|]", value or "")]:
        if not item:
            continue
        if item in mapping:
            slugs.append(mapping[item])
        else:
            unmapped.append(item)
    return sorted(set(slugs)), sorted(set(unmapped))


def yaml_scalar(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def yaml_list(name: str, values: list[str]) -> list[str]:
    if not values:
        return [f"{name}: []"]
    return [f"{name}:"] + [f"  - {yaml_scalar(value)}" for value in values]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def canonicalize(rows: list[dict[str, str]]) -> tuple[list[dict[str, object]], dict[str, object]]:
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for index, row in enumerate(rows, start=1):
        row["_source_row"] = str(index)
        title = clean(row.get("title_for_website")) or clean(row.get("title_as_supplied"))
        year = clean_year(row.get("year_for_website"))
        grouped[(normalized_title(title), year)].append(row)

    used_ids: Counter[str] = Counter()
    publications: list[dict[str, object]] = []
    for (norm_title, year), group in sorted(grouped.items(), key=lambda item: (item[0][1], item[0][0])):
        first = group[0]
        title = clean(first.get("title_for_website")) or clean(first.get("title_as_supplied"))
        base = slugify("-".join(part for part in [title, year] if part))
        digest = hashlib.sha1(f"{norm_title}|{year}".encode("utf-8")).hexdigest()[:8]
        publication_id = f"{base[:78].strip('-')}-{digest}"
        used_ids[publication_id] += 1
        if used_ids[publication_id] > 1:
            publication_id = f"{publication_id}-{used_ids[publication_id]}"

        faculty_slugs = sorted(
            {
                FACULTY_SLUGS[clean(row.get("faculty"))]
                for row in group
                if clean(row.get("faculty")) in FACULTY_SLUGS
            }
        )
        themes: set[str] = set()
        approaches: set[str] = set()
        unmapped: list[str] = []
        for row in group:
            row_themes, row_unmapped_themes = split_mapped(row.get("research_theme_inference", ""), THEME_SLUGS)
            row_approaches, row_unmapped_approaches = split_mapped(row.get("method_inference", ""), APPROACH_SLUGS)
            themes.update(row_themes)
            approaches.update(row_approaches)
            unmapped.extend([f"theme:{item}" for item in row_unmapped_themes])
            unmapped.extend([f"approach:{item}" for item in row_unmapped_approaches])

        statuses = sorted({clean(row.get("publication_review_status")) for row in group if clean(row.get("publication_review_status"))})
        ready = all(status.startswith("READY") for status in statuses)
        doi = next((clean(row.get("doi_for_website")) for row in group if clean(row.get("doi_for_website"))), "")
        doi_status = next((clean(row.get("doi_verification_status")) for row in group if clean(row.get("doi_for_website"))), "")
        bibliography_status = "verified" if doi_status == "online-primary-verified" else "source-supported"
        if not ready:
            bibliography_status = "needs-review"

        notes = []
        if len(group) > 1:
            notes.append(f"Deduplicated from {len(group)} identical title/year source rows.")
        if unmapped:
            notes.append("Unmapped taxonomy terms: " + "; ".join(sorted(set(unmapped))))
        if not ready:
            notes.append("Source review status: " + "; ".join(statuses))

        publications.append(
            {
                "publicationId": publication_id,
                "title": title,
                "year": year,
                "authors": [clean(first.get("authors_as_supplied"))] if clean(first.get("authors_as_supplied")) else [],
                "sourceOrVenue": clean(first.get("source_or_venue_as_supplied")),
                "publicationType": "other",
                "doi": doi,
                "url": f"https://doi.org/{doi}" if doi else "",
                "facultyRelationships": faculty_slugs,
                "researchThemes": sorted(themes),
                "geomaticsApproaches": sorted(approaches),
                "visibility": "internal",
                "bibliographicStatus": bibliography_status,
                "sourceProvenance": "; ".join(sorted({clean(row.get("provenance")) for row in group if clean(row.get("provenance"))})),
                "internalNotes": " ".join(notes),
                "sourceRows": ",".join(row["_source_row"] for row in group),
                "sourceReviewStatuses": "; ".join(statuses),
                "reviewDecision": "pending-review" if ready else "hold",
            }
        )

    audit = {
        "source_rows": len(rows),
        "canonical_publications": len(publications),
        "ready_rows": sum(1 for row in rows if clean(row.get("publication_review_status")).startswith("READY")),
        "review_or_hold_rows": sum(1 for row in rows if not clean(row.get("publication_review_status")).startswith("READY")),
        "doi_total": sum(1 for row in rows if clean(row.get("doi_for_website"))),
        "doi_by_status": Counter(clean(row.get("doi_verification_status")) or "(blank)" for row in rows if clean(row.get("doi_for_website"))),
        "duplicate_groups": sum(1 for group in grouped.values() if len(group) > 1),
        "deduplicated_rows": sum(len(group) for group in grouped.values() if len(group) > 1),
        "hold_publications": sum(1 for publication in publications if publication["reviewDecision"] == "hold"),
    }
    return publications, audit


def write_publication(publication: dict[str, object]) -> None:
    path = PUBLICATION_DIR / f"{publication['publicationId']}.md"
    lines = ["---"]
    for field in ["title", "publicationId", "identifier"]:
        value = publication["publicationId"] if field == "identifier" else publication[field]
        lines.append(f"{field}: {yaml_scalar(str(value))}")
    lines.extend(yaml_list("authors", publication["authors"]))  # type: ignore[arg-type]
    if publication["year"]:
        lines.append(f"year: {publication['year']}")
    lines.append(f"publicationType: {publication['publicationType']}")
    if publication["sourceOrVenue"]:
        lines.append(f"sourceOrVenue: {yaml_scalar(str(publication['sourceOrVenue']))}")
        lines.append(f"venue: {yaml_scalar(str(publication['sourceOrVenue']))}")
    if publication["doi"]:
        lines.append(f"doi: {publication['doi']}")
    if publication["url"]:
        lines.append(f"url: {publication['url']}")
    lines.extend(yaml_list("facultyRelationships", publication["facultyRelationships"]))  # type: ignore[arg-type]
    lines.extend(yaml_list("researchThemes", publication["researchThemes"]))  # type: ignore[arg-type]
    lines.extend(yaml_list("geomaticsApproaches", publication["geomaticsApproaches"]))  # type: ignore[arg-type]
    lines.append("projects: []")
    lines.append("datasets: []")
    lines.append("tools: []")
    lines.append("keywords: []")
    lines.append(f"visibility: {publication['visibility']}")
    lines.append(f"bibliographicStatus: {publication['bibliographicStatus']}")
    if publication["sourceProvenance"]:
        lines.append(f"sourceProvenance: {yaml_scalar(str(publication['sourceProvenance']))}")
    if publication["internalNotes"]:
        lines.append(f"internalNotes: {yaml_scalar(str(publication['internalNotes']))}")
    lines.append("---")
    lines.append("")
    lines.append(
        "This internal publication record was generated from the verified Phase 6F source register and remains excluded from public pages until maintainer approval."
    )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_csvs(publications: list[dict[str, object]], audit: dict[str, object]) -> None:
    MAINTENANCE_CSV.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "publicationId",
        "title",
        "year",
        "authors",
        "sourceOrVenue",
        "publicationType",
        "doi",
        "url",
        "facultyRelationships",
        "researchThemes",
        "geomaticsApproaches",
        "visibility",
        "bibliographicStatus",
        "sourceProvenance",
        "internalNotes",
        "sourceRows",
        "sourceReviewStatuses",
    ]
    with MAINTENANCE_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for publication in publications:
            writer.writerow({field: "|".join(publication[field]) if isinstance(publication[field], list) else publication[field] for field in fields})

    review_fields = [
        "publicationId",
        "title",
        "year",
        "facultyRelationships",
        "reviewDecision",
        "visibilityAfterPublish",
        "reviewNotes",
    ]
    with REVIEW_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=review_fields)
        writer.writeheader()
        for publication in publications:
            writer.writerow(
                {
                    "publicationId": publication["publicationId"],
                    "title": publication["title"],
                    "year": publication["year"],
                    "facultyRelationships": "|".join(publication["facultyRelationships"]),  # type: ignore[arg-type]
                    "reviewDecision": publication["reviewDecision"],
                    "visibilityAfterPublish": "internal",
                    "reviewNotes": publication["internalNotes"],
                }
            )

    IMPORT_DOC.parent.mkdir(parents=True, exist_ok=True)
    doi_status = audit["doi_by_status"]
    IMPORT_DOC.write_text(
        "\n".join(
            [
                "# Faculty Publications Import 2026",
                "",
                "Status: Phase 6F import audit",
                "",
                "The verified source register supplied by the maintainer is the authoritative source for this import. The workflow does not use web lookup and does not infer missing bibliographic metadata.",
                "",
                f"- Source rows: {audit['source_rows']}",
                f"- READY rows: {audit['ready_rows']}",
                f"- REVIEW/HOLD rows: {audit['review_or_hold_rows']}",
                f"- Canonical publication records after exact title/year deduplication: {audit['canonical_publications']}",
                f"- Duplicate title/year groups: {audit['duplicate_groups']}",
                f"- Source rows represented in duplicate groups: {audit['deduplicated_rows']}",
                f"- DOI values retained: {audit['doi_total']}",
                f"- DOI values marked online-primary-verified: {doi_status.get('online-primary-verified', 0)}",
                f"- DOI values marked user-supplied-SUKAT: {doi_status.get('user-supplied-SUKAT', 0)}",
                f"- Canonical records held from public review because at least one source row is REVIEW/HOLD: {audit['hold_publications']}",
                "",
                "All imported records default to `visibility: internal`. Maintainers must update `data-maintenance/faculty-publications-review.csv` and run the publish script before any record can become public.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-register", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--write", action="store_true", help="Write maintenance CSVs and generated publication content.")
    args = parser.parse_args()

    rows = read_rows(args.source_register)
    publications, audit = canonicalize(rows)
    print(f"source_rows={audit['source_rows']}")
    print(f"ready_rows={audit['ready_rows']}")
    print(f"review_or_hold_rows={audit['review_or_hold_rows']}")
    print(f"canonical_publications={audit['canonical_publications']}")
    print(f"doi_total={audit['doi_total']}")
    print(f"doi_by_status={dict(audit['doi_by_status'])}")
    print(f"duplicate_groups={audit['duplicate_groups']}")
    print(f"deduplicated_rows={audit['deduplicated_rows']}")
    print(f"hold_publications={audit['hold_publications']}")
    if args.write:
        PUBLICATION_DIR.mkdir(parents=True, exist_ok=True)
        for publication in publications:
            write_publication(publication)
        write_csvs(publications, audit)
        print("write=complete")
    else:
        print("write=dry-run")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
