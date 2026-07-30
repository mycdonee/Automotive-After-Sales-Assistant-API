# Curated Vehicle Regulation Dataset

## Purpose

This directory contains a small, manually curated vehicle-regulation dataset for the Regulatory Management branch of the Automotive AI API.

The dataset supports:

* natural-language semantic search
* regulatory metadata filtering
* source provenance
* regulation detail lookup
* structured regulation comparison
* later Power Apps and Power Automate integration

It is not intended to be a machine-learning training dataset or a complete legal-regulation repository.

## Initial Dataset Scope

The first version targets 18 curated regulation records from two public regulatory frameworks:

* UNECE vehicle regulations
* United States Federal Motor Vehicle Safety Standards in 49 CFR Part 571

The records are grouped into three regulated systems:

* braking and vehicle stability
* occupant restraint systems
* lighting and light-signalling

Current curation status:

* 18 records have completed source and comparability verification
* 0 regulation records remain pending within the locked lighting and light-signalling inventory
* the final initial dataset target is 18 verified regulation records

European Union and EUR-Lex sources are intentionally deferred to a later milestone.

## Locked Dataset Inventory

### Braking and Vehicle Stability

Status: source verification completed.

#### UNECE

* UN Regulation No. 13-H — Braking of passenger cars
* UN Regulation No. 140 — Electronic Stability Control systems

#### United States

* FMVSS No. 135 — Light vehicle brake systems
* FMVSS No. 126 — Electronic stability control systems for light vehicles

Record count: 4.

### Occupant Restraint Systems

Status: source verification completed.

#### UNECE

* UN Regulation No. 14 — Safety-belt anchorages
* UN Regulation No. 16 — Safety-belts
* UN Regulation No. 145 — ISOFIX anchorage systems, ISOFIX top tether anchorages and i-Size seating positions

#### United States

* FMVSS No. 210 — Seat belt assembly anchorages
* FMVSS No. 209 — Seat belt assemblies
* FMVSS No. 225 — Child restraint anchorage systems

Record count: 6.

### Lighting and Light-Signalling

Status: source and comparability verification in progress; UN R48 and FMVSS 108 have completed verification.

#### UNECE

* UN Regulation No. 48 — Installation of lighting and light-signalling devices
* UN Regulation No. 148 — Light-signalling devices
* UN Regulation No. 149 — Road illumination devices
* UN Regulation No. 150 — Retro-reflective devices and markings
* UN Regulation No. 104 — Retro-reflective markings for heavy and long vehicles
* UN Regulation No. 27 — Advance-warning triangles

#### United States

* FMVSS No. 108 — Lamps, reflective devices, and associated equipment
* FMVSS No. 125 — Warning devices

Record count: 8.

### Dataset Count

* braking and vehicle stability: 4 records
* occupant restraint systems: 6 records
* lighting and light-signalling: 8 records
* total: 18 records

## Comparison Map

The following eleven relationships have completed source-based verification.

| UNECE regulation | U.S. regulation | Status | Comparison level | Comparison focus |
| ---------------- | --------------- | ------ | ---------------- | ---------------- |
| UN R13-H | FMVSS 135 | approved | `partial` | light-vehicle braking |
| UN R140 | FMVSS 126 | approved | `partial` | electronic stability control |
| UN R14 | FMVSS 210 | approved | `partial` | seat-belt anchorages |
| UN R16 | FMVSS 209 | approved | `partial` | seat-belt assemblies |
| UN R145 | FMVSS 225 | approved | `partial` | child-restraint anchorages |
| UN R48 | FMVSS 108 | approved | `partial` | vehicle lighting installation |
| UN R148 | FMVSS 108 | approved | `partial` | light-signalling device performance |
| UN R149 | FMVSS 108 | approved | `partial` | road-illumination device performance |
| UN R150 | FMVSS 108 | approved | `partial` | retro-reflective device performance |
| UN R104 | FMVSS 108 | approved | `partial` | vehicle conspicuity marking requirements |
| UN R27 | FMVSS 125 | approved | `partial` | portable advance warning triangle performance |

All eleven locked comparison relationships have completed source-based verification and received a comparison level.

| UNECE regulation | U.S. regulation | Status | Candidate comparison focus |
| ---------------- | --------------- | ------ | -------------------------- |

Approved relationships are research comparison links, not claims of legal equivalence.

Candidate relationships must be verified against official applicability, vehicle scope, regulated object, requirement topics, test conditions, amendment status, and other relevant provisions before they are added to the comparison-pair dataset.

## Comparability Policy

Regulations must not be treated as equivalent merely because they have similar titles or concern the same broad vehicle system.

A comparison pair may be approved only when official sources demonstrate overlap in:

* regulated system
* vehicle applicability
* regulated object or function
* requirement topics
* performance or test dimensions

Every approved pair must receive one of the following comparison levels:

* `direct`
* `partial`
* `system_level`

A candidate must be rejected or marked as not directly comparable when the scopes do not overlap sufficiently.

## Record Definition

One dataset record represents one identifiable regulation or safety standard.

The initial dataset does not create separate records for every paragraph, test procedure, requirement, amendment, or annex.

Full legal texts are not stored in the repository.

## Field Provenance

### Official Source Fields

These fields should reproduce or directly represent information found in an official source:

* `official_identifier`
* `title`
* `issuing_authority`
* `official_vehicle_categories`
* `document_status`
* `effective_date`
* `revision`
* `source_name`
* `source_url`

An unknown or unclear official value must be stored as `null` or an explicitly allowed unknown value. It must not be guessed.

### Project-Normalized Fields

These fields are created by the project to support consistent search, filtering, and comparison across regulatory frameworks:

* `regulation_id`
* `jurisdiction`
* `regulation_family`
* `regulated_system`
* `normalized_vehicle_scope`
* `requirement_topics`

Normalized fields do not replace the original terminology used by the official source.

### Project-Created Text Fields

These fields are written by the project based on reviewed official material:

* `requirement_summary`
* `source_text`
* `summary_origin`

Project-created summaries must remain factual, limited in scope, and traceable to official sources.

They must not present legal interpretations, homologation decisions, compliance conclusions, or approval decisions.

## Planned Files

```text
data/regulations/
├── comparability_verification.md
├── regulation_records.jsonl
├── regulation_comparison_pairs.json
└── README.md
```

`comparability_verification.md` records the source-based research decisions used to approve or reject candidate comparison relationships.

`regulation_records.jsonl` will contain the normalized regulation records.

`regulation_comparison_pairs.json` will contain only reviewed and explicitly approved comparison relationships.

## Source Requirements

Every record must:

* use an official UNECE, eCFR, GovInfo, NHTSA, or other approved government source
* contain an official source URL
* record the date on which the source was last verified
* distinguish official information from project-created summaries
* avoid unsupported legal conclusions

Secondary websites, commercial regulation summaries, Wikipedia, and search-result snippets must not be used as the final source for a record.

## Limitations

This is a small proof-of-concept dataset created for regulatory-information retrieval and comparison workflows.

It is not:

* a complete collection of vehicle regulations
* an official homologation database
* a compliance certification system
* legal advice
* an authoritative legal interpretation

Regulation identifiers, official titles, and source references are based on public official sources. Normalized summaries and comparison fields are created for demonstration purposes and are not authoritative legal interpretations.
