# Architecture

This document defines the architecture direction for the EnviSAGE web platform. Phase 1 established the static-site development foundation, and Phase 2 established the visual identity and design-system foundation while keeping final public-page implementation deferred to later phases.

## Goals

The platform should become a public-first research laboratory website and catalog for EnviSAGE. It should support laboratory identity, research communication, project discovery, publications, student research outputs, research tools, and one initial interactive spatial explorer.

The architecture should stay simple enough for faculty, researchers, students, and future maintainers to understand and extend through GitHub pull requests.

`docs/FOUNDING_CHARTER.md` is the canonical identity document for EnviSAGE. Public site copy and future laboratory communication materials should derive their institutional framing from the charter rather than creating independent definitions of the laboratory.

`docs/RESEARCH_MODEL.md` is the canonical research ecosystem model. It defines how research areas, topics, people, projects, theses, outputs, and supporting entities relate conceptually before those concepts are represented in website content schemas or catalog pages.

`docs/PEOPLE_MODEL.md` is the canonical Person architecture for EnviSAGE membership, roles, visibility, and future profile enrichment.

`docs/STUDENT_RESEARCH_MODEL.md` is the canonical thesis and student research architecture for authorship, adviser roles, visibility, imports, GitHub relationships, and future student research catalogs.

## Phase 1 And 2 Stack

The Phase 1 implementation stack is:

- Astro 7 for the static site framework
- TypeScript for typed application and data code
- Tailwind CSS 4 for styling support
- Markdown/MDX content collections with Astro schema validation
- GitHub Actions for CI validation
- npm for package management
- Node.js 24 LTS

MapLibre GL JS, spatial explorer functionality, GitHub Pages deployment automation, and final branding are deferred to later phases.

## Design System Architecture

Phase 2 defines design tokens in `src/styles/global.css` using CSS custom properties and the Tailwind 4 CSS-first theme layer. Reusable Astro primitives live in `src/components/`.

The design system includes:

- Brand, neutral, and semantic color tokens
- System typography stacks
- Content width tokens
- Radius, border, focus, and subtle shadow treatments
- Typographic fallback brand lockups
- Lightweight geospatial motif classes
- A development-only `/design-system` preview route that is available in Astro dev and excluded from production static builds

The historical EnviSAGE logo remains the temporary official logo, but no logo asset is fabricated in this repository. Approved future brand files should be placed in `public/brand/`.

## Hosting Model

The site is configured as a statically generated Astro project deployed to the organization GitHub Pages URL:

https://updge-envisage.github.io/

This repository is `UPDGE-EnviSAGE/UPDGE-EnviSAGE.github.io`, so the site is hosted at the domain root. Astro uses `site: "https://updge-envisage.github.io"` and does not set a repository `base` path.

Deployment automation runs through `.github/workflows/deploy-pages.yml` on pushes to `main`. The workflow builds the site, uploads `dist/` as a GitHub Pages artifact, and deploys it through the official GitHub Pages deployment action.

The repository setting must be configured manually in GitHub: Settings → Pages → Build and deployment → Source: GitHub Actions.

This keeps hosting cost low, reduces operational burden, and matches the repository name `UPDGE-EnviSAGE.github.io`.

The initial platform should not require a server, database, authentication provider, or cloud processing runtime.

## Content Architecture

Content should be stored in the repository as Markdown/MDX and structured data. The content model should support:

- People
- Research areas
- Projects
- Publications
- Student research records
- Research tools
- Datasets and spatial layers
- Training resources

Content should be reviewable through GitHub pull requests.

The content model should translate the canonical research ecosystem from `docs/RESEARCH_MODEL.md` into website-managed records without requiring a database-backed CMS.

People records should follow `docs/PEOPLE_MODEL.md`: one canonical Person per person, public rendering only for `visibility: public`, and empty public categories omitted from directory pages.

Student research records should follow `docs/STUDENT_RESEARCH_MODEL.md`: Thesis records are canonical scholarly records, student Person records are separate identity records, and internal thesis imports must not generate public routes or directory entries until reviewed.

## Repository Structure

The Phase 1 repository structure includes:

- `.github/workflows/ci.yml` for non-deploying CI
- `astro.config.mjs` for static Astro configuration
- `src/content.config.ts` for content collection schema validation
- `src/content/` for repository-managed content collections
- `src/layouts/` for reusable page layouts
- `src/pages/` for Astro routes
- `src/styles/` for global styles and Tailwind
- `src/components/` for future reusable components
- `src/utils/` for future shared utilities
- `public/` for static assets
- `public/brand/` for approved EnviSAGE brand assets when provided
- `public/images/research/` for future optimized, public-approved research visual derivatives

The `/design-system` route is a development preview and is not emitted as production content by `npm run build`.

## Homepage Architecture

Phase 3B replaces the development homepage placeholder with the first production homepage. Reusable homepage presentation components live in `src/components/`, while temporary homepage section definitions live in `src/data/homepage.ts` so broad research themes, research highlights, and open research feature links can later be connected to validated content collections without rewriting the page structure.

Homepage imagery remains static and image-ready. Where approved EnviSAGE research imagery is not yet available, the page uses non-data-bearing geospatial motifs rather than fabricated maps or unsourced imagery.

