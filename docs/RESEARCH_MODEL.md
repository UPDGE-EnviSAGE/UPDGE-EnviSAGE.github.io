# EnviSAGE Research Model

Canonical Research Ecosystem Architecture

Status: Canonical design document

This document defines the conceptual model for organizing EnviSAGE research knowledge. It is not yet a database schema, content schema, CMS model, or required implementation plan for every website feature.

`docs/FOUNDING_CHARTER.md` remains authoritative for why EnviSAGE exists. This document is authoritative for how EnviSAGE research entities and relationships are organized. `docs/CONTENT_MODEL.md` describes how these concepts are represented as website content, and `docs/ARCHITECTURE.md` describes how the platform implements them technically.

## Research Principle

EnviSAGE studies Geomatics Engineering for Environmental Systems.

Official tagline:

Spatial Understanding for Environmental Sustainability

The research ecosystem is organized around:

Research Areas -> Research Work -> Research Outputs

People and supporting entities connect across the model. The model is many-to-many by default and should not imply that every entity belongs to only one parent.

## Core Entities

The EnviSAGE research ecosystem is organized around these core entities:

1. Research Area
2. Research Topic
3. Person
4. Project
5. Thesis
6. Publication
7. Dataset
8. Software
9. Grant
10. Partner
11. Equipment

Study Area / Geographic Location is a planned extension rather than a required v1 entity.

## Research Areas

Research Areas are broad, strategic, navigation-level, and relatively stable. They organize the laboratory's major environmental and geomatics directions.

Current Research Areas:

- Earth Observation & Remote Sensing
- Coastal & Marine Environments
- Environmental Monitoring & Modeling
- Geospatial AI & Spatial Analytics
- Climate, Hazards & Resilience
- Geospatial Data & Decision Support

A Project or Thesis may belong to multiple Research Areas. Do not force one-area-only membership.

## Research Topics

Research Topics are flexible, specific, descriptive, and useful for filtering or discovery. They are not equivalent to Research Areas.

Examples:

- Water Quality
- Mangroves
- Seagrass
- Coral Reefs
- Air Quality
- PM2.5
- Flooding
- Bathymetry
- LiDAR
- Biodiversity
- Agriculture
- Fisheries
- Aquaculture
- Land Cover
- Climate Change

Research Areas are broad, strategic, navigation-level, and relatively stable. Research Topics are specific, descriptive, filtering-level, and flexible.

A public Research Topic page should only be generated when at least one public item references that topic. Empty public topic sections should not be shown unnecessarily.

## Project Model

A Project usually represents funded or formally organized research.

Possible Project relationships:

- principal investigator
- co-investigators
- researchers
- staff
- students
- grants
- partners
- research areas
- research topics
- theses
- publications
- datasets
- software
- other outputs

A Project and a Grant are not the same entity. A Project may receive support from one or more Grants. A Grant may support more than one Project or research activity.

## Thesis Model

A Thesis represents student research. A Thesis may belong to a funded Project, or it may exist independently under EnviSAGE.

The Thesis is the canonical public scholarly record for student research. Student profile pages are optional and are not required for v1.

Each Thesis may connect to:

- student(s)
- degree
- adviser
- co-adviser(s)
- research areas
- research topics
- optional parent Project
- publications
- datasets
- software
- GitHub repository
- dashboards/maps
- other outputs

Student rules:

- BS Geodetic Engineering thesis: 1 or 2 students
- MS thesis: exactly 1 student
- PhD dissertation: exactly 1 student

The implementation may use `students[]` for all levels.

Completed approved theses should eventually have their own public EnviSAGE page. The thesis page is the permanent EnviSAGE research record and may link to a GitHub repository, publications, datasets, software, related Project, maps, or dashboards.

Do not require a separate permanent student profile for every thesis author.

## People Model

The Person entity is specialized in `docs/PEOPLE_MODEL.md`.

People may include:

- Laboratory Heads / Lead Faculty
- Faculty
- Affiliate Faculty
- Researchers
- Research Staff
- Graduate Students
- Undergraduate Researchers
- Alumni

People should link automatically to their public contributions where possible.

Examples:

- Faculty -> Projects -> Students advised -> Publications -> Datasets -> Software -> Research Areas
- Student -> Thesis -> Publications -> Datasets -> Software

Do not require permanent public student profile pages for every student.

