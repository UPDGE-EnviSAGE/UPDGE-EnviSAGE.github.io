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

## Initial Technical Direction

The likely initial stack is:

- Astro
- TypeScript
- Tailwind CSS
- Markdown/MDX or structured content
- MapLibre GL JS
- GitHub Pages
- GitHub Actions

Future technologies such as Cloud Optimized GeoTIFF, PMTiles, GeoParquet, PostGIS, APIs, object storage, Google Earth Engine, authentication, large-scale data infrastructure, and internal collaboration features are deferred until later phases unless explicitly approved.

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Roadmap](docs/ROADMAP.md)
- [Content model](docs/CONTENT_MODEL.md)
- [Contributing guide](docs/CONTRIBUTING.md)
- [Agent instructions](AGENTS.md)

## Data Policy

Large raster, scientific, and raw research datasets must not be committed directly to this repository. The website should initially visualize selected prepared datasets and metadata while source datasets remain in appropriate storage systems such as the laboratory NAS, local research storage, external drives, Google Drive, object storage, or future geospatial data services.
