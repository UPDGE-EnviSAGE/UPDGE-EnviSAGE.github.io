import { defineCollection } from "astro:content";
import { glob } from "astro/loaders";
import { z } from "astro/zod";

const collectionLoader = (directory: string) =>
  glob({
    pattern: "**/*.{md,mdx}",
    base: `./src/content/${directory}`,
  });

const slug = z
  .string()
  .regex(/^[a-z0-9]+(?:-[a-z0-9]+)*$/, "Use lowercase kebab-case.");

const year = z.number().int().min(1900).max(2100);

const url = z.url();

const doi = z
  .string()
  .regex(/^10\.\d{4,9}\/[-._;()/:A-Z0-9]+$/i, "Use a valid DOI format.")
  .optional();

const relationList = z.array(slug).default([]);

const visibility = z.enum([
  "draft",
  "internal",
  "public",
  "private",
  "archived",
]);

const publicVisibility = z.enum(["private", "internal", "public"]);

const personRole = z.enum([
  "head",
  "co-head",
  "faculty-affiliate",
  "researcher",
  "research-staff",
  "graduate-researcher",
  "undergraduate-researcher",
  "thesis-author",
  "alumni",
]);

const personCategory = z.enum([
  "leadership",
  "faculty-affiliate",
  "researcher",
  "research-staff",
  "graduate-researcher",
  "undergraduate-researcher",
  "thesis-author",
  "alumni",
]);

const membershipStatus = z.enum(["active", "alumni", "inactive"]);

const thesisType = z.enum([
  "bs-geodetic-engineering-thesis",
  "ms-thesis",
  "phd-dissertation",
]);

const thesisStatus = z.enum(["ongoing", "completed", "archived"]);

const adviserRole = z.enum(["main-adviser", "co-adviser"]);

const envisageAssociationBasis = z.enum([
  "main-adviser",
  "co-adviser-only",
  "none",
]);

const people = defineCollection({
  loader: collectionLoader("people"),
  schema: z.object({
    name: z.string().min(1),
    slug,
    envisageRoles: z.array(personRole).min(1),
    categories: z.array(personCategory).min(1),
    membershipStatus,
    displayOrder: z.number().int().optional(),
    institution: z.string().optional(),
    institutionalPosition: z.string().optional(),
    academicProgram: z.string().optional(),
    shortBio: z.string().optional(),
    email: z.email().optional(),
    contactUrl: url.optional(),
    photo: z.string().optional(),
    researchAreas: relationList,
    specializations: z.array(z.string().min(1)).default([]),
    researchInterests: z.array(z.string().min(1)).default([]),
    researchTopics: z.array(slug).default([]),
    projects: relationList,
    theses: relationList,
    publications: relationList,
    datasets: relationList,
    tools: relationList,
    grants: relationList,
    studentResearch: relationList,
    orcid: z.string().optional(),
    googleScholar: url.optional(),
    personalWebsite: url.optional(),
    github: url.optional(),
    importBatch: z.string().optional(),
    visibility: publicVisibility.default("private"),
  }),
});

const researchAreas = defineCollection({
  loader: collectionLoader("research-areas"),
  schema: z.object({
    title: z.string().min(1),
    slug,
    summary: z.string().min(1),
    keywords: z.array(z.string()).default([]),
    people: relationList,
    projects: relationList,
    publications: relationList,
    datasets: relationList,
    tools: relationList,
    visibility: visibility.default("draft"),
  }),
});

const projects = defineCollection({
  loader: collectionLoader("projects"),
  schema: z.object({
    title: z.string().min(1),
    slug,
    summary: z.string().min(1),
    status: z.enum(["planned", "active", "completed", "archived"]),
    startYear: year.optional(),
    endYear: year.optional(),
    funderOrPartner: z.string().optional(),
    team: relationList,
    researchAreas: relationList,
    publications: relationList,
    datasets: relationList,
    tools: relationList,
    externalLinks: z.array(url).default([]),
    featuredImage: z.string().optional(),
    visibility: visibility.default("draft"),
  }),
});

const publications = defineCollection({
  loader: collectionLoader("publications"),
  schema: z.object({
    title: z.string().min(1),
    publicationId: slug.optional(),
    identifier: slug.optional(),
    authors: z.array(z.string()).default([]),
    year: year.optional(),
    publicationType: z.enum([
      "journal-article",
      "conference-paper",
      "book-chapter",
      "report",
      "thesis",
      "preprint",
      "other",
    ]),
    sourceOrVenue: z.string().optional(),
    venue: z.string().optional(),
    abstract: z.string().optional(),
    doi,
    url: url.optional(),
    facultyRelationships: relationList,
    researchThemes: relationList,
    geomaticsApproaches: relationList,
    projects: relationList,
    datasets: relationList,
    tools: relationList,
    keywords: z.array(z.string()).default([]),
    bibliographicStatus: z
      .enum(["source-supported", "verified", "needs-review"])
      .default("needs-review"),
    sourceProvenance: z.string().optional(),
    internalNotes: z.string().optional(),
    visibility: visibility.default("draft"),
  }),
});

