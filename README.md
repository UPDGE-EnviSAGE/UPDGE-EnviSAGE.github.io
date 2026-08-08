# Environmental Systems Applications of Geomatics Engineering

Environmental Systems Applications of Geomatics Engineering (EnviSAGE) is the research laboratory of the UP Department of Geodetic Engineering focusing on the use of Geomatics and geospatial technologies in addressing environmental issues.

This repository is the GitHub Pages organization repository for the EnviSAGE web platform.

The platform is public-first. Future internal collaboration features should be deferred until later phases unless explicitly approved.

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
- Research areas
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

## Project Structure

- `.github/workflows/ci.yml` - CI workflow for pull requests and pushes to `main`
- `astro.config.mjs` - Astro static-site configuration
- `src/content.config.ts` - Astro content collection schemas and validation
- `src/content/` - repository-managed structured content collections
- `src/layouts/` - reusable page layouts
- `src/pages/` - Astro routes
- `src/styles/` - global styles and Tailwind entry point
- `src/components/` - future reusable components
- `src/utils/` - future shared utilities
- `public/` - static public assets

## Stack

The Phase 1 stack is:

- Astro
- TypeScript
- Tailwind CSS
- Markdown/MDX content collections with schema validation
- GitHub Actions CI

MapLibre GL JS, spatial explorer functionality, and GitHub Pages deployment automation are planned for later phases.

Future technologies such as Cloud Optimized GeoTIFF, PMTiles, GeoParquet, PostGIS, APIs, object storage, Google Earth Engine, authentication, large-scale data infrastructure, and internal collaboration features are deferred until later phases unless explicitly approved.

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Roadmap](docs/ROADMAP.md)
- [Content model](docs/CONTENT_MODEL.md)
- [Design system](docs/DESIGN_SYSTEM.md)
- [Contributing guide](docs/CONTRIBUTING.md)
- [Agent instructions](AGENTS.md)

## Data Policy

Large raster, scientific, and raw research datasets must not be committed directly to this repository. The website should initially visualize selected prepared datasets and metadata while source datasets remain in appropriate storage systems such as the laboratory NAS, local research storage, external drives, Google Drive, object storage, or future geospatial data services.
