# Architecture

This document defines the architecture direction for the EnviSAGE web platform. Phase 1 established the static-site development foundation, and Phase 2 established the visual identity and design-system foundation while keeping final public-page implementation deferred to later phases.

## Goals

The platform should become a public-first research laboratory website and catalog for EnviSAGE. It should support laboratory identity, research communication, project discovery, publications, student research outputs, research tools, and one initial interactive spatial explorer.

The architecture should stay simple enough for faculty, researchers, students, and future maintainers to understand and extend through GitHub pull requests.

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

The site is configured as a statically generated Astro project suitable for GitHub Pages. Deployment automation is intentionally deferred beyond Phase 1. This keeps hosting cost low, reduces operational burden, and matches the repository name `UPDGE-EnviSAGE.github.io`.

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

The current homepage is a minimal development placeholder using Phase 2 tokens and is not the final EnviSAGE homepage. The `/design-system` route is a development preview and is not emitted as production content by `npm run build`.

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
