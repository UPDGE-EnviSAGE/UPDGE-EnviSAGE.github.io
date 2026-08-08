# Content Model

This document defines the initial repository-managed content model for the EnviSAGE web platform. Exact schemas should be finalized during implementation, but the platform should be designed around structured content rather than a database-backed CMS.

EnviSAGE is Environmental Systems Applications of Geomatics Engineering, the research laboratory of the UP Department of Geodetic Engineering focusing on the use of Geomatics and geospatial technologies in addressing environmental issues.

## Content Principles

- Store public content as Markdown/MDX and structured data files.
- Keep the platform public-first.
- Make content reviewable through GitHub pull requests.
- Use stable slugs and identifiers.
- Keep large datasets outside the repository.
- Link related records across people, research areas, projects, publications, student research, tools, and datasets.

## Core Content Types

### People

Suggested fields:

- name
- slug
- role
- affiliation
- email or contact URL when public
- profile image
- biography
- research areas
- projects
- publications
- tools
- student research records

### Research Areas

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
- research areas
- publications
- datasets
- tools
- external links
- featured image

### Publications

Suggested fields:

- title
- slug or citation key
- authors
- year
- publication type
- venue
- abstract
- DOI
- URL
- related projects
- related datasets
- related tools
- keywords

### Student Research

Suggested fields:

- thesis title
- slug
- student
- adviser
- year
- abstract
- keywords
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

Ongoing thesis repositories should normally remain private. After completion and appropriate review, repositories may become public under the EnviSAGE GitHub organization.

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
