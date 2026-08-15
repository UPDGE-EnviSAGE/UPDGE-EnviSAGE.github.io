# Student Research Publication Guide

Status: Maintainer review workflow

This guide explains how to review and publish student research records without editing many individual content files.

Publication is explicit. Records do not become public unless the review CSV says so.

## File To Review

Open:

```text
data-maintenance/student-research-publication-review.csv
```

This CSV is the maintainer review layer. Canonical records remain in:

- `src/content/student-research/`
- `src/content/people/`

## Review All Entries

1. Open `data-maintenance/student-research-publication-review.csv`.
2. Review each row.
3. Change `publication_decision` to one of:
   - `approve`
   - `hold`
   - `needs-fix`
   - `pending-review`
4. Save the CSV.
5. Run a dry-run:

```sh
python3 scripts/publish-student-research.py
```

6. Review the summary.
7. If correct, apply changes:

```sh
python3 scripts/publish-student-research.py --write
```

8. Run site validation:

```sh
npm run format:check
npm run check
npm run lint
npm run build
```

9. Review `git diff`.
10. Commit the reviewed publication changes.

## Approve Many Records Quickly

Use Excel, LibreOffice, or another CSV editor.

Filter to records that are ready. For selected rows, fill:

```text
publication_decision = approve
```

Save the CSV, then run:

```sh
python3 scripts/publish-student-research.py
```

Bulk approval still only affects rows explicitly marked `approve`. Pending, held, or needs-fix records stay internal.

## Regenerate The Review CSV

When canonical thesis data changes, regenerate the review CSV:

```sh
python3 scripts/review-student-research.py --summary
```

Regeneration preserves these maintainer columns by stable `record_id`:

- `publication_decision`
- `public_thesis`
- `public_student_1`
- `public_student_2`
- `review_notes`

## Review Columns

- `record_id`: Stable identifier used to preserve decisions.
- `year`: Thesis year.
- `thesis_title`: Thesis title.
- `student_1`, `student_2`: Student authors.
- `main_adviser`: Main adviser.
- `co_advisers`: Co-advisers.
- `association_basis`: Whether EnviSAGE faculty is main adviser or co-adviser only.
- `student_1_envisage_affiliated`, `student_2_envisage_affiliated`: Derived from the main-adviser rule.
- `abstract_preview`: Short abstract preview for review.
- `abstract_present`: Whether the canonical record has an abstract.
- `keywords`: Source keywords.
- `keywords_present`: Whether keywords exist.
- `thesis_status`: Ongoing, completed, or archived.
- `thesis_slug`: Public URL slug if published.
- `current_visibility`: Current canonical visibility.
- `publication_decision`: Main approval decision.
- `public_thesis`: `auto`, `yes`, or `no`.
- `public_student_1`, `public_student_2`: `auto`, `yes`, or `no`.
- `review_notes`: Maintainer notes. These are not public.

## Approval Rules

If `publication_decision = approve`, the thesis may become public.

If `publication_decision` is `pending-review`, `hold`, or `needs-fix`, the thesis remains internal.

If `public_thesis = no`, the thesis remains internal even if the decision says approve.

## Student Visibility

If the thesis main adviser is EnviSAGE faculty and the thesis is approved, affiliated completed students may become public alumni Person records unless blocked by `public_student_1` or `public_student_2`.

If EnviSAGE faculty is only a co-adviser, the student name may appear as a thesis author on the public thesis page, but the student does not become EnviSAGE alumni or a public EnviSAGE member solely because of co-advising.

Use `public_student_1 = no` or `public_student_2 = no` when a student Person record should remain internal. The student name still appears on the approved thesis page unless the thesis itself is held.

## Correcting Data

If thesis or student data is wrong, normally edit:

```text
data-maintenance/undergraduate-theses.csv
```

Then run:

```sh
python3 scripts/sync-undergraduate-theses.py data-maintenance/undergraduate-theses.csv --write
python3 scripts/review-student-research.py --summary
```

Do not edit generated canonical files directly unless it is an exceptional correction. If you do, reconcile the maintenance CSV afterward.

## Common Reasons To Hold

- Adviser spelling needs checking.
- Abstract is missing.
- Keywords are missing.
- Co-adviser parsing looks suspicious.
- Student requested privacy.
- Thesis title needs correction.

Use `review_notes` to capture the reason.

## Publication Output

Approved public theses appear in:

```text
/student-research/
/student-research/<slug>/
```

Approved public EnviSAGE-affiliated alumni appear in:

```text
/people/alumni/
```

The main `/people/` page shows only the current EnviSAGE community plus a compact alumni teaser. It does not list all historical undergraduate alumni.

Faculty profile pages derive Undergraduate Research Advising sections from approved public thesis records. The section preserves Main Adviser and Co-Adviser roles and updates automatically as thesis visibility changes.

Review notes, publication decisions, internal visibility states, and administrative metadata are never rendered publicly.