## Publications

Publications are independent scholarly entities.

They may connect to:

- authors
- EnviSAGE people
- Projects
- Theses
- Research Areas
- Research Topics
- Datasets
- Software

Do not model a Publication as belonging exclusively to one faculty member. Faculty publication lists should be generated from relationships.

## Datasets

Datasets are independent research entities. The public website is primarily a discovery and visualization layer initially. Do not assume large datasets are stored directly in GitHub.

### Research Dataset

A Research Dataset is generated or assembled for a specific research activity.

Examples:

- field measurements
- processed imagery
- classification products

### Shared Reference Dataset

A Shared Reference Dataset is reusable across multiple research activities.

Examples:

- elevation
- rainfall
- land cover
- administrative boundaries
- coastline
- climatology

Datasets may be linked to multiple Projects, Theses, Publications, and Software.

## Software

Software is an independent entity.

Possible forms:

- Python software
- R workflows/packages
- MATLAB tools
- Google Earth Engine scripts/apps
- QGIS plugins
- Jupyter workflows
- web applications

Software may link to:

- developers
- GitHub repository
- version
- license
- documentation
- Research Areas
- Research Topics
- Projects
- Theses
- Publications
- Datasets

GitHub is the primary development and code-hosting platform. The EnviSAGE website is the discovery layer.

## Grants

Grants are independent entities.

Fields may include:

- funding agency
- program
- grant title
- lead investigator
- dates
- supported Projects
- Partners
- optional funding amount

Grant amount visibility is controlled per Grant. Possible visibility for amount:

- public
- internal/private

Do not assume all funding amounts are public.

## Partners

Partners are independent entities.

Possible partner types:

- universities
- government agencies
- industry
- NGOs
- international organizations

Partners may connect to Projects, Grants, Publications, research collaborations, training, or other activities where appropriate.

## Equipment

Equipment is an independent research asset entity.

Examples:

- UAV
- GNSS receiver
- LiDAR system
- USV
- hyperspectral sensor
- multispectral camera
- water-quality sensor
- workstation/server

Public representation may include:

- name
- type
- capabilities
- description
- selected Projects where appropriate

Private or internal future functions may include borrower, reservation, checkout, return, maintenance, and inventory status.

Never expose internal borrowing or maintenance records publicly.

## Visibility

Major entities should support visibility such as:

- private
- internal
- public

Only public records are rendered on the public site. This is especially important for ongoing theses, unpublished research, private datasets, internal grant details, and equipment administration.

## Lifecycle And Status

Where appropriate, entities should support lifecycle states such as:

- draft
- ongoing
- completed
- archived

Examples:

- Ongoing thesis: `visibility: private`, `status: ongoing`
- Completed approved thesis: `visibility: public`, `status: completed`

## Discovery Model

Users should eventually be able to discover public research by:

- Research Area
- Research Topic
- Project
- Thesis
- Person
- Publication
- Dataset
- Software
- Partner

Topic pages should hide empty sections. For example, a Water Quality page may show only the public content that exists, such as Projects, Theses, Publications, Datasets, Software, or Maps/Dashboards.

Do not show empty categories unnecessarily.

## Teaching

Normal academic courses are not part of the EnviSAGE research ecosystem. Student theses are.

Training activities may become a separate entity later if needed.

## Study Areas - Planned Extension

Geographic Study Area / Location is a planned future entity, not a Phase 5B implementation requirement.

Possible examples:

- Bolinao
- Calatagan
- Laguna de Bay
- Palanan

A future Study Area may connect:

- Projects
- Theses
- Datasets
- Publications
- Partners
- Spatial Explorer layers

Do not implement this entity in Phase 5B.

## Conceptual Relationship Diagram

```text
                         EnviSAGE
                            |
             +--------------+--------------+
             |                             |
       Research Areas                    People
             |                             |
        Research Topics ------------------+
             |
        Research Work
        /           \
   Projects       Theses
        \           /
         \         /
          Outputs
             |
   +---------+----------+
   |         |          |
Publications Datasets Software
             |
      Spatial discovery

Supporting relationships:

Grants    -> Projects
Partners  -> Projects
Equipment -> Projects / Theses
Locations -> future spatial discovery
```

This diagram is conceptual. It does not imply that all relationships are strictly hierarchical. Many-to-many relationships are expected across the ecosystem.
