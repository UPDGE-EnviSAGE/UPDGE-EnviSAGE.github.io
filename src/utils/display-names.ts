const LOWERCASE_PARTICLES = new Set([
  "de",
  "del",
  "dela",
  "la",
  "las",
  "los",
  "van",
  "von",
  "y",
]);

const HONORIFIC_PREFIX = /^(Dr\.|Asst\. Prof\.|Engr\.)\s+/u;

const normalizeSpaces = (value: string) => value.trim().replace(/\s+/gu, " ");

const formatNamePart = (part: string, index: number) => {
  const cleaned = part.trim();

  if (!cleaned) {
    return cleaned;
  }

  if (/^[A-Z]\.$/u.test(cleaned)) {
    return cleaned;
  }

  const lower = cleaned.toLocaleLowerCase("en-US");

  if (index > 0 && LOWERCASE_PARTICLES.has(lower)) {
    return lower;
  }

  return lower.replace(/(^|[-'])(\p{L})/gu, (_match, prefix, letter) => {
    return `${prefix}${letter.toLocaleUpperCase("en-US")}`;
  });
};

export const toTitleCasePersonName = (name: string) =>
  normalizeSpaces(name)
    .split(" ")
    .map((part, index) => formatNamePart(part, index))
    .join(" ");

export const formatPersonDisplayName = (name: string) => {
  const cleaned = normalizeSpaces(name.replace(/^["']|["']$/gu, ""));

  if (!cleaned) {
    return cleaned;
  }

  const honorific = cleaned.match(HONORIFIC_PREFIX)?.[0] ?? "";
  const withoutHonorific = honorific
    ? cleaned.slice(honorific.length)
    : cleaned;
  const commaParts = withoutHonorific.split(",");

  if (
    commaParts.length === 2 &&
    commaParts.every((part) => part.trim().length > 0)
  ) {
    return `${honorific}${toTitleCasePersonName(
      `${commaParts[1]} ${commaParts[0]}`,
    )}`;
  }

  return `${honorific}${toTitleCasePersonName(withoutHonorific)}`;
};

export const joinDisplayNames = (names: readonly string[]) => {
  const formatted = names.map((name) => formatPersonDisplayName(name));

  if (formatted.length < 2) {
    return formatted.join("");
  }

  if (formatted.length === 2) {
    return `${formatted[0]} and ${formatted[1]}`;
  }

  return `${formatted.slice(0, -1).join(", ")}, and ${formatted.at(-1)}`;
};
