# Faculty Publication Review Guide

Status: Phase 6F.1 maintainer workflow

This guide controls the review and publication workflow for the imported faculty publication records. It uses only the maintainer-supplied verified source register and repository-managed QA files. Do not use web lookup, bibliographic databases, or inferred metadata to complete blank fields during this review.

## Review Files

- `data-maintenance/faculty-publications-review.csv` is the primary clean-publication review set.
- `data-maintenance/faculty-publications-exceptions.csv` lists records that require specific attention before approval.
- `data-maintenance/faculty-publications-multifaculty-review.csv` audits publications related to more than one faculty member.
- `data-maintenance/faculty-publications-duplicate-candidates.csv` lists exact, probable, possible, or not-duplicate duplicate findings.
- `data-maintenance/faculty-publications-faculty-summary.csv` summarizes repository-only QA counts by faculty.
- `data-maintenance/faculty-publications-deduplication-reconciliation.csv` explains how exact title/year source rows collapse into canonical publication records.
- `data-maintenance/faculty-publications-taxonomy-audit.csv` lists taxonomy records needing review, including no-theme and multiple-theme cases.

These files are maintenance assets only. They must not be copied into `public/`, linked as public downloads, or exposed in `dist/`.

## Safe Review Commands

Run the source import in dry-run mode:

```sh
python3 scripts/sync-faculty-publications.py
```

Regenerate QA files after source or canonical record changes:

```sh
python3 scripts/audit-faculty-publications.py --write
```

Summarize review decisions:

```sh
python3 scripts/review-faculty-publications.py
```

Preview clean-record approval without writing:

```sh
python3 scripts/review-faculty-publications.py --approve-clean
```

Apply clean-record approval only after maintainer review:

```sh
python3 scripts/review-faculty-publications.py --approve-clean --write
```

Preview publication:

```sh
python3 scripts/publish-faculty-publications.py
```

Publish approved records only after final review:

```sh
python3 scripts/publish-faculty-publications.py --write
```

## Approval Rules

Only `publication_decision: approve` can make an imported faculty publication eligible for public visibility.

Do not approve a record if it appears in `faculty-publications-exceptions.csv` unless the exception has been resolved and the QA file has been regenerated.

The bulk approval helper:

- Approves only clean records when `--approve-clean --write` is used.
- Never approves exceptions.
- Preserves existing `approve`, `hold`, and `needs-fix` decisions.
- Defaults to dry-run output unless `--write` is present.

## Exception Handling

The current exception set includes records with unresolved source status, missing year support, conflicting source titles, or conservative duplicate candidates. Keep these out of public pages until the source register or canonical record has been reviewed by a maintainer.

DOI is not required. Venue is not required. Blank fields must remain blank unless supported by the source register.

## Public Display

Public pages may show only:

- title
- authors
- year grouping
- source or venue when available
- DOI link when available
- reliable URL when available

Public pages must not show source-review statuses, import counts, READY/REVIEW/HOLD labels, duplicate counts, verification counts, `bibliographicStatus`, `sourceProvenance`, or `internalNotes`.
