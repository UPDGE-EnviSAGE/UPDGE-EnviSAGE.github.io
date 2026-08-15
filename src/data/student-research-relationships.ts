import type { CollectionEntry } from "astro:content";
import { formatPersonDisplayName } from "../utils/display-names";

type PersonEntry = CollectionEntry<"people">;
type ThesisEntry = CollectionEntry<"student-research">;

export type FacultyDirectoryEntry = {
  name: string;
  href: string;
};

export type FacultyAdvisingRecord = {
  thesis: ThesisEntry;
  role: "Main Adviser" | "Co-Adviser";
};

export const isPublicFacultyPerson = (person: PersonEntry) =>
  person.data.visibility === "public" &&
  person.data.membershipStatus === "active" &&
  Boolean(person.data.shortBio) &&
  (person.data.categories.includes("leadership") ||
    person.data.categories.includes("faculty-affiliate"));

export const createFacultyDirectory = (people: readonly PersonEntry[]) =>
  new Map(
    people.filter(isPublicFacultyPerson).map((person) => [
      person.data.slug,
      {
        name: person.data.name,
        href: `/people/${person.data.slug}/`,
      },
    ]),
  );

export const getAdviserHref = (
  adviserSlug: string | undefined,
  facultyDirectory: ReadonlyMap<string, FacultyDirectoryEntry>,
) => (adviserSlug ? facultyDirectory.get(adviserSlug)?.href : undefined);

export const getFacultyAdvisingRecords = (
  theses: readonly ThesisEntry[],
  facultySlug: string,
) => {
  const records: FacultyAdvisingRecord[] = [];

  for (const thesis of theses) {
    if (thesis.data.visibility !== "public") {
      continue;
    }

    if (thesis.data.mainAdviserPerson === facultySlug) {
      records.push({ thesis, role: "Main Adviser" });
      continue;
    }

    if (thesis.data.envisageCoAdvisers.includes(facultySlug)) {
      records.push({ thesis, role: "Co-Adviser" });
    }
  }

  return records.sort(
    (first, second) =>
      (second.thesis.data.year ?? 0) - (first.thesis.data.year ?? 0) ||
      first.thesis.data.thesisTitle.localeCompare(
        second.thesis.data.thesisTitle,
      ),
  );
};

export const getFacultyAdvisingSummary = (
  records: readonly FacultyAdvisingRecord[],
) => {
  const thesisSlugs = new Set<string>();
  const studentIds = new Set<string>();

  for (const record of records) {
    thesisSlugs.add(record.thesis.data.slug);

    record.thesis.data.students.forEach((student, index) => {
      studentIds.add(
        record.thesis.data.studentPeople[index] ??
          formatPersonDisplayName(student),
      );
    });
  }

  return {
    thesesAdvised: thesisSlugs.size,
    studentsAdvised: studentIds.size,
    mainAdvised: records.filter((record) => record.role === "Main Adviser")
      .length,
    coAdvised: records.filter((record) => record.role === "Co-Adviser").length,
  };
};

export const getPublicUndergraduateAlumni = (
  people: readonly PersonEntry[],
  theses: readonly ThesisEntry[],
) => {
  const publicThesesBySlug = new Map(
    theses
      .filter((thesis) => thesis.data.visibility === "public")
      .map((thesis) => [thesis.data.slug, thesis]),
  );

  return people
    .filter(
      (person) =>
        person.data.visibility === "public" &&
        person.data.membershipStatus === "alumni" &&
        person.data.categories.includes("undergraduate-researcher") &&
        person.data.categories.includes("alumni"),
    )
    .map((person) => {
      const thesesForPerson = person.data.studentResearch
        .map((slug) => publicThesesBySlug.get(slug))
        .filter((thesis): thesis is ThesisEntry => Boolean(thesis))
        .sort(
          (first, second) =>
            (second.data.year ?? 0) - (first.data.year ?? 0) ||
            first.data.thesisTitle.localeCompare(second.data.thesisTitle),
        );

      return {
        person,
        displayName: formatPersonDisplayName(person.data.name),
        thesis: thesesForPerson[0],
      };
    })
    .sort(
      (first, second) =>
        (second.thesis?.data.year ?? 0) - (first.thesis?.data.year ?? 0) ||
        first.displayName.localeCompare(second.displayName),
    );
};
