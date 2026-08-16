# Student Research Model

Status: Canonical model document

This document defines how EnviSAGE represents student research and thesis records. It specializes the Thesis entity from `docs/RESEARCH_MODEL.md` and complements `docs/PEOPLE_MODEL.md`.

## Purpose

The Student Research model establishes a public-first but review-gated structure for thesis records, thesis authorship, adviser relationships, GitHub repositories, datasets, software, publications, and future public catalog pages.

Phase 6C imports historical BS Geodetic Engineering thesis records as internal staging content only. Successful import does not imply publication approval.

## Thesis as Canonical Scholarly Record

A Thesis is the canonical scholarly record for student research. The thesis record should carry the title, year, program, authors, adviser roles, abstract, keywords, review status, visibility, and future relationships to repositories and research outputs.

Student profile pages are optional. Do not require one public student profile for every thesis author.

Undergraduate thesis records also carry a stable `recordId` for maintenance synchronization. Do not use a thesis title as the identity key because ongoing titles may change.

## Person vs Thesis

A Person record represents an individual. A Thesis record represents a scholarly work.

Do not use a thesis record to imply EnviSAGE membership for every author. Do not use a Person record as the only public scholarly record for a thesis.

## Undergraduate Pair-Thesis Rules

BS Geodetic Engineering thesis records may have one or two student authors.

If a source record has two authors, keep both authors on one thesis record. Do not split pair theses into separate records.

## MS/PhD Individual-Thesis Rules

MS thesis and PhD dissertation records should have exactly one student author.

This rule is enforced in the content schema and should remain distinct from BS thesis rules.

## Adviser Relationships

Thesis records preserve adviser roles explicitly:

- `adviser` stores the main adviser display name.
- `mainAdviserPerson` stores the canonical Person slug when the main adviser is an existing EnviSAGE faculty record.
- `coAdvisers` stores co-adviser display names.
- `coAdviserPeople` stores canonical Person slugs when co-advisers are existing EnviSAGE faculty records.

Do not collapse main adviser and co-advisers into an undifferentiated adviser list.

Public thesis pages and the Student Research catalog may link adviser names to faculty profile pages only when the adviser resolves to a canonical public EnviSAGE faculty Person record. Non-EnviSAGE advisers remain plain text until a future external-person model exists.

Faculty undergraduate advising lists are derived from reviewed public thesis records using `mainAdviserPerson` and `envisageCoAdvisers`. Do not manually duplicate thesis titles or advising counts in faculty Person records.

## EnviSAGE-Associated Thesis

A thesis is EnviSAGE-associated when at least one of these is true:

- the main adviser is EnviSAGE Faculty; or
- at least one co-adviser is EnviSAGE Faculty.

Use `envisageAssociated`, `envisageAssociationBasis`, `envisageMainAdviser`, `envisageCoAdvisers`, and `envisageAdviserRoles` to preserve this distinction.

## EnviSAGE-Affiliated Student

A student is an EnviSAGE-affiliated Undergraduate Researcher only when the thesis main adviser is EnviSAGE Faculty.

If EnviSAGE Faculty appears only as co-adviser, the thesis is EnviSAGE-associated but the student is not classified as an EnviSAGE Undergraduate Researcher.

## Alumni Classification

Historical completed BS thesis students whose main adviser is EnviSAGE Faculty may be represented internally as:

- `envisageRoles: undergraduate-researcher, alumni`
- `categories: undergraduate-researcher, alumni`
- `membershipStatus: alumni`
- `visibility: internal`

They should not appear publicly until reviewed and explicitly promoted.

## Co-Advised-Only Authors

Associated but non-affiliated thesis authors may have internal canonical Person records so authorship relationships resolve.

Use the neutral internal `thesis-author` role/category for these records. This is not a public-facing EnviSAGE membership category and must not be used to describe someone as EnviSAGE alumni or an EnviSAGE undergraduate researcher.

## Visibility and Publication Workflow

Imported thesis and student records should begin as `visibility: internal`.

Only reviewed `visibility: public` thesis records may generate public Student Research pages or appear in public catalogs. Internal records must not be exposed on the public website.

Publication is controlled through `data-maintenance/student-research-publication-review.csv`. A thesis becomes eligible for public catalog and page generation only when its `publication_decision` is explicitly set to `approve` and the publication sync applies the change.

## Abstract and Keyword Handling

Import abstracts as supplied, preserving meaning. Normalize only accidental whitespace and line-break problems.

