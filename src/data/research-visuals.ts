export type ResearchVisualType =
  | "satellite"
  | "habitat-map"
  | "water-quality-map"
  | "terrain"
  | "lidar"
  | "bathymetry"
  | "drone"
  | "fieldwork"
  | "geoai"
  | "scientific-figure"
  | "map"
  | "other";

export type ResearchVisualRole =
  | "hero"
  | "research-theme"
  | "project"
  | "spatial-explorer"
  | "dataset"
  | "publication"
  | "general";

export type ResearchVisualStatus =
  "draft" | "internal-review" | "public-approved" | "retired";

export interface ResearchVisual {
  id: string;
  src: string;
  title: string;
  alt: string;
  caption?: string;
  credit?: string;
  year?: number;
  location?: string;
  sourceDescription: string;
  researchAreas?: string[];
  project?: string;
  visualType: ResearchVisualType;
  roles: ResearchVisualRole[];
  status: ResearchVisualStatus;
}

export const researchVisuals: ResearchVisual[] = [];

export function getApprovedVisuals() {
  return researchVisuals.filter(
    (visual) => visual.status === "public-approved",
  );
}

export function getVisualsByRole(role: ResearchVisualRole) {
  return getApprovedVisuals().filter((visual) => visual.roles.includes(role));
}

export function getHeroVisual() {
  return getVisualsByRole("hero")[0] ?? null;
}

export function getVisualsByResearchArea(researchArea: string) {
  return getApprovedVisuals().filter((visual) =>
    visual.researchAreas?.includes(researchArea),
  );
}
