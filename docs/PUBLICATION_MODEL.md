# Publication Model

Status: Canonical Phase 6F.1 publication workflow

Publications are independent scholarly records. A publication may be related to multiple EnviSAGE faculty members, Research Themes, Geomatics Approaches, projects, theses, datasets, or tools.

## Source Authority

The Phase 6F faculty publication import uses the verified source register supplied by the maintainer:

`EnviSAGE_Faculty_Publications_Verified_Source_Register_2026-08-18.csv`

Do not use web lookup to complete missing bibliographic fields during this import. Use only `title_for_website`, `year_for_website`, and `doi_for_website` for public-facing title, year, and DOI values. If an approved field is blank in the source register, leave it blank in the imported record.

## Canonical Record Rule

Create one canonical Publication record per publication. Faculty publication lists must be generated from relationships, not from duplicate per-faculty publication copies.

Deduplicate only when normalized full title and compatible year match. Do not merge near matches, truncated titles, or ambiguous records.

## Visibility

Imported faculty publication records default to `visibility: internal`.

Public pages and faculty profiles must render only `visibility: public` publication records. Internal fields such as `bibliographicStatus`, `sourceProvenance`, and `internalNotes` are maintainer fields and must not appear on public pages.

At Phase 6F.1 completion, all newly imported faculty publication records remain internal. Public display requires an explicit maintainer review decision followed by the publication script.

## Maintainer Workflow

1. Run `python3 scripts/sync-faculty-publications.py` to audit the source register without writing.
2. Run `python3 scripts/sync-faculty-publications.py --write` only when the import audit is expected.
3. Run `python3 scripts/audit-faculty-publications.py --write` to regenerate review, exceptions, duplicate, multi-faculty, taxonomy, and faculty-summary QA files.
4. Review `data-maintenance/faculty-publications-review.csv` and `data-maintenance/faculty-publications-exceptions.csv`.
5. Mark records for publication only with `publication_decision: approve`. Leave exceptions as `hold`, `needs-fix`, or `pending-review` until corrected.
6. Run `python3 scripts/review-faculty-publications.py --approve-clean` to dry-run bulk approval of clean records.
7. Run `python3 scripts/review-faculty-publications.py --approve-clean --write` only when the maintainer has approved the clean set.
8. Run `python3 scripts/publish-faculty-publications.py` to dry-run publication.
9. Run `python3 scripts/publish-faculty-publications.py --write` only after review.

The public `/publications/` route is production-capable but intentionally empty until maintainers approve records.

## Review Fields

The primary review CSV starts with these fields:

`publication_decision`, `year`, `title`, `faculty`, `authors_preview`, `source_or_venue`, `doi`, `research_themes`, `geomatics_approaches`, `duplicate_status`, `bibliographic_status`, `review_notes`, `publication_id`

The supported decisions are:

- `pending-review` - default for clean records awaiting maintainer review.
- `approve` - explicit maintainer approval for public publication.
- `hold` - keep out of public workflows.
- `needs-fix` - requires source or content correction before reconsideration.

The bulk approval helper never approves records listed in the exceptions CSV and preserves existing `approve`, `hold`, and `needs-fix` decisions.
