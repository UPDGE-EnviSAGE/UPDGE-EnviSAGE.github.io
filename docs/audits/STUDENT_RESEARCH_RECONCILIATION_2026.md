# Student Research Count Reconciliation 2026

Status: Phase 6F.3 audit

This audit reconciles the apparent difference between the historical Phase 6C undergraduate thesis import count of 125 associated theses and a later reported count of 124 public undergraduate thesis records. It does not approve, publish, delete, or modify any thesis record.

## Authoritative Counts

- Historical Phase 6C source thesis rows examined: 125
- Historical Phase 6C EnviSAGE-associated theses imported: 125
- Current `data-maintenance/undergraduate-theses.csv` rows: 125
- Current `data-maintenance/student-research-publication-review.csv` rows: 125
- Current canonical BS Geodetic Engineering thesis content records: 125
- Current public canonical thesis records: 125
- Current internal canonical thesis records: 0
- Current private development-only thesis fixtures: 1
- Current public EnviSAGE undergraduate alumni: 181

## Reconciliation Result

The current production repository contains 125 public undergraduate thesis records. No canonical thesis record accounts for a true 125 versus 124 public-count difference.

The apparent 124 count was caused by an audit parser error, not by repository data. One public thesis abstract contains the substring `---` inside normal prose, and a naive frontmatter split treated that substring as the end of the frontmatter block. That caused the audit to miss the valid `reviewStatus: public` and `visibility: public` fields later in the file.

One separate workflow caution was observed: `data-maintenance/undergraduate-theses.csv` still records the historical staging visibility as `internal` for its 125 rows, while `data-maintenance/student-research-publication-review.csv` records 125 `approve` decisions and canonical content records are public. The publication review CSV and canonical content are authoritative for the current public site. Do not run the maintenance sync with `--write` until that older maintenance CSV workflow is intentionally reconciled.

Affected record:

- Record ID: `bsge-2018-035`
- Slug: `using-gis-in-planning-a-post-earthquake-evacuation-scheme-routing-and-shelter-assignments-in-barangay-batasan-hills-quezon-city`
- Year: 2018
- Title: Using GIS in Planning a Post-Earthquake Evacuation Scheme: Routing and Shelter Assignments in Barangay Batasan Hills, Quezon City
- Students: CAMELOTE, Katlyn Joy A.; FOMBUENA, Honey Grace E.
- Main adviser: BLANCO, Ariel C.
- Co-advisers: none
- EnviSAGE association basis: main-adviser
- Visibility: public
- Review status: public
- Publication decision: approve
- Reason it appeared non-public in the earlier count: audit parser split on an unanchored `---` sequence inside the abstract text.

## Classification

Classification: other.

Evidence indicates no intentional non-public thesis record, incomplete maintainer review, publication workflow inconsistency, or canonical-data inconsistency causing a 124 public count. The repository's current canonical content, publication review CSV, public route filters, and production build all support 125 public thesis records. The stale staging visibility in `data-maintenance/undergraduate-theses.csv` is a maintenance-workflow caution, not the cause of the 124 count.

## Relationship QA

The public undergraduate alumni count remains 181. Co-adviser-only student authors remain internal/non-member people records and are not incorrectly promoted as EnviSAGE undergraduate alumni. No missing student Person references, duplicate Person slugs, or student relationship length mismatches were found in public thesis records.

Faculty advising counts are derived from current public thesis records:

- Ariel C. Blanco: 50 public theses advised; 44 main-advised; 6 co-advised; 95 students.
- Ayin M. Tamondong: 62 public theses advised; 45 main-advised; 17 co-advised; 119 students.
- Jommer M. Medina: 23 public theses advised; 0 main-advised; 23 co-advised; 42 students.
- Erica Erin E. Elazegui: 12 public theses advised; 3 main-advised; 9 co-advised; 24 students.
- Margaux Angelica A. Cruz: 2 public theses advised; 1 main-advised; 1 co-advised; 4 students.
- John Emmanuel D. Escoto: 3 public theses advised; 0 main-advised; 3 co-advised; 5 students.

## Public Route QA

The public student research list, thesis detail pages, people directory, alumni directory, and faculty profile advising sections are all driven by `visibility: public` canonical content. The development-only thesis fixture remains `visibility: private` and does not produce a public thesis route.

## Final Interpretation

No data correction is required. The authoritative current public thesis count is 125, with 181 public EnviSAGE undergraduate alumni. Future audit scripts or ad hoc checks should parse frontmatter using delimiter lines anchored at the beginning of a line rather than splitting on any `---` substring in file content.
