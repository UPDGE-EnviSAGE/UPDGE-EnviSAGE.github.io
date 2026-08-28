#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import YAML from "yaml";

const root = process.cwd();
const publicationDir = path.join(root, "src/content/publications");
const peopleDir = path.join(root, "src/content/people");
const studentResearchDir = path.join(root, "src/content/student-research");
const distDir = path.join(root, "dist");
const venueAuditPath = path.join(
  root,
  "data-maintenance/publication-venue-display-audit.csv",
);

const approvedThemes = new Set([
  "coastal-marine-systems",
  "ecosystems-biodiversity-land-change",
  "water-air-environmental-quality",
  "climate-hazards-resilience",
  "urban-sustainable-systems",
]);

const noTitlePattern = /^\(?\s*no\s+title\s*\)?$/iu;

const normalizeForComparison = (value) =>
  String(value ?? "")
    .trim()
    .toLocaleLowerCase("en")
    .replace(/[^\p{L}\p{N}]+/gu, " ")
    .replace(/\s+/gu, " ")
    .trim();

const readMarkdownCollection = (directory) =>
  fs
    .readdirSync(directory)
    .filter((filename) => filename.endsWith(".md") || filename.endsWith(".mdx"))
    .map((filename) => {
      const filepath = path.join(directory, filename);
      const source = fs.readFileSync(filepath, "utf8");
      const match = source.match(/^---\n([\s\S]*?)\n---/u);
      if (!match) {
        throw new Error(`Missing frontmatter: ${filepath}`);
      }
      return {
        filename,
        filepath,
        data: YAML.parse(match[1]) ?? {},
      };
    });

const csvEscape = (value) => {
  const text = String(value ?? "");
  return /[",\n\r]/u.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
};

const classifyVenue = (sourceOrVenue, title) => {
  const value = String(sourceOrVenue ?? "").trim();
  if (!value) {
    return {
      display_classification: "D",
      display_issue: "No source or venue value is available.",
      recommended_display_action:
        "Omit the venue line unless a DOI is present.",
    };
  }
  if (noTitlePattern.test(value)) {
    return {
      display_classification: "C",
      display_issue: "The source or venue value is a no-title placeholder.",
      recommended_display_action:
        "Omit the venue from public display and preserve the source value for later bibliographic correction.",
    };
  }
  const normalizedValue = normalizeForComparison(value);
  const normalizedTitle = normalizeForComparison(title);

  if (
    normalizedValue === normalizedTitle ||
    (normalizedValue.length > 20 && normalizedTitle.includes(normalizedValue))
  ) {
    return {
      display_classification: "C",
      display_issue:
        "The source or venue value repeats or appears to be part of the publication title.",
      recommended_display_action:
        "Omit the venue from public display and preserve the source value for later bibliographic correction.",
    };
  }
  if (value.includes("…") || value.endsWith("...")) {
    return {
      display_classification: "B",
      display_issue:
        "The source or venue appears truncated but remains meaningful.",
      recommended_display_action:
        "Display the existing source or venue without fabricating a completion.",
    };
  }
  return {
    display_classification: "A",
    display_issue: "",
    recommended_display_action: "Display the existing source or venue.",
  };
};

const walk = (directory) => {
  if (!fs.existsSync(directory)) return [];
  return fs.readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const filepath = path.join(directory, entry.name);
    return entry.isDirectory() ? walk(filepath) : [filepath];
  });
};

const publications = readMarkdownCollection(publicationDir);
const publicPublications = publications.filter(
  ({ data }) => data.visibility === "public",
);
const canonicalPublications = publications.filter(
  ({ data }) => data.identifier !== "development-fixture",
);
const people = readMarkdownCollection(peopleDir);
const theses = readMarkdownCollection(studentResearchDir);

