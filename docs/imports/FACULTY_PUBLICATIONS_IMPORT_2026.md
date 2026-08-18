# Faculty Publications Import 2026

Status: Phase 6F.1 import and QA audit

The verified source register supplied by the maintainer is the authoritative source for this import. The workflow does not use web lookup and does not infer missing bibliographic metadata.

- Source rows: 351
- READY rows: 345
- REVIEW/HOLD rows: 6
- Canonical publication records after exact title/year deduplication: 299
- Duplicate title/year groups: 50
- Source rows represented in duplicate groups: 102
- DOI values retained: 61
- DOI values marked online-primary-verified: 18
- DOI values marked user-supplied-SUKAT: 43
- Canonical records held from public review because at least one source row is REVIEW/HOLD: 6

Phase 6F.1 adds controlled QA files around the 299 canonical records:

- Clean-for-review records: 289
- Exception records: 10
- Multi-faculty canonical records: 48
- Conservative duplicate candidates: 2
- Taxonomy review rows: 134

The six non-ready source records remain held. They must not be corrected, completed, or made public without maintainer review of the source register.

All imported records default to `visibility: internal`. Maintainers must update `data-maintenance/faculty-publications-review.csv` with `publication_decision: approve` and run the publish script before any record can become public.

See `docs/FACULTY_PUBLICATION_REVIEW_GUIDE.md` for the controlled review workflow.
