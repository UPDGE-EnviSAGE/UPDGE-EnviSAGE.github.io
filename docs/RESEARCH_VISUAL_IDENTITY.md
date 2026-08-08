# Research Visual Identity

This document defines how EnviSAGE should prepare, approve, describe, and use research visuals on the public website.

## Purpose

Phase 4A establishes the visual identity framework for future authentic EnviSAGE imagery. It does not add production research images, fabricate maps, download stock imagery, or replace abstract motifs with unsupported scientific visuals.

## Visual Philosophy

EnviSAGE visuals should feel scientific, environmental, geospatial, restrained, and credible. The site may use abstract coordinate grids, contours, raster patterns, and spatial geometry as visual language while approved research images are unavailable.

The public site should look intentional even when the image registry has zero approved entries.

## Decorative Motifs And Scientific Imagery

Decorative geospatial motifs include coordinate grids, contours, raster patterns, and abstract spatial geometry. These are brand and layout devices. They do not represent scientific data.

Authentic research visuals include satellite imagery, remote sensing products, habitat classifications, water-quality maps, LiDAR or hillshade outputs, bathymetry, drone imagery, fieldwork photographs, model outputs, GeoAI outputs, scientific maps, and figures. These must originate from real EnviSAGE research and must have documented provenance and public-use permission.

Never present decorative motifs as real scientific outputs.

## Approved Asset Requirements

Every production research visual must have:

- Known creator or source
- Known research or project context
- Public-use permission
- Meaningful alt text
- Caption where appropriate
- Credit or attribution where appropriate
- Optimized web derivative
- No confidential information
- No unpublished sensitive material
- Scientifically accurate representation

Only visuals with `status: "public-approved"` in the research visual registry are eligible for production rendering.

## Provenance

Visual metadata should explain what the image is, where it came from, and what research context it belongs to. For processed imagery or maps, describe the source data and processing context at a high level without exposing sensitive or unpublished details.

## Copyright And Public-Use Review

Before a visual is used publicly, maintainers must confirm that EnviSAGE has permission to publish the optimized derivative on the website. This applies to satellite products, field photographs, generated maps, figures, and partner-provided visuals.

Do not use stock images, unsourced web images, unpublished private thesis figures, or third-party graphics without clear permission.

## Naming

Use descriptive lowercase kebab-case filenames that include place/theme, visual type, and year where helpful:

- `coastal-calatagan-sentinel-benthic-2025.webp`
- `water-quality-bolinao-chlorophyll-2026.webp`
- `habitat-palawan-mangrove-2025.webp`

Avoid ambiguous names such as:

- `final2.png`
- `map_new_new.png`
- `figure6-revised.png`

## Directories

Optimized public derivatives should live under `public/images/research/`.

Recommended future subdirectories:

- `coastal/`
- `water-quality/`
- `habitats/`
- `terrain/`
- `environmental-monitoring/`
- `geoai/`
- `fieldwork/`

Do not commit raw scientific datasets, large rasters, complete data archives, or unreviewed thesis materials to this repository.

## Registry Fields

The typed registry lives in `src/data/research-visuals.ts` and supports zero entries. Future entries should include:

- `id`
- `src`
- `title`
- `alt`
- `caption`
- `credit`
- `year`
- `location`
- `sourceDescription`
- `researchAreas`
- `project`
- `visualType`
- `roles`
- `status`

Supported visual roles include hero, research theme, project, spatial explorer, dataset, publication, and general use.

## Status Workflow

Use these statuses:

- `draft`
- `internal-review`
- `public-approved`
- `retired`

Only `public-approved` visuals may be rendered as production research imagery. Retired visuals should remain in the registry only if historical context is useful.

## Alt Text

Alt text should describe the visual meaning for users who cannot see the image. For decorative motifs, use empty alt text or hide the motif when the surrounding copy already carries the meaning. For research imagery, describe the subject, geography or context when public, and visual type.

Avoid starting alt text with "image of" unless the medium itself matters.

## Captions

Captions should explain what a viewer is seeing and why it matters. For processed scientific products, clarify enough context to avoid implying unsupported conclusions.

## Credits

Credits should identify the creator, laboratory, partner, dataset provider, or publication context as appropriate. Keep attribution concise and consistent.

## Optimization

Preferred derivative formats:

- WebP for most raster or photographic imagery
- PNG where lossless linework or transparency is required
- SVG only for genuine vector graphics suitable for SVG

Recommended approximate dimensions:

- Hero visuals: around 2400 x 1350 or similar wide format
- Card visuals: around 1200 x 800

Exact dimensions may vary by visual context and aspect ratio. Do not automatically convert scientific figures in this phase.

## Hero Usage

The homepage may use an abstract geospatial motif until an approved hero visual is available. A future hero image should be selected through the registry with the `hero` role and `public-approved` status, and should include strong alt text, caption guidance, source description, and credit.

## Research-Theme Imagery

Research-theme cards may use subtle grid, contour, and raster motifs when no approved thematic image exists. Approved thematic visuals should be connected by research area and role, not hardcoded into each card.

## Project Imagery

Project images should represent reviewed project content. Do not invent project imagery, project titles, study areas, or results. Project visuals should be connected to project metadata once the project catalog is implemented.

## Spatial-Data Imagery

Spatial-data visuals and explorer teasers must distinguish conceptual motifs from real maps, layers, products, and datasets. Scientific maps require source, processing, date, spatial context, legend or explanation where appropriate, and public-use approval.

## Contributor Workflow

Future visual contribution flow:

Researcher or student proposes a visual, confirms source and provenance, confirms public-use permission, prepares an optimized web derivative, provides metadata, caption, credit, and alt text, opens a pull request, receives EnviSAGE review, and updates the registry status to `public-approved` only after approval.

Ongoing thesis materials should remain private until completion and approval for public release.

## Review Checklist

Before approving a visual, confirm:

- The visual comes from real EnviSAGE research or an approved partner/source
- Creator/source and research context are documented
- Public-use permission is clear
- The derivative is optimized for web use
- Alt text is meaningful
- Caption and credit are appropriate
- No confidential, private, sensitive, or unpublished material is exposed
- The visual is scientifically accurate and not misleading
- Registry status is `public-approved` only after review