const venueRows = publicPublications
  .slice()
  .sort(
    (first, second) =>
      Number(second.data.year ?? 0) - Number(first.data.year ?? 0) ||
      String(first.data.title).localeCompare(String(second.data.title)),
  )
  .map(({ data }) => ({
    publication_id: data.publicationId ?? data.identifier ?? "",
    year: data.year ?? "",
    title: data.title ?? "",
    source_or_venue: data.sourceOrVenue ?? "",
    ...classifyVenue(data.sourceOrVenue, data.title),
  }));

const csvFields = [
  "publication_id",
  "year",
  "title",
  "source_or_venue",
  "display_classification",
  "display_issue",
  "recommended_display_action",
];

fs.writeFileSync(
  venueAuditPath,
  [
    csvFields.join(","),
    ...venueRows.map((row) =>
      csvFields.map((field) => csvEscape(row[field])).join(","),
    ),
    "",
  ].join("\n"),
);

const invalidThemeCount = publicPublications.reduce(
  (count, { data }) =>
    count +
    (data.researchThemes ?? []).filter((theme) => !approvedThemes.has(theme))
      .length,
  0,
);

const missingPublicYear = publicPublications.filter(
  ({ data }) => !data.year,
).length;

const distHtml = walk(distDir)
  .filter((filepath) => filepath.endsWith(".html"))
  .map((filepath) => fs.readFileSync(filepath, "utf8"))
  .join("\n");

const forbiddenDistPatterns = [
  /bibliographicStatus/iu,
  /sourceProvenance/iu,
  /internalNotes/iu,
  /publication_decision/iu,
  /source register/iu,
  /canonical publication/iu,
  /publication records/iu,
  /record ID/iu,
];

const internalPublicationWorkflowFieldsInDist = forbiddenDistPatterns.filter(
  (pattern) => pattern.test(distHtml),
).length;

const maintenanceCsvEmittedToDist = walk(distDir).filter((filepath) =>
  filepath.endsWith(".csv"),
).length;

const publicTheses = theses.filter(({ data }) => data.visibility === "public");
const publicAlumni = people.filter(
  ({ data }) =>
    data.visibility === "public" && data.membershipStatus === "alumni",
);
const nonPublicExceptions = canonicalPublications.filter(
  ({ data }) => data.visibility !== "public",
);

const classifications = venueRows.reduce((counts, row) => {
  counts[row.display_classification] =
    (counts[row.display_classification] ?? 0) + 1;
  return counts;
}, {});

const summary = {
  canonical_publications: canonicalPublications.length,
  public_publications: publicPublications.length,
  non_public_exceptions: nonPublicExceptions.length,
  public_theses: publicTheses.length,
  public_alumni: publicAlumni.length,
  theme_labels_invalid: invalidThemeCount,
  public_publication_missing_year: missingPublicYear,
  internal_publication_workflow_fields_in_dist:
    internalPublicationWorkflowFieldsInDist,
  maintenance_csv_emitted_to_dist: maintenanceCsvEmittedToDist,
  venue_audit_csv: path.relative(root, venueAuditPath),
  venue_display_classifications: {
    usable: classifications.A ?? 0,
    truncated: classifications.B ?? 0,
    suspicious: classifications.C ?? 0,
    blank: classifications.D ?? 0,
  },
};

console.log(JSON.stringify(summary, null, 2));

const failures = [];
if (summary.public_publications !== 289) failures.push("public publications");
if (summary.non_public_exceptions !== 10)
  failures.push("non-public exceptions");
if (summary.public_theses !== 125) failures.push("public theses");
if (summary.public_alumni !== 181) failures.push("public alumni");
if (summary.theme_labels_invalid !== 0) failures.push("invalid themes");
if (summary.public_publication_missing_year !== 0)
  failures.push("missing public publication year");
if (summary.internal_publication_workflow_fields_in_dist !== 0)
  failures.push("workflow fields in dist");
if (summary.maintenance_csv_emitted_to_dist !== 0)
  failures.push("maintenance CSV emitted to dist");

if (failures.length > 0) {
  console.error(`publication discovery audit failed: ${failures.join(", ")}`);
  process.exit(1);
}
