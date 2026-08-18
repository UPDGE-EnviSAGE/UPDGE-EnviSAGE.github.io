# People Model

This document defines the EnviSAGE Person model for the public website and future research ecosystem catalogs. It specializes the Person entity from `docs/RESEARCH_MODEL.md` without redefining the full research ecosystem.

## Purpose

The People model establishes canonical Person records, EnviSAGE membership categories, role labels, visibility rules, and lightweight profile expectations for current and future members.

The public People directory answers: Who is part of EnviSAGE now?

## Canonical Person Principle

A person exists once in the EnviSAGE system.

A Person may have multiple relationships, including EnviSAGE role, institutional position, Projects, Theses, Publications, Research Themes, Geomatics Approaches, Research Topics, Grants, Datasets, and Software. Do not create duplicate Person records for different roles.

For example, a faculty member who is a Laboratory Head, Project PI, Thesis Adviser, and Publication Author should still have one canonical Person record.

## Categories

Categories describe a person's relationship with EnviSAGE. They are not the same as institutional job titles.

Supported categories:

1. Leadership
2. Faculty Affiliates
3. Researchers
4. Research Staff
5. Graduate Researchers
6. Undergraduate Researchers
7. Alumni

The internal neutral `thesis-author` category may be used only for associated but non-affiliated thesis authors who need canonical identity records for thesis authorship. It is not a public-facing EnviSAGE membership category.

A Person may have multiple categories where appropriate. Leadership records may also be classified as faculty-affiliated without duplicating the Person.

## EnviSAGE Roles

Supported EnviSAGE roles:

- Head
- Co-Head
- Faculty Affiliate
- Researcher
- Research Staff
- Graduate Researcher
- Undergraduate Researcher
- Alumni

The internal neutral `thesis-author` role may be used only for associated but non-affiliated thesis authors. It must not be used to imply EnviSAGE membership.

Roles describe the public-facing EnviSAGE relationship. They should be concise and should not be used to invent institutional titles.

## Institutional Position vs EnviSAGE Role

Institutional position describes a person's official appointment or public institutional title when it has been reviewed and approved for display.

EnviSAGE role describes the person's relationship to the laboratory.

These are separate fields. A person may be a faculty member institutionally while holding an EnviSAGE role such as Head, Co-Head, or Faculty Affiliate.

## Membership Status

Membership status is separate from public visibility.

Supported statuses:

- active
- alumni
- inactive

Examples:

- `membershipStatus: active`, `visibility: public`
- `membershipStatus: alumni`, `visibility: public`
- `membershipStatus: active`, `visibility: internal`

## Visibility

Only public Person records should render on the public People directory.

Supported Person visibility values:

- private
- internal
- public

Private and internal records must not appear publicly. This protects unfinished records, student information, internal membership details, and profile enrichment that has not been reviewed.

## Faculty Public Fields

Faculty profile architecture may support:

- name
- EnviSAGE role
- membership category
- institutional position
- photo
- short biography
- research interests
- Research Themes
- Geomatics Approaches
- Research Topics
- ORCID
- Google Scholar

Do not populate or display these fields until the values are explicitly reviewed and approved.

## Student Public Fields

Future student directory records should remain intentionally lightweight.

Recommended public fields:

- name
- category
- academic program or course
- current research or thesis topic
- optional Research Themes
- optional Geomatics Approaches
- optional Research Topics
- optional photo

Do not require long biographies, Google Scholar, ORCID, personal email, CV, or profile photographs for student records.

## Profile Lifecycle

Phase 6A implements the public directory. Phase 6B implements individual profile pages for the current reviewed EnviSAGE faculty records only.

Profile lifecycle:

1. Create private or internal Person record.
2. Review name, role, category, membership status, and visibility.
3. Publish only approved public fields.
4. Add profile enrichment such as biographies, photos, research interests, ORCID, Google Scholar, publications, datasets, software, and project relationships after review.
5. Enable individual profile pages only for reviewed public profiles.

Person cards should be able to support future profile links without rendering links to nonexistent pages.

## Research Relationships

`docs/RESEARCH_MODEL.md` remains authoritative for how People connect to Projects, Theses, Publications, Datasets, Software, Grants, Research Themes, Geomatics Approaches, and Research Topics.

The People model requires compatibility with those relationships but does not implement every relationship in Phase 6A.

## Faculty Specializations vs EnviSAGE Research Themes

Faculty specializations are faculty-specific areas of expertise. They may describe a person's methods, domains, or applied research strengths after review.

EnviSAGE Research Themes are lab-wide domains that represent the collective research portfolio. The approved Phase 6F taxonomy is defined in `docs/RESEARCH_TAXONOMY.md`. Do not substitute broad Research Themes for faculty specializations, and do not infer specialization values from thesis titles, abstracts, publication titles, or broad theme assignments.

