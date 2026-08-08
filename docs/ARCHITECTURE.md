# Architecture

This document defines the initial architecture direction for the EnviSAGE web platform. It is intentionally conservative because Phase 0 establishes governance before implementation.

## Goals

The platform should become a public-first research laboratory website and catalog for EnviSAGE. It should support laboratory identity, research communication, project discovery, publications, student research outputs, research tools, and one initial interactive spatial explorer.

The architecture should stay simple enough for faculty, researchers, students, and future maintainers to understand and extend through GitHub pull requests.

## Initial Stack Direction

The likely initial implementation stack is:

- Astro for the static site framework
- TypeScript for typed application and data code
- Tailwind CSS for styling
- Markdown/MDX or structured content collections for repository-managed content
- MapLibre GL JS for browser-based interactive maps
- GitHub Pages for hosting
- GitHub Actions for automated deployment

These choices are not yet installed in Phase 0. They should be introduced in Phase 1 only after the project foundation is ready.

## Hosting Model

The site should be statically generated and deployed from GitHub to GitHub Pages. This keeps hosting cost low, reduces operational burden, and matches the repository name `UPDGE-EnviSAGE.github.io`.

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