const studentResearch = defineCollection({
  loader: collectionLoader("student-research"),
  schema: z
    .object({
      thesisTitle: z.string().min(1),
      slug,
      recordId: slug.optional(),
      importBatch: z.string().optional(),
      sourceRow: z.number().int().optional(),
      thesisType,
      program: z.string().optional(),
      status: thesisStatus.default("ongoing"),
      students: z.array(z.string().min(1)).min(1),
      studentPeople: relationList,
      adviser: z.string().min(1),
      mainAdviserPerson: slug.optional(),
      coAdvisers: z.array(z.string().min(1)).default([]),
      coAdviserPeople: relationList,
      year: year.optional(),
      abstract: z.string().optional(),
      keywords: z.array(z.string()).default([]),
      researchTopics: z.array(slug).default([]),
      researchAreas: relationList,
      envisageAssociated: z.boolean().default(false),
      envisageAssociationBasis: envisageAssociationBasis.default("none"),
      envisageMainAdviser: slug.optional(),
      envisageCoAdvisers: relationList,
      envisageAdviserRoles: z.array(adviserRole).default([]),
      projects: relationList,
      publications: relationList,
      datasets: relationList,
      tools: relationList,
      repository: url.optional(),
      sourceCode: url.optional(),
      notebooks: z.array(url).default([]),
      sampleData: z.array(url).default([]),
      documentation: url.optional(),
      installationInstructions: z.string().optional(),
      exampleOutputs: z.array(url).default([]),
      mapsOrFigures: z.array(url).default([]),
      thesisPdfReference: url.optional(),
      relatedPublication: slug.optional(),
      datasetDoi: doi,
      softwareDoi: doi,
      reviewStatus: z.enum(["ongoing-private", "under-review", "public"]),
      visibility: visibility.default("private"),
    })
    .superRefine((record, context) => {
      if (
        record.thesisType === "bs-geodetic-engineering-thesis" &&
        record.students.length > 2
      ) {
        context.addIssue({
          code: "custom",
          path: ["students"],
          message:
            "BS Geodetic Engineering thesis records must list 1 to 2 students.",
        });
      }

      if (
        (record.thesisType === "ms-thesis" ||
          record.thesisType === "phd-dissertation") &&
        record.students.length !== 1
      ) {
        context.addIssue({
          code: "custom",
          path: ["students"],
          message:
            "MS thesis and PhD dissertation records must list 1 student.",
        });
      }
    }),
});

const researchTools = defineCollection({
  loader: collectionLoader("research-tools"),
  schema: z.object({
    name: z.string().min(1),
    slug,
    summary: z.string().min(1),
    toolLevel: z.enum(["level-1-code", "level-2-browser-tool"]),
    repositoryUrl: url.optional(),
    demoUrl: url.optional(),
    documentationUrl: url.optional(),
    license: z.string().optional(),
    maintainers: relationList,
    projects: relationList,
    publications: relationList,
    datasets: relationList,
    programmingLanguage: z.string().optional(),
    installationInstructions: z.string().optional(),
    exampleOutputs: z.array(url).default([]),
    visibility: visibility.default("draft"),
  }),
});

const datasets = defineCollection({
  loader: collectionLoader("datasets"),
  schema: z.object({
    title: z.string().min(1),
    slug,
    summary: z.string().min(1),
    dataType: z.enum([
      "vector",
      "raster",
      "tabular",
      "imagery",
      "model-output",
      "other",
    ]),
    spatialExtent: z.string().optional(),
    temporalExtent: z.string().optional(),
    coordinateReferenceSystem: z.string().optional(),
    source: z.string().optional(),
    processingMethod: z.string().optional(),
    license: z.string().optional(),
    citation: z.string().optional(),
    storageLocationReference: z.string().optional(),
    publicAccessUrl: url.optional(),
    projects: relationList,
    publications: relationList,
    tools: relationList,
    mapLayerConfig: z.record(z.string(), z.unknown()).optional(),
    legend: z.string().optional(),
    updateFrequency: z.string().optional(),
    visibility: visibility.default("draft"),
  }),
});

const news = defineCollection({
  loader: collectionLoader("news"),
  schema: z.object({
    title: z.string().min(1),
    slug,
    summary: z.string().min(1),
    publishDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    authors: z.array(z.string()).default([]),
    relatedPeople: relationList,
    relatedProjects: relationList,
    tags: z.array(z.string()).default([]),
    visibility: visibility.default("draft"),
  }),
});

export const collections = {
  people,
  "research-areas": researchAreas,
  projects,
  publications,
  "student-research": studentResearch,
  "research-tools": researchTools,
  datasets,
  news,
};
