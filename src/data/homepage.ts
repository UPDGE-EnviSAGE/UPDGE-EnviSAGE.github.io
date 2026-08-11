export const researchThemes = [
  {
    title: "Earth Observation & Remote Sensing",
    description:
      "Satellite, aerial, and field-linked observations of environmental change.",
    motif: "grid",
  },
  {
    title: "Coastal & Marine Environments",
    description:
      "Spatial analysis of water, reefs, seagrass, mangroves, and nearshore systems.",
    motif: "contour",
  },
  {
    title: "Environmental Monitoring & Modeling",
    description: "Environmental indicators, models, and monitoring workflows.",
    motif: "raster",
  },
  {
    title: "Geospatial AI & Spatial Analytics",
    description:
      "Spatial statistics, machine learning, and reproducible analysis.",
    motif: "grid",
  },
  {
    title: "Climate, Hazards & Resilience",
    description:
      "Exposure, risk, and landscape change for climate and hazard resilience.",
    motif: "contour",
  },
  {
    title: "Geospatial Data & Decision Support",
    description:
      "Maps, data products, and decision support for research and partners.",
    motif: "raster",
  },
] as const;

export const researchHighlights = [
  {
    title: "Environmental observation",
    description:
      "Field, satellite, and spatial datasets for environmental change.",
  },
  {
    title: "Spatial analysis for decisions",
    description: "Geospatial evidence for research, planning, and monitoring.",
  },
  {
    title: "Reusable research workflows",
    description:
      "Reproducible methods, code, and data products for reviewed work.",
  },
] as const;

export const openResearchFeatures = [
  {
    title: "Student Research",
    description: "Reviewed thesis outputs, repositories, notebooks, and maps.",
    href: "/student-research/",
    linkText: "Explore student research",
  },
  {
    title: "Research Tools",
    description:
      "Reusable code, GitHub repositories, tools, and documentation.",
    href: "/tools/",
    linkText: "Explore tools",
  },
  {
    title: "Data",
    description:
      "Dataset metadata, spatial products, access notes, and citations.",
    href: "/data/",
    linkText: "Explore data",
  },
] as const;
