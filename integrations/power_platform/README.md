# Power Platform Connector

This directory contains a Swagger 2.0 contract for importing the Automotive Regulatory Search API as a Microsoft Power Platform custom connector.

## Included files

```text
integrations/power_platform/
├── README.md
└── swagger.json
```

The connector exposes two operations:

```text
SearchRegulations
SearchRegulationComparisons
```

These operations call:

```text
POST /regulations/search
POST /regulations/comparisons/search
```

## Current connector status

The committed Swagger file currently uses the placeholder host:

```text
replace-with-your-api-host.example.com
```

The schema and operations are ready for connector import, but the placeholder host cannot make real API requests.

A publicly reachable HTTPS deployment is required before the connector can be tested from Power Apps or Power Automate.

## Generate the Swagger file

Run the exporter from the project root:

```bash
python -m scripts.export_power_platform_openapi
```

This generates:

```text
integrations/power_platform/swagger.json
```

The default export uses the placeholder host.

## Export for a deployed API

After the FastAPI application has been deployed to a public HTTPS domain, regenerate the connector definition with the real hostname.

Example:

```bash
python -m scripts.export_power_platform_openapi   --host automotive-api.example.com
```

The `--host` value must contain only the hostname.

Correct:

```text
automotive-api.example.com
```

Incorrect:

```text
https://automotive-api.example.com
automotive-api.example.com/api
```

The Swagger contract already specifies:

```text
schemes = ["https"]
basePath = "/"
```

## Connector operations

### SearchRegulations

Searches the verified regulation dataset.

Input fields:

- `query`
- `top_k`
- `jurisdiction`
- `regulatory_system`

Example request body:

```json
{
  "query": "portable reflective warning triangle requirements",
  "top_k": 3,
  "jurisdiction": "UNECE",
  "regulatory_system": "lighting_and_light_signalling"
}
```

The result includes:

- regulation ID
- official identifier
- title
- jurisdiction
- regulatory system
- regulated object
- scope summary
- reviewed version
- similarity score

### SearchRegulationComparisons

Searches approved UNECE–FMVSS comparison pairs.

Input fields:

- `query`
- `top_k`
- `regulatory_system`

Example request body:

```json
{
  "query": "compare European and United States warning triangle requirements",
  "top_k": 3,
  "regulatory_system": "lighting_and_light_signalling"
}
```

The result includes:

- pair ID
- pair number
- UNECE and FMVSS regulation IDs
- official identifiers
- regulatory system
- comparison focus
- comparison level
- overlap summary
- similarity score
- legal-equivalence field

For all committed comparison pairs:

```text
legal_equivalence = false
```

The connector must not describe semantic similarity as legal confidence, regulatory approval, certification, or proof of legal equivalence.

## Import workflow

After deploying the API and regenerating `swagger.json` with the real host:

1. Open the custom connector area in Power Apps or Power Automate.
2. Create a new connector by importing an OpenAPI or Swagger file.
3. Upload `integrations/power_platform/swagger.json`.
4. Review the connector name, host, base URL, and operations.
5. Configure authentication if authentication is added to the API.
6. Create the connector.
7. Create a connection.
8. Test `SearchRegulations`.
9. Test `SearchRegulationComparisons`.
10. Verify that comparison results retain `legal_equivalence = false`.

The exact interface labels can vary between Power Platform environments.

## Power Apps proof-of-concept

A later Power Apps interface can contain:

- a text input for the natural-language query
- a jurisdiction dropdown
- a regulatory-system dropdown
- a search button
- a gallery for regulation results
- a gallery for comparison results
- a visible legal-equivalence disclaimer

Conceptual request flow:

```text
Power Apps
    ↓
Power Platform custom connector
    ↓
public HTTPS FastAPI deployment
    ↓
cached semantic-search service
    ↓
verified regulation dataset
```

## Validation

Run the connector contract tests:

```bash
python -m pytest   tests/test_power_platform_openapi.py   -q
```

The tests verify:

- Swagger 2.0 format
- HTTPS configuration
- stable operation IDs
- agreement with FastAPI operation IDs
- valid definition references
- absence of unsupported OpenAPI 3 keywords
- legal-equivalence safeguards
- host validation
- connector file size

Run the complete project suite:

```bash
python -m pytest -q
```

## Regeneration rule

Do not manually edit `swagger.json`.

Instead:

1. update `scripts/export_power_platform_openapi.py`;
2. regenerate the Swagger file;
3. run the connector tests;
4. review the generated diff;
5. commit the exporter and generated file together.

This keeps the committed connector contract reproducible.