Public faculty directory cards may show specialization keywords only when approved specialization data exists. If no approved specialization data exists, omit the keywords rather than inventing them.

## Student and Thesis Distinction

Students and Theses are separate entities.

A Thesis is the canonical scholarly research record. A student Person record may connect to a Thesis later, but the Thesis remains the public research record.

Examples:

```text
Undergraduate pair:

Student A --+
            +-- Thesis
Student B --+

MS/PhD:

Student
   |
Thesis / Dissertation
```

Do not implement thesis relationships in Phase 6A.

`docs/STUDENT_RESEARCH_MODEL.md` is authoritative for student research and thesis authorship rules, including the distinction between EnviSAGE-associated theses and EnviSAGE-affiliated students.

## Alumni Behavior

Alumni records may be public when reviewed and approved. Alumni status should not delete or duplicate historical Person records.

When someone becomes alumni, update membership status and category rather than creating a second Person record.

For undergraduate thesis maintenance, alumni status is derived from the thesis status only when the main adviser is EnviSAGE faculty. A co-adviser-only relationship does not make student authors EnviSAGE undergraduate researchers or alumni by itself.

For student research publication, approved thesis pages may display all thesis authors. Public alumni Person records remain limited to EnviSAGE-affiliated students whose main adviser was EnviSAGE faculty and whose student visibility has not been blocked during review.

The main `/people/` page should remain a concise current-community directory. It may show a compact alumni teaser and link to `/people/alumni/`, but it must not render a long historical wall of undergraduate alumni.

The `/people/alumni/` page is the public directory for historical EnviSAGE-affiliated undergraduate researchers. It excludes co-advised-only thesis authors, internal students, active students, and unrelated thesis authors. Alumni are grouped by thesis or completion year and should link to a public thesis when one resolves.

Do not generate standalone undergraduate alumni profile routes. The Thesis remains the canonical public scholarly record for undergraduate research.

## Empty-Category Behavior

The public People directory should omit categories with zero public records.

Do not show empty sections such as "No researchers yet" or "Alumni coming soon." This rule keeps the public directory concise while allowing future categories to appear automatically when public records exist.

When public alumni grow large, render alumni with a compact list/grid rather than oversized faculty-style cards.

## Faculty Undergraduate Advising

Faculty profile pages may show an Undergraduate Research Advising section derived from reviewed public Student Research records.

Advising relationships must be derived from thesis records, not hardcoded into faculty records. Preserve the role distinction:

- Main Adviser
- Co-Adviser

Faculty advising counts should count unique public undergraduate thesis records where the faculty member is main adviser or co-adviser. Student counts should count unique public student authors across those thesis records without double-counting the same canonical student identity.

Faculty names may link to `/people/<faculty-slug>/` only when the adviser resolves to a reviewed public EnviSAGE faculty Person record. Do not create or link to external adviser profiles in this model.

Public advising display should be compact and progressively disclosed. Faculty profiles may show thesis and student totals, optional main/co-adviser counts, and year-grouped thesis lists. Avoid large dashboard-style metric cards or one large card per thesis.

## Faculty Profile Enrichment

The official institutional verification source for future faculty position review is:

https://home.dge.upd.edu.ph/faculty

Maintainer-supplied Google Scholar references for future Phase 6B profile enrichment:

- Ariel C. Blanco: https://scholar.google.com/citations?user=GsTd7Q8AAAAJ&hl=en
- Ayin M. Tamondong: https://scholar.google.com/citations?hl=en&user=znfmgaoAAAAJ
- Jommer M. Medina: https://scholar.google.com/citations?hl=en&user=3IQbFRkAAAAJ
- Erica Erin E. Elazegui: https://scholar.google.com/citations?hl=en&user=ITTl_r0AAAAJ
- Margaux Angelica A. Cruz: https://scholar.google.com/citations?hl=en&user=qc7H3KEAAAAJ
- John Emmanuel D. Escoto: https://scholar.google.com/citations?hl=en&user=i_J4w8cAAAAJ

Do not automatically query Google Scholar for publication counts, citation counts, h-index, or other metrics. These values are dynamic and are not part of the faculty profile system.

Use `docs/FACULTY_PROFILE_GUIDE.md` for the current faculty biography, research-interest, photo, Google Scholar, ORCID, and future relationship rules.

## Public and Privacy Principles

- Publish only reviewed public fields.
- Do not invent biographies, research interests, photos, emails, ORCID records, awards, CVs, projects, theses advised, or publication lists.
- Do not expose private or internal records on the public site.
- Do not expose student personal information beyond reviewed lightweight public fields.
- Do not render blank labels or unavailable placeholders.
- Do not use stock portraits, generated faces, silhouette clip art, or unsupported profile photographs.
