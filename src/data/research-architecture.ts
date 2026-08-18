import {
  geomaticsApproaches,
  researchThemes,
  type ResearchMotif,
} from "./research-taxonomy";

export type { ResearchMotif };

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

export const researchAreas: readonly ResearchArea[] = researchThemes.map(
  (theme) => ({
    title: theme.name,
    description: theme.description,
    methods: theme.methods,
    applications: theme.applications,
    motif: theme.motif,
  }),
);

export const researchApproaches = geomaticsApproaches;

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
