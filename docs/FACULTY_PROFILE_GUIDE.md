# Faculty Profile Guide

Status: Maintainer guide

This guide defines how public EnviSAGE faculty profiles are curated and maintained. It extends `docs/PEOPLE_MODEL.md` for current faculty profile pages without changing the broader research ecosystem model in `docs/RESEARCH_MODEL.md`.

## Canonical Profile Structure

Each public faculty profile is backed by one Person content record in `src/content/people/`.

Required reviewed fields for current faculty profiles:

- full public name
- EnviSAGE role
- UP Department of Geodetic Engineering position
- short professional biography
- research interests
- broad EnviSAGE Research Areas
- Google Scholar URL
- public visibility

Optional fields:

- ORCID
- approved profile photo
- personal website
- GitHub profile

Do not create duplicate Person records for a faculty member who later appears as a project investigator, adviser, publication author, dataset contributor, or software contributor.

## Approved Sources

Use the UP Department of Geodetic Engineering faculty pages as the institutional source for names, positions, and research interests:

https://home.dge.upd.edu.ph/faculty

Google Scholar URLs may be stored only when supplied or reviewed by maintainers. Do not use Google Scholar as a source for dynamic metrics, publication counts, citation counts, h-index, or unreviewed publication lists.

## Biography Style

Faculty biographies should be original summaries written for the public EnviSAGE website.

Use 2 to 3 short paragraphs totaling about 120 to 180 words. Each biography should describe:

- the faculty member's UP role
- their EnviSAGE role
- verified research interests
- how those interests connect to the laboratory's public research direction

Do not copy institutional profile text verbatim. Do not add awards, education history, grants, project titles, publication claims, citation metrics, or thesis-advising statements unless those facts are reviewed and intentionally added to the content model.

## Research Interests

Store specific reviewed interests in `researchInterests`.

Research interests should come from the approved institutional faculty source or another explicitly approved source. Preserve the meaning of the source terms, but minor editorial normalization is acceptable for consistency.

Do not treat research interests as the same thing as EnviSAGE Research Areas. Research Areas are broad navigation categories defined by `docs/RESEARCH_MODEL.md`; research interests are more specific faculty descriptors.

## Photo Policy

Use a faculty photo only when the image is official, public, suitable for website reuse, and approved for inclusion in the repository.

Do not use generated portraits, stock photos, screenshots, or unrelated images. If an approved photo is not available, leave `photo` empty and allow the site to use the built-in initials fallback. The profile architecture supports replacing the fallback with an approved photo later.

## Google Scholar Policy

Faculty records may include a reviewed Google Scholar URL in `googleScholar`.

Do not scrape Google Scholar. Do not store citation counts, h-index, i10-index, publication counts, or inferred publication lists from Google Scholar. These values change over time and require a different review process.

## ORCID Policy

Populate `orcid` only when the ORCID is available from an official institutional source or clearly linked from the faculty member's reviewed public profile.

Leave `orcid` empty when the identifier is unknown, ambiguous, or discovered only through unreviewed search results.

## Future Relationship Population

Faculty profile pages are designed to receive automatic public relationship sections later.

Future connections may include:

- Projects
- Publications
- Student Research
- Datasets
- Software

These sections must be generated from reviewed public content records. Do not manually write placeholder contribution lists into faculty biographies or profile pages.

Until related records exist, contribution sections should not render on public profile pages.
