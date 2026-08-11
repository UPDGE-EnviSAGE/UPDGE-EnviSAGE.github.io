export type ResearchMotif = "grid" | "contour" | "raster";

export interface ResearchArea {
  title: string;
  description: string;
  methods: readonly string[];
  applications: readonly string[];
  motif: ResearchMotif;
}

export interface ResearchOutput {
  title: string;
  description: string;
}

export const researchAreas: readonly ResearchArea[] = [
  {
    title: "Earth Observation & Remote Sensing",
    description:
      "Satellite, aerial, and field-linked observation of environmental change.",
    methods: [
      "Multispectral and thermal image analysis",
      "SAR and optical remote sensing",
      "Classification and change detection",
    ],
    applications: [
      "Land cover monitoring",
      "Water quality indicators",
      "Coastal habitat assessment",
    ],
    motif: "raster",
  },
  {
    title: "Coastal & Marine Environments",
    description:
      "Spatial study of nearshore water, habitats, ecosystems, and coastal pressures.",
    methods: [
      "Coastal and shoreline mapping",
      "Bathymetric mapping",
      "Habitat classification",
    ],
    applications: [
      "Seagrass, coral, and mangrove mapping",
      "Fisheries and aquaculture contexts",
      "Coastal water assessment",
    ],
    motif: "contour",
  },
  {
    title: "Environmental Monitoring & Modeling",
    description:
      "Indicators and models for tracking environmental conditions over time.",
    methods: [
      "Environmental indicator design",
      "Spatiotemporal analysis",
      "Model integration and validation",
    ],
    applications: [
      "Water quality monitoring",
      "Ecosystem condition tracking",
      "Air and land system assessment",
    ],
    motif: "grid",
  },
  {
    title: "Geospatial AI & Spatial Analytics",
    description:
      "Machine learning, spatial statistics, and reproducible environmental analysis.",
    methods: [
      "Geospatial machine learning",
      "Feature extraction",
      "Spatial statistics and pattern analysis",
    ],
    applications: [
      "Image interpretation",
      "Environmental pattern detection",
      "Decision-ready spatial products",
    ],
    motif: "raster",
  },
  {
    title: "Climate, Hazards & Resilience",
    description:
      "Mapping exposure, risk, and change for climate and hazard resilience.",
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
    motif: "contour",
  },
  {
    title: "Geospatial Data & Decision Support",
    description:
      "Maps, metadata, tools, and interfaces for usable spatial evidence.",
    methods: [
      "Cartographic design",
      "Metadata and data product design",
      "Dashboard and repository workflows",
    ],
    applications: [
      "Public communication",
      "Agency and partner support",
      "Reusable geospatial evidence",
    ],
    motif: "grid",
  },
] as const;

export const researchTopics = [
  "Water Quality",
  "Mangroves",
  "Seagrass",
  "Coral Reefs",
  "Flooding",
  "Air Quality",
  "PM2.5",
  "Bathymetry",
  "LiDAR",
  "Biodiversity",
  "Climate Change",
  "Agriculture",
  "Fisheries",
  "Aquaculture",
  "Land Cover",
] as const;

export const researchOutputs: readonly ResearchOutput[] = [
  {
    title: "Publications",
    description: "Papers, theses, reports, and citable scholarly records.",
  },
  {
    title: "Datasets",
    description: "Documented metadata and selected prepared data products.",
  },
  {
    title: "Software",
    description: "Reviewed code, notebooks, packages, and workflows.",
  },
  {
    title: "Maps & Dashboards",
    description: "Spatial views of selected layers, indicators, and results.",
  },
  {
    title: "Technical Reports",
    description: "Applied documentation for partners and collaborators.",
  },
  {
    title: "GitHub Repositories",
    description: "Public code, examples, thesis outputs, and documentation.",
  },
] as const;
