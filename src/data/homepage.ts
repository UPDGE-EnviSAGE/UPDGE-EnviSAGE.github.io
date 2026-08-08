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

export const featuredProjectSlots = [
  {
    title: "Featured project slot",
    description:
      "Reserved for a reviewed EnviSAGE project summary once the project catalog is populated.",
    researchArea: "To be assigned from structured content",
    status: "Awaiting approved project content",
  },
  {
    title: "Featured project slot",
    description:
      "Designed for concise project context, research area metadata, status, and an optional approved image.",
    researchArea: "To be assigned from structured content",
    status: "Future content integration",
  },
  {
    title: "Featured project slot",
    description:
      "Ready to connect to validated project entries without changing the homepage layout.",
    researchArea: "To be assigned from structured content",
    status: "Catalog phase pending",
  },
] as const;

export const openResearchFeatures = [
  {
    title: "Student Research",
    description:
      "A future catalog for selected thesis outputs, reviewed repositories, notebooks, maps, and reproducible workflows.",
    href: "/student-research/",
    linkText: "Open student research",
  },
  {
    title: "Research Tools",
    description:
      "A future index of reusable research code, GitHub repositories, browser-accessible tools, and documentation.",
    href: "/tools/",
    linkText: "Browse research tools",
  },
  {
    title: "Data",
    description:
      "A future entry point for selected dataset metadata, spatial products, access notes, licenses, and citations.",
    href: "/data/",
    linkText: "View data portal",
  },
] as const;
