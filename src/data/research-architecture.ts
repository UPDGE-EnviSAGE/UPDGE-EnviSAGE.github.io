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
      "Observing environmental change through satellite, aerial, and field-linked geospatial measurements.",
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
      "Studying nearshore systems where water, land, ecosystems, communities, and climate pressures meet.",
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
      "Connecting observations, indicators, and models to understand environmental conditions over time.",
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
      "Applying spatial statistics, machine learning, and reproducible workflows to environmental data.",
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
      "Mapping exposure, risk, and environmental change to support climate and hazard resilience.",
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
      "Preparing maps, metadata, tools, and interfaces that help research evidence become usable.",
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

export const researchConnections = [
  {
    title: "Research Areas & Topics",
    description:
      "Broad themes and flexible topic tags organize environmental and geomatics questions.",
  },
  {
    title: "Research Work",
    description:
      "Formal projects and student theses apply methods to specific questions. A thesis may also stand independently from a funded project.",
  },
  {
    title: "Projects & Theses",
    description:
      "Projects and theses may connect to each other, but neither is required to contain the other.",
  },
  {
    title: "Outputs",
    description:
      "Research work can produce maps, code, datasets, dashboards, reports, repositories, and scholarly records.",
  },
  {
    title: "Publications, Datasets, Software & Dashboards",
    description:
      "Discoverable public records that help users trace evidence and reuse reviewed work.",
  },
] as const;

export const researchOutputs: readonly ResearchOutput[] = [
  {
    title: "Publications",
    description:
      "Peer-reviewed papers, conference outputs, theses, reports, and other citable research records.",
  },
  {
    title: "Datasets",
    description:
      "Documented metadata and selected prepared data products, with large source data kept outside the website repository.",
  },
  {
    title: "Software",
    description:
      "Reviewed code, scripts, notebooks, packages, and reproducible workflows hosted through appropriate repositories.",
  },
  {
    title: "Interactive dashboards",
    description:
      "Browser-based interfaces that communicate selected spatial layers, indicators, and research results.",
  },
  {
    title: "Maps",
    description:
      "Static and web-ready maps that communicate environmental patterns, monitoring results, and decision context.",
  },
  {
    title: "Technical reports",
    description:
      "Applied documentation prepared for partners, agencies, communities, and research collaborators.",
  },
  {
    title: "GitHub repositories",
    description:
      "Reviewed public repositories for tools, thesis outputs, examples, and supporting documentation.",
  },
] as const;
