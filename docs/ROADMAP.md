# Roadmap

This roadmap defines the broad development phases for the EnviSAGE web platform.

## Phase 0 - Governance and Architecture

Establish project identity, documentation, contribution norms, architecture direction, content model, and implementation roadmap.

Deliverables:

- `AGENTS.md`
- `README.md`
- Architecture documentation
- Roadmap documentation
- Content model documentation
- Contributing documentation

## Phase 1 - Development Foundation

Introduce the initial static-site development stack and baseline repository structure.

Status: Implemented as the Phase 1 development foundation. The foundation intentionally does not include final branding, full navigation, content UIs, spatial dashboards, deployment automation, or Phase 2 design-system work.

Deliverables:

- Astro project setup
- TypeScript configuration
- Tailwind CSS configuration
- Basic page layout structure
- Content directory structure
- Formatting, linting, type-checking, and build commands
- Astro content collection schema validation
- GitHub Actions CI workflow without deployment

## Phase 2 - Brand and Design System

Define the EnviSAGE visual identity for web use.

Status: Implemented as the Phase 2 design-system foundation. The foundation intentionally does not include final homepage design, full navigation, production content pages, catalog interfaces, spatial dashboards, deployment automation, or logo redesign.

Deliverables:

- Color palette
- Typography scale
- Layout grid
- UI components
- Accessibility rules
- Image and map styling direction
- Brand lockup strategy
- Brand asset location and documentation
- Development-only design-system preview route

## Phase 3 - Core Public Website

Build the initial public-facing website structure.

Status: Begun with Phase 3A global site shell. Phase 3A adds the production header, navigation, mobile menu, footer, shell layout, active states, and minimal placeholder routes.

Phase 3A.1 adds automatic GitHub Pages deployment for the organization Pages site at `https://updge-envisage.github.io/`. Deployment runs on pushes to `main` through the official GitHub Pages artifact workflow. The repository Pages source must be set to GitHub Actions.

Phase 3B adds the first production homepage. The homepage introduces EnviSAGE, broad research themes, research highlights, the Spatial Explorer, open research outputs, publications, people, and final calls to action while keeping destination pages as placeholders for later phases.

Likely remaining deliverables:

- About page
- Site navigation
- Footer
- Basic search or discovery affordances if appropriate
- Mobile and desktop responsive layouts

## Phase 4 - People and Research Areas

Publish structured information about the laboratory community and research themes.

Phase 4A establishes the research visual identity framework before full People and Research Areas pages. It adds a typed zero-entry visual registry, reusable research visual and motif components, public-approved-only usage rules, documented asset directories, and an approval workflow for future authentic EnviSAGE imagery.

Likely deliverables:

- People directory
- Faculty, researcher, student, and alumni groupings
- Research areas pages
- Links between people, projects, publications, and tools

## Phase 5 - Projects

Create the research project catalog.

Phase 5A establishes the EnviSAGE Founding Charter and production About page before the project catalog. The charter becomes the canonical identity document for the laboratory, and the About page provides a concise public-facing expression of that charter.

Phase 5B establishes the public research architecture before catalog implementation. It replaces the `/research/` placeholder with a conceptual research page covering research philosophy, six research areas, example topics, output types, and the discovery path from research areas to future projects, theses, and outputs.

Phase 5B also adds `docs/RESEARCH_MODEL.md` as the canonical conceptual model for research entities and relationships. The Founding Charter explains why EnviSAGE exists, the Research Model explains how EnviSAGE research knowledge is organized, the Content Model translates those concepts into website content, and Architecture explains the technical implementation.

Phase 5C refines public content and UX across the homepage, About page, Research page, site footer, and public placeholder pages. It reduces developer-facing language, tightens hero spacing, lowers card density where appropriate, and keeps each public page focused on a distinct visitor question.

Likely deliverables:

- Project listing page
- Project detail pages
- Project metadata schema
- Featured project support
- Related people, publications, tools, and datasets

## Phase 6A - People Directory Architecture

Phase 6A establishes `docs/PEOPLE_MODEL.md`, upgrades the Person content model, creates current public EnviSAGE leadership and faculty-affiliate records, and replaces the `/people/` placeholder with a production directory. Full individual profile pages remain deferred.

## Phase 6 - Publications

Create the publications database.

Likely deliverables:

- Publications listing
- Publication metadata schema
- Filters by year, author, type, keyword, and research area
- DOI, repository, dataset, and tool links where available

## Phase 7 - Student Research and Thesis Repository Ecosystem

Create the student research catalog and standard thesis repository model.

Likely deliverables:

- Student research listing
- Thesis metadata schema
- Thesis repository template
- Guidance for private ongoing repositories
- Guidance for reviewed public repositories under the EnviSAGE GitHub organization

## Phase 8 - Research Tools Catalog

Create a catalog for research code and selected interactive tools.

Likely deliverables:

- GitHub research tools catalog
- Tool metadata schema
- Links to repositories, documentation, demos, releases, and example outputs
- Criteria for browser-accessible tools

## Phase 9 - Spatial Data Architecture

Prepare the spatial data model and lightweight delivery approach.

Likely deliverables:

- Spatial layer metadata schema
- Dataset documentation conventions
- Data storage and publication guidance
- Initial prepared web datasets
- License, citation, and update procedure documentation

## Phase 10 - Interactive Spatial Explorer

Build the first interactive spatial dashboard.

Likely deliverables:

- MapLibre-based map interface
- Layer switching
- Legends
- Feature or location inspection
- Opacity controls
- Basic metadata panels
- Basic temporal filtering where appropriate
- Initial satellite-derived water quality and coastal ecosystem layers where available

## Phase 11 - Deployment, QA, Accessibility, Documentation

Harden the platform for public release.

Likely deliverables:

- GitHub Pages deployment verification
- Build and accessibility checks
- Responsive QA
- Content review
- Maintainer documentation
- Release checklist

## Phase 12 - EnviSAGE v1.0 Release

Publish EnviSAGE v1.0.

Likely deliverables:

- Public website launch
- Projects catalog
- Publications database
- Student research catalog
- Research tools catalog
- Standard thesis repository template
- One interactive spatial dashboard
- Final maintainer documentation
