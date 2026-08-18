import { researchThemes as approvedResearchThemes } from "./research-taxonomy";

export const researchThemes = approvedResearchThemes.map((theme) => ({
  title: theme.name,
  description: theme.description,
  motif: theme.motif,
}));

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
      "Reproducible methods, code, and data products for environmental research.",
  },
] as const;

export const openResearchFeatures = [
  {
    title: "Student Research",
    description: "Thesis outputs, repositories, notebooks, and maps.",
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
