# Contributing

This guide defines how future EnviSAGE maintainers, researchers, and students should contribute to the web platform.

EnviSAGE is Environmental Systems Applications of Geomatics Engineering, the research laboratory of the UP Department of Geodetic Engineering focusing on the use of Geomatics and geospatial technologies in addressing environmental issues.

## Contribution Model

The platform should use repository-managed content and code. Contributors should normally propose changes through GitHub pull requests so content, metadata, and implementation changes can be reviewed before publication.

The platform is public-first. Authentication, internal collaboration features, PostGIS, APIs, Google Earth Engine, and large-scale data infrastructure are deferred until later phases unless explicitly approved.

## Before Making Changes

- Read `README.md`, `AGENTS.md`, and the relevant files in `docs/`.
- Confirm whether the change is content, design, code, data metadata, or architecture.
- Avoid adding infrastructure or dependencies that are not needed for the current roadmap phase.
- Do not commit large research datasets.

## Content Contributions

Content contributions should be clear, public-ready, and structured according to `docs/CONTENT_MODEL.md`.

Use stable slugs and descriptive titles. Include related people, projects, publications, datasets, tools, and research areas where known.

## Student Research Contributions

Ongoing thesis repositories should normally remain private. Public student research entries should be added only after completion and appropriate review.

Student research records should include the applicable fields from the student research content model, including thesis title, thesis type, students, adviser, year, abstract, keywords, repository, code, notebooks, sample data, documentation, outputs, thesis PDF reference, related publication, dataset DOI, and software DOI where available.

## Data Contributions

Do not commit large raster, scientific, raw, or archival datasets to this repository.

For data-related contributions, provide:

- Dataset title
- Description
- Source
- License or access conditions
- Citation
- Processing notes
- Storage location reference
- Public access URL when available
- Related project, publication, or tool links

Only lightweight prepared web assets or small sample data should be committed when justified.

## Code Contributions

Implementation should follow the established project stack once Phase 1 begins. Until then, do not scaffold the website or add build dependencies without an explicit task.

Code should be:

- Maintainable
- Accessible
- Responsive
- Performant
- Modular
- Documented where architectural decisions are involved

## Verification

Before submitting implementation changes, run the relevant project commands for formatting, linting, type checking, building, and testing.

If verification cannot be run, explain why in the pull request or final handoff.

## Documentation Updates

Update documentation when a contribution changes:

- Architecture
- Roadmap phase scope
- Content schemas
- Data policies
- Contributor workflow
- Deployment behavior
- Testing or build expectations

## Review Priorities

Reviewers should prioritize:

- Accuracy of public-facing information
- Accessibility
- Responsive behavior
- Performance
- Maintainability
- Data and licensing clarity
- Avoidance of unnecessary complexity
