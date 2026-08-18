# Content Model

This document defines the initial repository-managed content model for the EnviSAGE web platform. Exact schemas should be finalized during implementation, but the platform should be designed around structured content rather than a database-backed CMS.

EnviSAGE is Environmental Systems Applications of Geomatics Engineering, the research laboratory of the UP Department of Geodetic Engineering focusing on the use of Geomatics and geospatial technologies in addressing environmental issues.

`docs/RESEARCH_MODEL.md` is the canonical conceptual model for EnviSAGE research entities and relationships. This content model describes how those concepts can be represented as website-managed content.

`docs/PEOPLE_MODEL.md` specializes the Person entity for EnviSAGE membership categories, roles, visibility, and future profile enrichment.

`docs/STUDENT_RESEARCH_MODEL.md` specializes thesis and student research records, including authorship, adviser relationships, visibility, import rules, and future publication review.

## Content Principles

- Store public content as Markdown/MDX and structured data files.
- Keep the platform public-first.
- Make content reviewable through GitHub pull requests.
- Use stable slugs and identifiers.
- Keep large datasets outside the repository.
- Link related records across people, Research Themes, Geomatics Approaches, projects, publications, student research, tools, and datasets.

## Core Content Types

### People

Suggested fields:

- name
- slug
- EnviSAGE roles
- categories
- membership status
- visibility
- display order
- institution
- institutional position
- academic program when relevant
- photo
- short biography
- email or contact URL when public and approved
- ORCID, Google Scholar, personal website, or GitHub when reviewed
- research themes
- geomatics approaches
- research topics
- projects
- theses
- publications
- datasets
- tools
- grants
- student research records
- import batch identifier when records are generated from an internal source

Only public Person records should appear in the public People directory. Private and internal records, including development fixtures, must remain excluded.

### Research Themes

Suggested fields:

- title
- slug
- summary
- description
- keywords
- related people
- related projects
- related publications
- related datasets
- related tools

The implemented schema may still use the legacy key `researchAreas` for compatibility. Public copy should use Research Themes, and canonical taxonomy values are defined in `docs/RESEARCH_TAXONOMY.md`.

### Projects

Suggested fields:

- title
- slug
- summary
- description
- status
- start year
- end year
- funder or partner
- project team
- research themes
- geomatics approaches
- publications
- datasets
- tools
- external links
- featured image

### Publications

Suggested fields:

- title
- slug or citation key
- canonical publication ID
- authors
- year
- publication type
- source or venue
- abstract
- DOI
- URL
- faculty relationships
- research themes
- geomatics approaches
- visibility
- bibliographic status
- source provenance
- internal notes
- related projects
- related datasets
- related tools
- keywords

Imported faculty publications default to `visibility: internal`. Public publication pages and faculty profiles must render only `visibility: public` records and must not expose internal provenance or review fields.

### Student Research

Suggested fields:

- thesis title
- slug
- stable record ID for maintainer synchronization
- thesis type
- program
- status
- students
- canonical student Person references
- main adviser
- canonical main adviser Person reference when applicable
- co-advisers
- canonical co-adviser Person references when applicable
- year
- abstract
- keywords
- research topics
- research themes
- geomatics approaches
- EnviSAGE association status and basis
- EnviSAGE adviser roles
- projects
- publications
- datasets
- tools
- repository
- source code
- notebooks
- sample data
- documentation
- installation instructions
- example outputs
- maps or figures
- thesis PDF reference
- related publication
- dataset DOI
- software DOI
- review/publication status
- visibility

Ongoing thesis repositories should normally remain private. After completion and appropriate review, repositories may become public under the EnviSAGE GitHub organization.

The implemented student research schema uses `students[]` rather than a singular `student` field. BS Geodetic Engineering thesis records must list 1 to 2 students. MS thesis and PhD dissertation records must list exactly 1 student.

Imported historical thesis records may remain `visibility: internal` while awaiting review. Internal student research records must not generate public pages or appear in public catalogs.

Undergraduate thesis maintenance uses `data-maintenance/undergraduate-theses.csv` as a non-public editing layer. The canonical records remain the Person and Student Research content files; the CSV should be synchronized into those files through the documented dry-run-first workflow rather than treated as an independent database.

Student research publication uses `data-maintenance/student-research-publication-review.csv` as a non-public approval layer. Review decisions must be synchronized into canonical visibility fields before the public website renders thesis catalog cards, thesis pages, or public alumni records.

### Research Tools

Suggested fields:

- name
- slug
- summary
- description
- tool level
- repository URL
- demo URL
- documentation URL
- license
- maintainers
- related projects
- related publications
- related datasets
- programming language
- installation instructions
- example outputs

V1 should support Level 1 open research code hosted in GitHub repositories and selected Level 2 browser-accessible research tools where technically appropriate.

### Datasets and Spatial Layers

Suggested fields:

- title
- slug
- summary
- description
- data type
- spatial extent
- temporal extent
- coordinate reference system
- source
- processing method
- license
- citation
- storage location reference
- public access URL when available
- related projects
- related publications
- related tools
- map layer configuration
- legend
- update frequency

Large raster and scientific datasets must not be committed directly to this repository.

### Teaching and Training Resources

Suggested fields:

- title
- slug
- summary
- resource type
- audience
- authors
- year
- files or links
- related tools
- related datasets
- prerequisites

## Initial Spatial Themes

The first spatial examples should focus on:

- Satellite-derived water quality
- Seagrass, coral, and mangrove mapping

## Repository Data Boundaries

Allowed in the repository:

- Metadata
- Markdown/MDX content
- Structured content files
- Small sample data
- Optimized thumbnails
- Prepared lightweight web map assets when justified

Not allowed in the repository:

- Large rasters
- Raw scientific datasets
- Large archives
- Unreviewed private thesis data
- Complete NAS, external drive, local computer, or Google Drive dataset copies
