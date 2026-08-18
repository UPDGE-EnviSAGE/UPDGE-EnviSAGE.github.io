export type ResearchMotif = "grid" | "contour" | "raster";

export interface ResearchTheme {
  slug: string;
  name: string;
  description: string;
  methods: readonly string[];
  applications: readonly string[];
  displayOrder: number;
  visibility: "public";
  motif: ResearchMotif;
}

export interface GeomaticsApproach {
  slug: string;
  name: string;
  description: string;
  displayOrder: number;
  visibility: "public";
}

export const researchThemes: readonly ResearchTheme[] = [
  {
    slug: "coastal-marine-systems",
    name: "Coastal & Marine Systems",
    description:
      "Spatial study of nearshore water, benthic habitats, coastal ecosystems, and marine pressures.",
    methods: [
      "Coastal and shoreline mapping",
      "Water quality and ocean color analysis",
      "Habitat classification",
    ],
    applications: [
      "Seagrass, coral, and mangrove mapping",
      "Fisheries and aquaculture contexts",
      "Coastal water assessment",
    ],
    displayOrder: 1,
    visibility: "public",
    motif: "contour",
  },
  {
    slug: "ecosystems-biodiversity-land-change",
    name: "Ecosystems, Biodiversity & Land Change",
    description:
      "Environmental mapping of habitats, vegetation, biodiversity contexts, land cover, and landscape change.",
    methods: [
      "Land cover classification",
      "Change detection",
      "Habitat and vegetation mapping",
    ],
    applications: [
      "Biodiversity and conservation planning",
      "Forest and mangrove change",
      "Agricultural and ecosystem monitoring",
    ],
    displayOrder: 2,
    visibility: "public",
    motif: "raster",
  },
  {
    slug: "water-air-environmental-quality",
    name: "Water, Air & Environmental Quality",
    description:
      "Indicators, models, and spatial evidence for environmental quality across water, air, and land systems.",
    methods: [
      "Environmental indicator design",
      "Spatiotemporal analysis",
      "Model integration and validation",
    ],
    applications: [
      "Satellite-derived water quality",
      "Air quality assessment",
      "Environmental exposure mapping",
    ],
    displayOrder: 3,
    visibility: "public",
    motif: "grid",
  },
  {
    slug: "climate-hazards-resilience",
    name: "Climate, Hazards & Resilience",
    description:
      "Mapping exposure, risk, climate-sensitive change, and resilience for communities and landscapes.",
    methods: [
      "Hazard and exposure mapping",
      "Landscape change analysis",
      "Risk and vulnerability overlays",
    ],
    applications: [
      "Flooding and hazards",
      "Climate-sensitive landscapes",
      "Resilience planning support",
    ],
    displayOrder: 4,
    visibility: "public",
    motif: "contour",
  },
  {
    slug: "urban-sustainable-systems",
    name: "Urban & Sustainable Systems",
    description:
      "Geospatial analysis of urban environments, infrastructure, public spaces, and sustainability transitions.",
    methods: [
      "Urban spatial analytics",
      "Suitability and accessibility analysis",
      "Geovisualization for planning",
    ],
    applications: [
      "Urban heat and comfort",
      "Sustainable land-use planning",
      "Infrastructure and service access",
    ],
    displayOrder: 5,
    visibility: "public",
    motif: "grid",
  },
] as const;

export const geomaticsApproaches: readonly GeomaticsApproach[] = [
  {
    slug: "earth-observation-remote-sensing",
    name: "Earth Observation & Remote Sensing",
    description:
      "Satellite, aerial, and field-linked observation of environmental conditions and change.",
    displayOrder: 1,
    visibility: "public",
  },
  {
    slug: "gis-spatial-analytics",
    name: "GIS & Spatial Analytics",
    description:
      "Spatial analysis, GIS workflows, and map-based synthesis for environmental evidence.",
    displayOrder: 2,
    visibility: "public",
  },
  {
    slug: "geoai-spatial-data-science",
    name: "GeoAI & Spatial Data Science",
    description:
      "Machine learning, spatial data science, and reproducible analysis for geospatial research.",
    displayOrder: 3,
    visibility: "public",
  },
  {
    slug: "lidar-photogrammetry-3d-geomatics",
    name: "LiDAR, Photogrammetry & 3D Geomatics",
    description:
      "Point clouds, close-range and aerial photogrammetry, UAS mapping, and 3D spatial products.",
    displayOrder: 4,
    visibility: "public",
  },
  {
    slug: "environmental-spatial-modeling",
    name: "Environmental & Spatial Modeling",
    description:
      "Models that connect environmental processes, spatial patterns, and decision-relevant scenarios.",
    displayOrder: 5,
    visibility: "public",
  },
  {
    slug: "geovisualization-decision-support",
    name: "Geovisualization & Decision Support",
    description:
      "Maps, dashboards, visual interfaces, and communication products that make spatial evidence usable.",
    displayOrder: 6,
    visibility: "public",
  },
] as const;

export const researchThemeLabels = Object.fromEntries(
  researchThemes.map((theme) => [theme.slug, theme.name]),
);

export const geomaticsApproachLabels = Object.fromEntries(
  geomaticsApproaches.map((approach) => [approach.slug, approach.name]),
);
