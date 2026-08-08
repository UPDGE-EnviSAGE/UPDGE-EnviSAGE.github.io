# Design System

Phase 2 establishes the EnviSAGE visual identity and design-system foundation. It does not redesign the historical logo, build final public pages, or introduce production research content.

## Design Philosophy

The EnviSAGE interface should feel clean, modern, scientific, geospatial, environmental, research-oriented, highly legible, and professional. The default experience is a light scientific interface with off-white backgrounds, dark charcoal/navy text, restrained borders, minimal shadows, generous whitespace, and clear hierarchy.

The site should avoid looking like a generic university department template, a generic sustainability NGO website, a dark technology dashboard, a futuristic gaming interface, or a corporate marketing landing page.

## Historical Brand Relationship

The existing EnviSAGE logo has long used blue, green, a globe/grid motif, an EnviSAGE wordmark, and glossy/3D styling. Phase 2 treats that logo as the temporary official logo and plans for a modern evolution rather than a full rejection of the established identity.

Future identity work should preserve conceptual continuity with blue, green, Earth/globe, spatial/geodetic grid, environmental science, and geospatial science while simplifying gradients, bevels, shadows, and small-scale globe details where appropriate.

## Color Palette

The palette preserves blue and green as dominant identity colors while modernizing them for a restrained research interface.

| Token                      | Value     | Purpose                                                  |
| -------------------------- | --------- | -------------------------------------------------------- |
| `--color-brand-blue`       | `#0b5fa5` | Geospatial, water, Earth observation, technical identity |
| `--color-brand-blue-deep`  | `#083d77` | Darker blue for hierarchy and emphasis                   |
| `--color-brand-green`      | `#1f8a5b` | Ecosystems and environmental applications                |
| `--color-brand-green-deep` | `#12613f` | Darker green for accessible labels                       |
| `--color-coastal`          | `#0e7c86` | Restrained coastal/data support                          |
| `--color-bathymetry`       | `#2b6cb0` | Map and depth-adjacent support                           |
| `--color-land`             | `#7a8f52` | Terrestrial/environmental support                        |
| `--color-atmosphere`       | `#dbeafe` | Light atmospheric support                                |
| `--color-background`       | `#f7f9f8` | Default page background                                  |
| `--color-surface`          | `#ffffff` | Cards and panels                                         |
| `--color-surface-muted`    | `#eef4f1` | Muted sections                                           |
| `--color-text`             | `#13201f` | Primary text                                             |
| `--color-muted`            | `#5d6b69` | Secondary text                                           |
| `--color-border`           | `#d7e2df` | Subtle boundaries                                        |
| `--color-link`             | `#0b5fa5` | Links                                                    |
| `--color-focus`            | `#0f766e` | Keyboard focus                                           |

These tokens are defined in `src/styles/global.css` and exposed to Tailwind through the Tailwind 4 CSS-first theme layer.

## Typography

The typography system uses privacy-conscious system font stacks instead of external web fonts:

- Primary sans: `"Source Sans 3", Aptos, "Segoe UI", ui-sans-serif, system-ui, sans-serif`
- Mono/data: `"IBM Plex Mono", "SFMono-Regular", Consolas, "Liberation Mono", monospace`

The system prioritizes readability, clear hierarchy, strong numerals, and reliable mobile rendering. Avoid ornamental typefaces or adding more font families without a clear accessibility or content need.

## Spacing

Spacing uses Tailwind's default scale plus repository-level content width tokens:

- `--content-width-narrow`: `48rem`
- `--content-width`: `72rem`
- `--content-width-wide`: `88rem`

Prefer the `Container` and `Section` components for page rhythm instead of one-off spacing decisions.

## Layout And Content Widths

Use constrained content widths for readable text and wider containers for comparison grids, design previews, and future catalog layouts. Avoid full-width text blocks on wide screens.

Responsive spacing should work from small mobile through wide desktop. Do not tune layouts only for desktop.

## Cards And Surfaces

Cards use restrained borders, small radii, white surfaces, and subtle shadows. Avoid nested cards and heavy decorative shadows.

Current surface tokens:

- `--radius-card`: `0.5rem`
- `--radius-control`: `0.375rem`
- `--shadow-subtle`: `0 1px 2px rgb(15 23 42 / 0.06)`

## Buttons And Links

Buttons are implemented as clear link-buttons for Phase 2. Use them for primary or secondary commands and avoid overusing them for ordinary text links.

All interactive elements must have visible keyboard focus. Link text should be descriptive.

## Imagery Strategy

Future imagery should prioritize authentic or scientifically meaningful EnviSAGE material:

- Sentinel-2 or Landsat imagery
- Coastal Earth observation imagery
- Coral reefs, seagrass, and mangroves
- Water-quality maps
- False-color satellite composites
- Bathymetry and environmental monitoring maps
- Remote sensing outputs
- Drone imagery and geospatial fieldwork

Phase 2 does not add copyrighted or unsourced external imagery. Use `ImageFrame` placeholders until approved imagery is available.

## Geospatial Visual Motifs

Subtle motifs may reference coordinate grids, latitude/longitude lines, topographic or bathymetric contours, raster pixels, map geometry, spatial sampling patterns, spectral imagery, and environmental gradients.

Do not fabricate geographic boundaries or scientific data. Use motifs as low-intensity background and placeholder treatments, not as decorative clutter.

## Logo Usage Strategy

The historical EnviSAGE logo remains the temporary official logo. No logo file is currently committed, and Phase 2 does not create a replacement logo.

Approved assets should later live in `public/brand/`. Planned asset names are documented in `public/brand/README.md`.

Until approved assets are provided, use typographic fallback lockups:

1. Compact: `EnviSAGE`
2. Standard: `EnviSAGE` plus full laboratory name
3. Institutional: standard lockup plus `Research Laboratory` and `UP Department of Geodetic Engineering`

## UP DGE Affiliation Hierarchy

The hierarchy is:

1. Primary: `EnviSAGE`
2. Secondary: `Environmental Systems Applications of Geomatics Engineering`
3. Institutional: `Research Laboratory`, `UP Department of Geodetic Engineering`

UP DGE affiliation should be visible, but the website should retain EnviSAGE's laboratory identity and should not mimic the main UP website. Do not add UP logos or seals unless approved assets are provided.

## Accessibility

Maintain semantic HTML, meaningful page titles, visible focus states, sufficient color contrast, accessible links and buttons, appropriate heading hierarchy, and responsive text sizing. Respect reduced-motion preferences when transitions or animation are introduced.

Phase 2 uses minimal color transitions and no animation libraries.

## Responsive Principles

Design primitives should work across small mobile, tablet, laptop, and wide desktop sizes. Components should wrap gracefully, avoid fixed text widths that cause overflow, and keep readable line lengths.

## Development Preview

`/design-system` is a development-only preview route. It is not linked from the public homepage and is not production content.

Future production rendering should use reviewed content entries with `visibility: public`. If the design-system route should be excluded from production later, move it behind an environment-controlled route, remove it before release, or exclude it through Astro routing/build configuration as part of the release workflow.

## Contributor Guidelines

- Use design tokens instead of arbitrary colors.
- Keep blue and green dominant.
- Preserve a light scientific interface by default.
- Use geospatial motifs subtly.
- Do not add external imagery without approval and source documentation.
- Do not fabricate logos, maps, boundaries, or scientific data.
- Keep components simple, accessible, responsive, and content-agnostic.
- Update this document when design tokens or visual rules change.
