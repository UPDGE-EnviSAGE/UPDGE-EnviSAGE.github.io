export const researchThemes = [
  {
    title: "Earth Observation & Remote Sensing",
    description:
      "Using satellite, aerial, and field-linked observations to monitor environmental change across land and coastal systems.",
    motif: "grid",
  },
  {
    title: "Coastal & Marine Environments",
    description:
      "Studying water, reef, seagrass, mangrove, and nearshore systems through spatially explicit environmental analysis.",
    motif: "contour",
  },
  {
    title: "Environmental Monitoring & Modeling",
    description:
      "Connecting observations, models, and environmental indicators to support evidence-based assessment and management.",
    motif: "raster",
  },
  {
    title: "Geospatial AI & Spatial Analytics",
    description:
      "Applying spatial statistics, machine learning, and reproducible workflows to environmental data and imagery.",
    motif: "grid",
  },
  {
    title: "Climate, Hazards & Resilience",
    description:
      "Mapping exposure, environmental risk, and landscape change to inform climate and hazard resilience work.",
    motif: "contour",
  },
  {
    title: "Geospatial Data & Decision Support",
    description:
      "Preparing maps, data products, and decision-support interfaces for researchers, communities, and partner agencies.",
    motif: "raster",
  },
] as const;

export const researchHighlights = [
  {
    title: "Environmental observation",
    description:
      "Linking field, satellite, and spatial datasets to characterize environmental conditions and change.",
  },
  {
    title: "Spatial analysis for decisions",
    description:
      "Preparing geospatial evidence that can support research, planning, monitoring, and environmental management.",
  },
  {
    title: "Reusable research workflows",
    description:
      "Building reproducible methods, code, and data products that selected projects can share after review.",
  },
] as const;

export const openResearchFeatures = [
  {
    title: "Student Research",
    description:
      "Selected thesis outputs, reviewed repositories, notebooks, maps, and reproducible workflows.",
    href: "/student-research/",
    linkText: "Open student research",
  },
  {
    title: "Research Tools",
    description:
      "Reusable research code, GitHub repositories, browser-accessible tools, and documentation.",
    href: "/tools/",
    linkText: "Browse research tools",
  },
  {
    title: "Data",
    description:
      "Selected dataset metadata, spatial products, access notes, licenses, and citations.",
    href: "/data/",
    linkText: "View data portal",
  },
] as const;
