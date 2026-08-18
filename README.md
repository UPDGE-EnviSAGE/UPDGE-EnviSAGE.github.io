# Environmental Systems Applications of Geomatics Engineering

Environmental Systems Applications of Geomatics Engineering (EnviSAGE) is the research laboratory of the UP Department of Geodetic Engineering focusing on the use of Geomatics and geospatial technologies in addressing environmental issues.

This repository is the GitHub Pages organization repository for the EnviSAGE web platform.

The platform is public-first. Future internal collaboration features should be deferred until later phases unless explicitly approved.

The canonical identity document for EnviSAGE is the [Founding Charter](docs/FOUNDING_CHARTER.md). Public-facing copy, proposals, presentations, and laboratory materials should trace their institutional framing back to the charter.

The canonical research ecosystem document is the [Research Model](docs/RESEARCH_MODEL.md). It defines how EnviSAGE Research Themes, Geomatics Approaches, topics, people, projects, theses, outputs, and supporting entities relate conceptually.

The canonical research taxonomy is the [Research Taxonomy](docs/RESEARCH_TAXONOMY.md). It defines the approved five public Research Themes and six cross-cutting Geomatics Approaches.

The canonical people architecture document is the [People Model](docs/PEOPLE_MODEL.md). It defines Person records, EnviSAGE membership categories, roles, visibility, and profile-enrichment rules.

The faculty profile maintainer guide is the [Faculty Profile Guide](docs/FACULTY_PROFILE_GUIDE.md). It defines source, biography, photo, Google Scholar, ORCID, and future relationship rules for public faculty pages.

The canonical student research architecture document is the [Student Research Model](docs/STUDENT_RESEARCH_MODEL.md). It defines thesis records, student authorship, adviser relationships, visibility, and import/review rules.

The undergraduate thesis maintainer workflow is documented in the [Undergraduate Thesis Maintenance Guide](docs/UNDERGRADUATE_THESIS_MAINTENANCE.md). Maintainers edit `data-maintenance/undergraduate-theses.csv`, run the dry-run sync, review warnings, and then apply changes to canonical Person and Student Research records.

The student research publication workflow is documented in the [Student Research Publication Guide](docs/STUDENT_RESEARCH_PUBLICATION_GUIDE.md). Maintainers review `data-maintenance/student-research-publication-review.csv`; only rows explicitly marked `approve` may become public.

The faculty publication workflow is documented in the [Publication Model](docs/PUBLICATION_MODEL.md) and [Faculty Publication Review Guide](docs/FACULTY_PUBLICATION_REVIEW_GUIDE.md). Imported faculty publications default to internal visibility and require maintainer approval before appearing on `/publications/` or faculty profiles.

## Platform Priorities

The EnviSAGE platform will be developed in this order:

1. Public laboratory website
2. Research project showcase
3. Repository/catalog of student thesis codes and tools
4. Spatial data portal
5. Interactive geospatial dashboard
6. Repository of publications/datasets
7. Teaching and training resources
8. Future internal laboratory collaboration platform

## Version 1.0 Scope

EnviSAGE v1.0 is expected to include:

- Professional laboratory homepage
- About section
- Research Themes
- People directory
- Projects catalog
- Publications database
- Student research catalog
- GitHub research tools catalog
- Standard thesis repository template
- One interactive spatial dashboard
- Responsive desktop and mobile design
- Automated deployment from GitHub
- Documentation for future maintainers

## Phase 1 Foundation

Phase 1 establishes the development foundation only. It is not the final visual implementation of the EnviSAGE website and does not include final branding, full navigation, research pages, catalogs, or the spatial dashboard.

## Phase 2 Design System

Phase 2 establishes the EnviSAGE visual identity and design-system foundation. It introduces design tokens, reusable visual primitives, brand asset expectations, and a development-only design-system preview route at `/design-system`.

The Phase 2 work does not redesign the historical EnviSAGE logo, build the final homepage, create full navigation, or add production research content.

## Research Architecture

Phase 5B establishes `/research/` as the conceptual center of the public platform. Phase 6F updates that page to use the approved five Research Themes, six cross-cutting Geomatics Approaches, representative research topics, and the discovery path from taxonomy into research work, projects, theses, outputs, publications, datasets, software, and dashboards.

This phase does not implement project, publication, student research, software, dataset, or dashboard catalogs. Those remain later roadmap work.

Student research schema support now uses `students[]` for thesis authorship. BS Geodetic Engineering thesis records support 1 to 2 students, while MS thesis and PhD dissertation records require exactly 1 student.

## Prerequisites

- Node.js 24 LTS, declared in `.nvmrc`
- npm 11 or newer

