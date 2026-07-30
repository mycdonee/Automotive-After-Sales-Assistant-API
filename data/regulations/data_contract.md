# Regulation Data Contract

## Purpose

This contract defines the committed structured data used by the regulatory
management demo.

The raw UNECE PDF, TXT, and eCFR XML files remain ignored research artifacts.
The committed JSON data contains verified summaries and traceable source
descriptions rather than copies of the source documents.

## Output files

- `regulation_records.jsonl`
  - one JSON object per line
  - exactly 18 regulation records
- `regulation_comparison_pairs.json`
  - one JSON array
  - exactly 11 comparison-pair objects

## Canonical regulation IDs

### Braking and stability

- `unece_r13h`
- `fmvss_135`
- `unece_r140`
- `fmvss_126`

### Occupant restraint

- `unece_r14`
- `fmvss_210`
- `unece_r16`
- `fmvss_209`
- `unece_r145`
- `fmvss_225`

### Lighting and light-signalling

- `unece_r48`
- `unece_r148`
- `unece_r149`
- `unece_r150`
- `unece_r104`
- `unece_r27`
- `fmvss_108`
- `fmvss_125`

## Canonical comparison IDs

1. `unece_r13h__fmvss_135`
2. `unece_r140__fmvss_126`
3. `unece_r14__fmvss_210`
4. `unece_r16__fmvss_209`
5. `unece_r145__fmvss_225`
6. `unece_r48__fmvss_108`
7. `unece_r148__fmvss_108`
8. `unece_r149__fmvss_108`
9. `unece_r150__fmvss_108`
10. `unece_r104__fmvss_108`
11. `unece_r27__fmvss_125`

## Regulation-record rules

Each regulation record must:

- use schema version `1.0`
- have one globally unique `regulation_id`
- represent one identifiable regulation or standard
- describe the reviewed regulation version rather than each amendment as a
  separate regulation
- use verified summaries only
- preserve vehicle-applicability limitations
- list requirement topics without asserting legal equivalence
- describe the official source chain in `reviewed_source_documents`
- use `source_content_date` for date-versioned sources such as eCFR
- use `null` when no single source-content date applies
- use `special_status_notes` for explicit transitional or legacy information
- use `verification_status: verified`

## Comparison-pair rules

Each comparison pair must:

- reference two existing regulation IDs
- use the UNECE regulation as `left_regulation_id`
- use the FMVSS standard as `right_regulation_id`
- preserve the approved pair number from
  `comparability_verification.md`
- use the verified comparison focus
- record comparable requirement topics
- record material scope and framework differences
- use `legal_equivalence: false`
- never imply that compliance with one framework establishes compliance with
  the other framework

## Current invariants

- regulation-record count: 18
- unique regulation IDs: 18
- comparison-pair count: 11
- unique comparison IDs: 11
- approved pairs: 11
- comparison level for the current locked set: `partial`
- pending regulation records: 0
- pending comparison pairs: 0

## Semantic-search text

The semantic-search layer must derive searchable text at load time.

For a regulation record, build search text from:

1. official identifier and aliases
2. title
3. regulatory system
4. regulated object
5. scope summary
6. vehicle applicability
7. requirement topics
8. reviewed version
9. special status notes

For a comparison pair, build search text from:

1. both referenced regulation records
2. comparison focus
3. overlap summary
4. comparable topics
5. scope differences

The derived search text is not stored in the source JSON files, preventing
duplicated text from drifting out of sync with the structured fields.

## Validation boundary

The structured data supports retrieval, filtering, comparison discovery, and
traceable summaries.

It does not provide legal advice, certify legal equivalence, or replace review
of the authoritative regulation text.
