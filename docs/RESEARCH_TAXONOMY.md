# Research Taxonomy

Status: Canonical Phase 6F taxonomy

This document defines the approved public taxonomy for EnviSAGE research discovery. Public pages should use the term **Research Themes** for lab-wide domains. The internal schema key `researchAreas` may remain in place for compatibility with earlier content until a future migration is explicitly approved.

## Research Themes

1. Coastal & Marine Systems
2. Ecosystems, Biodiversity & Land Change
3. Water, Air & Environmental Quality
4. Climate, Hazards & Resilience
5. Urban & Sustainable Systems

Research Themes describe broad environmental systems and problem domains. A project, thesis, publication, dataset, tool, or person may connect to more than one theme.

## Cross-Cutting Geomatics Approaches

1. Earth Observation & Remote Sensing
2. GIS & Spatial Analytics
3. GeoAI & Spatial Data Science
4. LiDAR, Photogrammetry & 3D Geomatics
5. Environmental & Spatial Modeling
6. Geovisualization & Decision Support

Geomatics Approaches describe methods and capabilities used across Research Themes. Do not use approaches as a replacement for Research Themes.

## Faculty Specializations

Faculty specializations are person-specific expertise statements. They are not the same as Research Themes, and they should not be inferred from thesis titles, publication titles, or broad taxonomy assignments unless explicitly reviewed.

## Implementation

The approved taxonomy is represented in `src/data/research-taxonomy.ts`. Public pages should import from that file or from compatibility wrappers that draw from it.

The public vocabulary is:

- Research Themes
- Geomatics Approaches
- Research Topics

Use `Research Areas` only when referring to legacy schema fields, historical phase names, or older content architecture that has not yet been migrated.