Use npm for package management and commit `package-lock.json` with dependency changes.

## Development

Install dependencies:

```sh
npm ci
```

Start the local development server:

```sh
npm run dev
```

Preview a production build locally:

```sh
npm run preview
```

## Validation

Run the core validation commands before committing implementation changes:

```sh
npm run format:check
npm run check
npm run lint
npm run build
```

Use `npm run format` to apply Prettier formatting.

## Deployment

The production site is deployed automatically to GitHub Pages at:

https://updge-envisage.github.io/

This repository is the organization Pages repository `UPDGE-EnviSAGE/UPDGE-EnviSAGE.github.io`, so the site publishes at the domain root. Astro is configured with `site: "https://updge-envisage.github.io"` and does not use a repository subpath such as `/UPDGE-EnviSAGE.github.io/`.

Deployment runs from `.github/workflows/deploy-pages.yml` on pushes to `main` and can also be started manually with `workflow_dispatch`.

The repository must be configured in GitHub:

Settings → Pages → Build and deployment → Source: GitHub Actions

Do not commit `dist/`; GitHub Actions builds and uploads the static site artifact.

## Project Structure

- `.github/workflows/ci.yml` - CI workflow for pull requests and pushes to `main`
- `.github/workflows/deploy-pages.yml` - GitHub Pages deployment workflow for pushes to `main`
- `astro.config.mjs` - Astro static-site configuration
- `src/content.config.ts` - Astro content collection schemas and validation
- `src/content/` - repository-managed structured content collections
- `src/layouts/` - reusable page layouts
- `src/pages/` - Astro routes
- `src/styles/` - global styles and Tailwind entry point
- `src/components/` - future reusable components
- `src/utils/` - future shared utilities
- `public/` - static public assets
- `public/images/research/` - future optimized, public-approved research visual derivatives
- `docs/FACULTY_PROFILE_GUIDE.md` - maintainer rules for public faculty profile enrichment
- `docs/STUDENT_RESEARCH_MODEL.md` - canonical student research and thesis model
- `docs/UNDERGRADUATE_THESIS_MAINTENANCE.md` - maintainer workflow for internal undergraduate thesis updates
- `docs/STUDENT_RESEARCH_PUBLICATION_GUIDE.md` - maintainer workflow for reviewed student research publication
- `scripts/import-undergraduate-theses.py` - reproducible internal import tool for the Phase 6C undergraduate thesis source workbook
- `scripts/sync-undergraduate-theses.py` - dry-run-first sync tool for the undergraduate thesis maintenance CSV
- `scripts/review-student-research.py` - review CSV generator for student research publication decisions
- `scripts/publish-student-research.py` - dry-run-first publisher for approved student research records
- `data-maintenance/undergraduate-theses.csv` - non-public maintainer editing layer for undergraduate thesis records
- `data-maintenance/student-research-publication-review.csv` - non-public publication review layer for student research records

## Stack

The Phase 1 stack is:

- Astro
- TypeScript
- Tailwind CSS
- Markdown/MDX content collections with schema validation
- GitHub Actions CI

MapLibre GL JS and spatial explorer functionality are planned for later phases.

Future technologies such as Cloud Optimized GeoTIFF, PMTiles, GeoParquet, PostGIS, APIs, object storage, Google Earth Engine, authentication, large-scale data infrastructure, and internal collaboration features are deferred until later phases unless explicitly approved.

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Roadmap](docs/ROADMAP.md)
- [Content model](docs/CONTENT_MODEL.md)
- [Founding Charter](docs/FOUNDING_CHARTER.md)
- [Research Model](docs/RESEARCH_MODEL.md)
- [People Model](docs/PEOPLE_MODEL.md)
- [Faculty Profile Guide](docs/FACULTY_PROFILE_GUIDE.md)
- [Student Research Model](docs/STUDENT_RESEARCH_MODEL.md)
- [Undergraduate Thesis Maintenance Guide](docs/UNDERGRADUATE_THESIS_MAINTENANCE.md)
- [Student Research Publication Guide](docs/STUDENT_RESEARCH_PUBLICATION_GUIDE.md)
- [Design system](docs/DESIGN_SYSTEM.md)
- [Research visual identity](docs/RESEARCH_VISUAL_IDENTITY.md)
- [Contributing guide](docs/CONTRIBUTING.md)
- [Agent instructions](AGENTS.md)

## Data Policy

Large raster, scientific, and raw research datasets must not be committed directly to this repository. The website should initially visualize selected prepared datasets and metadata while source datasets remain in appropriate storage systems such as the laboratory NAS, local research storage, external drives, Google Drive, object storage, or future geospatial data services.