Import source keywords into `keywords`. Do not replace source keywords with a new taxonomy.

Use `researchTopics` only when a keyword maps unambiguously to an existing controlled Research Topic. Leave uncertain topics unmapped for later curation.

Do not assign strategic Research Areas automatically from titles or abstracts.

## GitHub Relationship

Thesis records may later link to reviewed GitHub repositories, source code, notebooks, documentation, and example outputs.

Ongoing thesis repositories should normally remain private. Completed repositories may become public only after completion and review.

## Future Relationships

Thesis records are designed to connect later to:

- Projects
- Publications
- Datasets
- Software
- Maps and dashboards

Do not invent these relationships during import.

## Import Workflow

Use `scripts/import-undergraduate-theses.py` for the Phase 6C source workbook import.

The importer:

- accepts the source workbook path explicitly;
- reads the `Selected Advisers` worksheet;
- supports dry-run mode by default;
- writes generated content only with `--write`;
- performs deterministic slug generation;
- detects duplicate names and slug collisions;
- validates authorship, adviser, association, and visibility invariants;
- writes an internal audit document at `docs/imports/UNDERGRAD_THESIS_IMPORT_2026.md`.

The source workbook must remain outside the repository and must not be committed.

## Maintenance Workflow

Use `data-maintenance/undergraduate-theses.csv` as the human-editable layer for routine undergraduate thesis updates.

Use the dry-run sync first:

```sh
python3 scripts/sync-undergraduate-theses.py data-maintenance/undergraduate-theses.csv
```

Apply reviewed changes explicitly:

```sh
python3 scripts/sync-undergraduate-theses.py data-maintenance/undergraduate-theses.csv --write
```

The sync:

- matches records by stable `record_id`;
- preserves stable thesis and Person slugs where practical;
- supports one-student and two-student BS Geodetic Engineering theses;
- derives active/alumni student membership only from the EnviSAGE main-adviser rule;
- treats co-adviser-only authors as non-affiliated internal thesis authors;
- defaults visibility to internal and never promotes records to public;
- reports canonical records missing from the CSV instead of deleting them.

See `docs/UNDERGRADUATE_THESIS_MAINTENANCE.md` for maintainer-facing instructions.

## Publication Review Workflow

Use `scripts/review-student-research.py` to generate and summarize the publication review CSV:

```sh
python3 scripts/review-student-research.py --summary
```

Use `scripts/publish-student-research.py` for dry-run publication review:

```sh
python3 scripts/publish-student-research.py
```

Apply only reviewed decisions with:

```sh
python3 scripts/publish-student-research.py --write
```

Only rows with `publication_decision: approve` may transition a thesis to `visibility: public`. Pending, held, or needs-fix rows remain internal.

Public thesis pages may show all authors, including co-advised-only authors, because authorship is part of the scholarly record. Public Person promotion remains stricter: only EnviSAGE-affiliated students derived from the main-adviser rule may become public alumni records, and student-level privacy overrides may keep affiliated Person records internal.

Public display normalizes student and adviser names through a shared display helper. The helper converts unambiguous `LAST, First Middle` values to `First Middle Last`, applies conservative title casing, and preserves common lowercase particles such as `de`, `del`, `dela`, `de la`, `van`, `von`, and `y` where safely recognizable. Stable Person IDs and slugs remain authoritative and must not be regenerated solely because display capitalization changes.

Use `data-maintenance/student-name-normalization-review.csv` to review display-name changes where the normalized public form differs from the stored source name.

Public student research pages should read like a research catalog, not an administrative review system. Show thesis titles, years, students, adviser roles, abstracts, keywords, and relevant links in concise public language. Do not expose review decisions, import metadata, record IDs, visibility values, source workbook details, or maintainer notes on public pages.

See `docs/STUDENT_RESEARCH_PUBLICATION_GUIDE.md` for maintainer-facing publication instructions.

## Duplicate Handling

Normalize student names for duplicate detection by trimming whitespace, collapsing repeated spaces, and comparing normalized capitalization and punctuation.

Retain the first reviewed display name. If identity is uncertain, do not merge records merely because names are similar; flag the case for maintainer review.

## Privacy and Review

The Phase 6C import is a staging import.

Do not publish imported students or theses without a separate review phase. Future review should check titles, names, adviser parsing, abstracts, keywords, visibility, repository links, and any public-facing student/alumni classification.
