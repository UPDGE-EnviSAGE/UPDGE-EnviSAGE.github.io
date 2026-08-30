import { researchThemes as approvedResearchThemes } from "./research-taxonomy";

export const researchThemes = approvedResearchThemes.map((theme) => ({
  title: theme.name,
  description: theme.description,
  motif: theme.motif,
}));

export const exploreLinks = [
  {
    label: "Research",
    href: "/research/",
  },
  {
    label: "Projects",
    href: "/projects/",
  },
  {
    label: "Publications",
    href: "/publications/",
  },
  {
    label: "Student Research",
    href: "/student-research/",
  },
  {
    label: "People",
    href: "/people/",
  },
  {
    label: "Research Tools",
    href: "/tools/",
  },
  {
    label: "Data",
    href: "/data/",
  },
  {
    label: "Spatial Explorer",
    href: "/explorer/",
  },
] as const;
