# Publication Model

Status: Canonical Phase 6F.2 publication workflow

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

At Phase 6F.2 completion, the 289 clean records explicitly approved by maintainers are public. The 10 exception records remain non-public until later review.

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

The public `/publications/` route renders approved publications in a minimalist scholarly discovery experience. The overview metrics, publications-through-time chart, Research Theme distribution, search results, filter counts, and year groups must be computed from public publication data at build time.

Search may use public-safe page data: title, author text, displayed source or venue, year, faculty relationship labels, and approved Research Theme labels. It must not search or serialize review notes, provenance, publication IDs, bibliographic status, duplicate status, maintenance fields, or publication decisions.

The catalog remains the authoritative scholarly list. It groups publications by year with native disclosure controls: the newest year is open by default, older years are collapsed by default, and active search or filters open matching year groups while hiding empty groups.

Citation metrics and word clouds are not part of the Phase 6H public publication model. Do not add citation counts, h-index, i10-index, most-cited rankings, or keyword-frequency visualizations until a future approved source and methodology is supplied.

Venue display should be conservative. Use existing `sourceOrVenue` text when it is usable as displayed. Truncated but meaningful strings may be displayed honestly. Blank values, no-title placeholders, and values that repeat the publication title should be omitted from public display while preserved in canonical content for later bibliographic correction. The venue display-quality audit is emitted to `data-maintenance/publication-venue-display-audit.csv`.

## Review Fields

The primary review CSV starts with these fields:

`publication_decision`, `year`, `title`, `faculty`, `authors_preview`, `source_or_venue`, `doi`, `research_themes`, `geomatics_approaches`, `duplicate_status`, `bibliographic_status`, `review_notes`, `publication_id`

The supported decisions are:

- `pending-review` - default for clean records awaiting maintainer review.
- `approve` - explicit maintainer approval for public publication.
- `hold` - keep out of public workflows.
- `needs-fix` - requires source or content correction before reconsideration.

The bulk approval helper never approves records listed in the exceptions CSV and preserves existing `approve`, `hold`, and `needs-fix` decisions.
