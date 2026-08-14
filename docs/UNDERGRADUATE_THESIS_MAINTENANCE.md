# Undergraduate Thesis Maintenance Guide

Status: Internal maintainer workflow

This guide explains how EnviSAGE maintainers can add and update undergraduate thesis records without manually editing many individual content files.

All student and thesis records managed by this workflow remain internal in this phase. Public publication is separate review work.

## Purpose

The website keeps canonical records in:

- `src/content/people/`
- `src/content/student-research/`

Maintainers edit one CSV:

```text
data-maintenance/undergraduate-theses.csv
```

Then the sync script validates the CSV and updates the canonical records.

## Workflow

Changes should flow in one direction:

```text
Maintainer CSV -> validated sync -> canonical records -> website
```

Do not treat the CSV as a separate database. It is a controlled editing layer for the canonical website records.

If a canonical file must be edited manually for an exceptional case, update the CSV afterward so the next sync does not reintroduce stale data.

## CSV Columns

- `record_id`: Stable record identifier, such as `bsge-2026-001`. Do not change it after a row is created.
- `academic_year`: Thesis year, normally a four-digit year.
- `thesis_status`: `ongoing`, `completed`, or `archived`.
- `thesis_title`: Working or final thesis title.
- `student_1`: First student author.
- `student_2`: Second student author, blank for a one-student thesis.
- `student_1_program`: Usually `BS Geodetic Engineering`.
- `student_2_program`: Usually `BS Geodetic Engineering` when `student_2` is present.
- `student_1_membership_status`: Human review note; sync derives canonical membership from adviser and thesis status.
- `student_2_membership_status`: Human review note for the second student.
- `main_adviser`: Main adviser display name.
- `co_advisers`: Co-advisers separated with semicolons where possible.
- `abstract`: Abstract text when available. Leave blank if not yet reviewed or not available.
- `keywords`: Keywords separated with semicolons.
- `visibility`: Keep `internal` unless a future publication phase approves otherwise.
- `review_status`: Use `pending-review` for maintainer review. The sync maps this into valid canonical review states.
- `review_notes`: Free-text notes for maintainers.
- `github_url`: Optional reviewed GitHub repository URL. Ongoing thesis repositories normally remain private.
- `related_project_slug`: Optional future relationship to an EnviSAGE project.
- `publication_notes`: Optional notes about related publications.
- `dataset_notes`: Optional notes about related datasets.
- `software_notes`: Optional notes about related software.
- `sync_action`: Leave blank. Use `exclude` only when a row should be skipped intentionally.

## Record IDs

Historical records use deterministic IDs derived from the source year and row order, for example:

```text
bsge-2022-072
```

For new records, use a simple yearly sequence:

```text
bsge-2026-001
bsge-2026-002
```

The `record_id` is the identity key. Slugs are generated from titles and names and should not be invented manually.

## Add An Ongoing Thesis

Add one row to `data-maintenance/undergraduate-theses.csv`:

```csv
record_id,academic_year,thesis_status,thesis_title,student_1,student_2,main_adviser,co_advisers,abstract,keywords,visibility,review_status,review_notes
bsge-2026-001,2026,ongoing,Working title for water quality mapping,"Student, One A.","Student, Two B.","TAMONDONG, Ayin M.","","",water quality; remote sensing,internal,pending-review,Initial private record
```

Run a dry-run first:

```sh
python3 scripts/sync-undergraduate-theses.py data-maintenance/undergraduate-theses.csv
```

Review warnings and errors. Apply changes only when the output is expected:

```sh
python3 scripts/sync-undergraduate-theses.py data-maintenance/undergraduate-theses.csv --write
```

## Add A Two-Student Thesis

Use one row with both `student_1` and `student_2`.

Do not create two thesis records for a pair thesis.

## Update A Thesis

Edit the existing row with the same `record_id`.

Common updates include:

- title
- main adviser
- co-advisers
- abstract
- keywords
- review notes

Run the dry-run again. The sync updates the existing canonical thesis rather than creating a duplicate.

## Mark A Thesis Completed

Change:

```text
thesis_status: ongoing
```

to:

```text
thesis_status: completed
```

Then update final title, academic year, abstract, and keywords if available.

If the main adviser is EnviSAGE faculty, the sync changes affiliated students from active undergraduate researchers to alumni.

## Add A Newly Graduated Historical Thesis

Add a completed row directly:

```csv
record_id,academic_year,thesis_status,thesis_title,student_1,student_2,main_adviser,co_advisers,abstract,keywords,visibility,review_status,review_notes
bsge-2026-002,2026,completed,Final thesis title,"Student, One A.","","BLANCO, Ariel C.","","Reviewed abstract text.",remote sensing; GIS,internal,pending-review,Newly graduated record
```

The sync creates or updates:

- one Student Research record
- one or two canonical student Person records
- alumni status when the main adviser is EnviSAGE faculty

## Adviser Affiliation Rule

If the main adviser is EnviSAGE faculty:

- ongoing students are internal active undergraduate researchers;
- completed students are internal alumni;
- the thesis is EnviSAGE-associated by `main-adviser`.

If EnviSAGE faculty appears only as co-adviser:

- the thesis is EnviSAGE-associated by `co-adviser-only`;
- students are not classified as EnviSAGE undergraduate researchers or alumni solely because of co-advising;
- student Person records use the neutral internal `thesis-author` role when needed for authorship links.

## Visibility Rules

The workflow never defaults records to public.

Use:

```text
visibility: internal
```

If a maintainer accidentally leaves visibility blank, the sync treats it as internal. If `public` is entered, the sync warns and forces internal in this phase.

## Reviewing Warnings

Warnings may identify:

- co-adviser-only records;
- unmatched adviser names;
- missing abstracts;
- missing keywords;
- rows excluded with `sync_action`;
- canonical records absent from the CSV.

Warnings do not always block sync. Errors must be fixed before writing.

## Common Errors

- Blank `record_id`
- Duplicate `record_id`
- More than two BS Geodetic Engineering student authors
- Missing thesis title
- Invalid `thesis_status`
- Ambiguous EnviSAGE faculty name match

## Deletion And Archive Safety

The sync does not delete canonical records when a CSV row disappears.

If a record should stop being active, set:

```text
thesis_status: archived
```

and keep visibility internal.

## Backup And Recovery

Before applying large changes:

1. Commit or stash unrelated work.
2. Run the dry-run and save the summary if needed.
3. Apply with `--write`.
4. Review `git diff`.
5. If the output is wrong, do not commit. Use Git to inspect and restore the affected files with maintainer approval.

Because all changes are plain text, Git history is the recovery mechanism.

## Public Publication Is Separate

This workflow prepares internal records only.

Future public Student Research pages or public student/alumni directory entries require a separate review phase covering names, titles, abstracts, keywords, repository links, consent/privacy, and publication readiness.
