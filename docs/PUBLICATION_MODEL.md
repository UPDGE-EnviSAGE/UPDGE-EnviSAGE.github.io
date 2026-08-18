# Publication Model

Status: Canonical Phase 6F publication workflow

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

## Maintainer Workflow

1. Run `python3 scripts/sync-faculty-publications.py` to audit the source register without writing.
2. Run `python3 scripts/sync-faculty-publications.py --write` only when the audit is expected.
3. Review `data-maintenance/faculty-publications-review.csv`.
4. Mark records for publication only with `reviewDecision: approve-public` and `visibilityAfterPublish: public`.
5. Run `python3 scripts/review-faculty-publications.py` to summarize decisions.
6. Run `python3 scripts/publish-faculty-publications.py` to dry-run publication.
7. Run `python3 scripts/publish-faculty-publications.py --write` only after review.

At Phase 6F completion, all imported records remain internal. The public `/publications/` route is production-capable but intentionally empty until maintainers approve records.