Phase 4A adds the research visual identity framework through `src/data/research-visuals.ts`, `ResearchVisual`, and `ResearchVisualPlaceholder`. The registry supports zero entries, filters production use to `public-approved` visuals, and keeps decorative motifs separate from authentic research imagery with provenance.

Phase 5A adds the Founding Charter as the highest-level identity document and replaces the `/about/` placeholder with a concise production page distilled from that charter.

Phase 5B replaces the `/research/` placeholder with the public research architecture page. The page remains static-first and catalog-free in this phase. It introduces reusable research-area, topic, connection, and output presentation components backed by typed local data in `src/data/research-architecture.ts`.

The research architecture organizes discovery as:

Research Areas and Topics -> Research Work -> Projects and Theses -> Outputs -> Publications, Datasets, Software, and Dashboards

Projects and Theses are related forms of research work. A Thesis may belong to a Project, or it may exist independently under EnviSAGE. This model prepares future catalogs without requiring a database, CMS, authentication, backend APIs, or geospatial platform integration.

Phase 6A replaces the `/people/` placeholder with a production People directory backed by the Astro `people` content collection. It creates current public leadership and faculty-affiliate records and omits empty categories.

Phase 6B enriches the six current EnviSAGE faculty records and adds static individual faculty profile pages at `/people/{slug}/`. Profiles use reviewed public fields, keep photos optional through a built-in fallback, store Google Scholar URLs without metrics, and render future contribution sections only when reviewed related records exist. The profile curation rules live in `docs/FACULTY_PROFILE_GUIDE.md`.

Phase 6C imports historical BS Geodetic Engineering thesis records associated with EnviSAGE faculty as internal content only. It adds a reproducible workbook importer, internal canonical student Person records, internal Student Research records, explicit main/co-adviser relationships, and an import audit without changing the public site surface.

Phase 6C.1 adds internal QA and a maintainer editing workflow for those undergraduate thesis records. The workflow keeps canonical Person and Student Research files as the website source of truth while using `data-maintenance/undergraduate-theses.csv` as a non-public human editing layer. `scripts/sync-undergraduate-theses.py` is dry-run-first, matches by stable `recordId`, preserves existing slugs where practical, never deletes missing canonical records automatically, and never promotes records to public visibility.

Phase 6D adds the review-gated publication workflow and public Student Research surface. `data-maintenance/student-research-publication-review.csv` is the non-public maintainer approval layer, `scripts/review-student-research.py` regenerates it while preserving decisions, and `scripts/publish-student-research.py` dry-runs by default before applying approved visibility changes. Public `/student-research/` and `/student-research/{slug}/` routes render only `visibility: public` theses.

## Global Site Shell

Phase 3A adds the production global shell through `BaseLayout`, `SiteHeader`, and `SiteFooter`.

The shell provides:

- Skip-to-content link
- Responsive header
- Legacy-logo-aware brand treatment
- Desktop navigation with a keyboard-accessible Resources disclosure
- Mobile menu with `aria-expanded` state
- Centralized navigation configuration in `src/utils/navigation.ts`
- Active/current-page navigation logic
- Restrained institutional footer

Phase 3A placeholder routes exist only to support navigation and shell testing. They should be replaced by substantive pages in later roadmap phases.

## Data Architecture

The website should initially visualize selected prepared datasets rather than act as a large repository. Large raster and scientific datasets must remain outside the repository.

Appropriate repository data includes:

- Metadata
- Small GeoJSON samples when justified
- Small prepared demonstration files
- Thumbnails and optimized web images
- References to external storage or repositories

Student research metadata supports multiple undergraduate thesis authors through `students[]`. BS Geodetic Engineering thesis records must list 1 to 2 students, while MS thesis and PhD dissertation records must list exactly 1 student. Ongoing thesis repositories remain private by default until completion and review.

Undergraduate thesis maintenance uses stable `recordId` values rather than titles as identity keys because ongoing titles can change. The maintainer CSV must remain outside `public/` and is not emitted into the production build.

Student research publication requires explicit review approval. Co-advised-only authors may appear as authors on public thesis pages, but they must not become EnviSAGE alumni or public EnviSAGE member records solely from co-advising.

Inappropriate repository data includes:

- Large rasters
- Raw scientific datasets
- Unreviewed thesis data
- Large archives from NAS, local computers, external drives, or Google Drive

Future data architecture may include Cloud Optimized GeoTIFF, PMTiles, GeoParquet, PostGIS, APIs, object storage, large-scale data infrastructure, and Google Earth Engine. These are deferred until later phases unless explicitly approved.

## Spatial Architecture

The first spatial visualization system should support ordinary GIS functions:

- Pan and zoom
- Layer switching
- Legends
- Feature or location inspection
- Opacity controls
- Basic metadata
- Basic temporal filtering where appropriate

Initial visualization examples should focus on satellite-derived water quality and seagrass, coral, or mangrove mapping.

Advanced analytics, cloud processing, Google Earth Engine integration, authentication, PostGIS, APIs, large-scale data infrastructure, and internal collaboration features are deferred until later phases unless explicitly approved.

## Public and Private Areas

V1 is public-first. A private authenticated collaboration area may be considered later, but it should not complicate the initial architecture.

## Maintainability Rules

- Keep modules and content schemas small and understandable.
- Prefer open standards and static assets where practical.
- Avoid lock-in to one geospatial vendor or proprietary workflow.
- Document architectural changes as they happen.
- Keep implementation decisions aligned with the roadmap.
