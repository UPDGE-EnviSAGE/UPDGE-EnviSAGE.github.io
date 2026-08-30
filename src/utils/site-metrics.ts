import { getCollection } from "astro:content";
import { researchThemes } from "../data/research-taxonomy";
import {
  getPublicUndergraduateAlumni,
  isPublicFacultyPerson,
} from "../data/student-research-relationships";

export const getPublicResearchThemeCount = () =>
  researchThemes.filter((theme) => theme.visibility === "public").length;

export const getPublicFacultyCount = async () => {
  const people = await getCollection("people");
  return people.filter(isPublicFacultyPerson).length;
};

export const getPublicPublicationCount = async () => {
  const publications = await getCollection(
    "publications",
    ({ data }) => data.visibility === "public",
  );
  return publications.length;
};

export const getPublicUndergraduateThesisCount = async () => {
  const theses = await getCollection(
    "student-research",
    ({ data }) =>
      data.visibility === "public" &&
      data.thesisType === "bs-geodetic-engineering-thesis",
  );
  return theses.length;
};

export const getPublicAlumniCount = async () => {
  const [people, theses] = await Promise.all([
    getCollection("people", ({ data }) => data.visibility === "public"),
    getCollection(
      "student-research",
      ({ data }) => data.visibility === "public",
    ),
  ]);

  return getPublicUndergraduateAlumni(people, theses).length;
};

export const getHomepageMetrics = async () => [
  {
    value: getPublicResearchThemeCount(),
    label: "Research Themes",
  },
  {
    value: await getPublicFacultyCount(),
    label: "Faculty",
  },
  {
    value: await getPublicPublicationCount(),
    label: "Publications",
  },
  {
    value: await getPublicUndergraduateThesisCount(),
    label: "Undergraduate Theses",
  },
  {
    value: await getPublicAlumniCount(),
    label: "Research Alumni",
  },
];
