# AGENTS.md

Persistent instructions for Codex agents working on the EnviSAGE web platform.

## Project Purpose

This repository supports Environmental Systems Applications of Geomatics Engineering (EnviSAGE), the research laboratory of the UP Department of Geodetic Engineering focusing on the use of Geomatics and geospatial technologies in addressing environmental issues. The platform should present EnviSAGE as a clean, modern, professional, geospatial, environmental, research-oriented laboratory with its own visual identity while clearly acknowledging UP and the UP Department of Geodetic Engineering.

## Engineering Principles

- Favor simplicity, maintainability, accessibility, performance, open standards, reproducibility, modular architecture, clear documentation, low hosting cost, and minimal vendor lock-in.
- Avoid premature complexity.
- Do not introduce unnecessary frameworks, backend infrastructure, authentication, PostGIS, APIs, large-scale data infrastructure, cloud processing, internal collaboration features, or vendor-specific services.
- Prefer repository-managed structured content and Markdown/MDX over a WordPress-style CMS.
- Keep public-first architecture separate from any possible future private collaboration platform.

## Naming Conventions

- Use `EnviSAGE` for the laboratory name in prose.
- Use lowercase kebab-case for routes, filenames, content slugs, and asset names unless a framework convention requires otherwise.
- Use descriptive names for research areas, projects, people, publications, datasets, and tools.
- Keep content identifiers stable once published.

## Accessibility and Responsive Design

- All public pages must be usable on desktop, tablet, and mobile viewports.
- Use semantic HTML, readable heading order, descriptive link text, keyboard-accessible controls, visible focus states, and sufficient color contrast.
- Maps and dashboards must include non-map context where practical, including legends, metadata, and text alternatives or summaries for important spatial information.

## Test and Build Expectations

- Before completing implementation changes, run the relevant format, lint, type-check, build, and test commands available in the repository.
- For this npm-based Astro foundation, use Node.js 24 LTS and npm.
- Run `npm run format:check`, `npm run check`, `npm run lint`, and `npm run build` before committing implementation changes.
- If a command cannot be run, document why in the final response.
- Do not add test tooling before the project stack is established, but once established, keep verification lightweight and reliable.

## Content and Data Separation

- Keep site content, metadata, and configuration in repository-managed Markdown/MDX or structured data files.
- Maintain Astro content collection schema validation in `src/content.config.ts` for major content entities.
- Keep large raster, scientific, raw, and derived research datasets outside this repository.
- Commit only lightweight sample data, prepared web data, metadata, thumbnails, and small demonstration assets when appropriate.
- Document external data sources, licenses, update procedures, and processing assumptions.

## Spatial and Research Tool Guidance

- The first spatial examples should focus on satellite-derived water quality and seagrass, coral, or mangrove mapping.
- Initial map functionality should cover pan and zoom, layer switching, legends, feature or location inspection, opacity controls, basic metadata, and basic temporal filtering where appropriate.
- Defer Google Earth Engine integration until a later phase unless explicitly approved.
- V1 should support open research code hosted in GitHub repositories and selected browser-accessible tools where technically appropriate.
- Do not build a general cloud-processing platform in v1.

## Documentation Discipline

- Update documentation whenever architectural decisions, data policies, workflows, or content models change.
- Keep roadmap changes explicit in `docs/ROADMAP.md`.
- Keep data and content schema changes explicit in `docs/CONTENT_MODEL.md`.
- Keep contributor-facing process changes explicit in `docs/CONTRIBUTING.md`.
