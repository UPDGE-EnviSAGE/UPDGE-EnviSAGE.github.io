export const peopleRoleLabels = {
  head: "Head",
  "co-head": "Co-Head",
  "faculty-affiliate": "Faculty Affiliate",
  researcher: "Researcher",
  "research-staff": "Research Staff",
  "graduate-researcher": "Graduate Researcher",
  "undergraduate-researcher": "Undergraduate Researcher",
  "thesis-author": "Thesis Author",
  alumni: "Alumni",
} as const;

export const researchAreaLabels = {
  "coastal-marine-systems": "Coastal & Marine Systems",
  "ecosystems-biodiversity-land-change":
    "Ecosystems, Biodiversity & Land Change",
  "water-air-environmental-quality": "Water, Air & Environmental Quality",
  "climate-hazards-resilience": "Climate, Hazards & Resilience",
  "urban-sustainable-systems": "Urban & Sustainable Systems",
} as const;

export const peopleCategorySections = [
  {
    id: "leadership",
    label: "Leadership",
    description: "Laboratory leadership for EnviSAGE research direction.",
  },
  {
    id: "faculty-affiliate",
    label: "Faculty Affiliates",
    description: "Faculty connected to EnviSAGE research and mentoring.",
  },
  {
    id: "researcher",
    label: "Researchers",
    description: "Researchers contributing to EnviSAGE projects and outputs.",
  },
  {
    id: "research-staff",
    label: "Research Staff",
    description: "Staff supporting EnviSAGE research operations.",
  },
  {
    id: "graduate-researcher",
    label: "Graduate Researchers",
    description: "Graduate students connected to EnviSAGE research.",
  },
  {
    id: "undergraduate-researcher",
    label: "Undergraduate Researchers",
    description: "Undergraduate students connected to EnviSAGE research.",
  },
  {
    id: "alumni",
    label: "Alumni",
    description: "Former EnviSAGE members and student researchers.",
  },
] as const;
