export type VenueDisplayClassification =
  | "clearly usable as displayed"
  | "truncated but acceptable"
  | "suspicious/malformed for public display"
  | "blank";

export interface VenueDisplayReview {
  classification: VenueDisplayClassification;
  issue: string;
  recommendedDisplayAction: string;
  displayValue: string;
}

const noTitlePattern = /^\(?\s*no\s+title\s*\)?$/iu;

const normalizeForComparison = (value: string) =>
  value
    .trim()
    .toLocaleLowerCase("en")
    .replace(/[^\p{L}\p{N}]+/gu, " ")
    .replace(/\s+/gu, " ")
    .trim();

export const classifyVenueForDisplay = (
  sourceOrVenue: string | undefined,
  title: string,
): VenueDisplayReview => {
  const value = sourceOrVenue?.trim() ?? "";

  if (!value) {
    return {
      classification: "blank",
      issue: "No source or venue value is available.",
      recommendedDisplayAction: "Omit the venue line unless a DOI is present.",
      displayValue: "",
    };
  }

  if (noTitlePattern.test(value)) {
    return {
      classification: "suspicious/malformed for public display",
      issue: "The source or venue value is a no-title placeholder.",
      recommendedDisplayAction:
        "Omit the venue from public display and preserve the source value for later bibliographic correction.",
      displayValue: "",
    };
  }

  const normalizedValue = normalizeForComparison(value);
  const normalizedTitle = normalizeForComparison(title);

  if (
    normalizedValue === normalizedTitle ||
    (normalizedValue.length > 20 && normalizedTitle.includes(normalizedValue))
  ) {
    return {
      classification: "suspicious/malformed for public display",
      issue:
        "The source or venue value repeats or appears to be part of the publication title.",
      recommendedDisplayAction:
        "Omit the venue from public display and preserve the source value for later bibliographic correction.",
      displayValue: "",
    };
  }

  if (value.includes("…") || value.endsWith("...")) {
    return {
      classification: "truncated but acceptable",
      issue: "The source or venue appears truncated but remains meaningful.",
      recommendedDisplayAction:
        "Display the existing source or venue without fabricating a completion.",
      displayValue: value,
    };
  }

  return {
    classification: "clearly usable as displayed",
    issue: "",
    recommendedDisplayAction: "Display the existing source or venue.",
    displayValue: value,
  };
};

export const pluralize = (
  count: number,
  singular: string,
  plural = `${singular}s`,
) => `${count} ${count === 1 ? singular : plural}`;
