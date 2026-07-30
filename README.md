# Automotive After-Sales Assistant API

A FastAPI-based backend prototype for natural-language automotive information retrieval, issue classification, and regulation comparison.

## Project scope

The project currently contains two business lines.

### 1. Complaint Intelligence

- TF-IDF retrieval over automotive service records
- SentenceTransformer semantic retrieval
- retrieval over processed public NHTSA complaint records
- metadata filtering by category, make, model, and model year
- automotive issue-category classification
- confidence and review-required outputs

### 2. Regulatory Management

- semantic retrieval over verified UNECE and United States regulations
- structured UNECE–FMVSS comparison pairs
- runtime Pydantic validation
- JSON Schema and cross-reference validation
- explicit scope-difference documentation
- legal-equivalence safeguards
- typed REST and OpenAPI integration

## Current API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check application health |
| POST | `/retrieval/search` | Search service or complaint records |
| POST | `/classification/predict` | Classify an automotive issue |
| POST | `/regulations/search` | Search verified regulation records |
| POST | `/regulations/comparisons/search` | Search UNECE–FMVSS comparison pairs |

Interactive OpenAPI documentation is available at:

```text
http://127.0.0.1:8000/docs
```

The generated OpenAPI JSON is available at:

```text
http://127.0.0.1:8000/openapi.json
```

## Regulation dataset

The Regulatory Management branch currently contains:

- 18 verified regulation records
- 11 UNECE regulations
- 7 United States FMVSS standards
- 11 approved UNECE–FMVSS comparison pairs
- 3 regulatory systems

The covered regulatory systems are:

1. braking and stability
2. occupant restraint
3. lighting and light signalling

Every committed comparison pair is classified as:

```text
status = approved
comparison_level = partial
legal_equivalence = false
```

A partial comparison indicates meaningful technical overlap. It does not mean that two regulations are legally interchangeable.

## Regulation search

### Search individual regulations

```text
POST /regulations/search
```

Supported request fields:

- `query`
- `top_k`
- `jurisdiction`
- `regulatory_system`

Example request:

```json
{
  "query": "portable reflective warning triangle for a stopped vehicle",
  "top_k": 3,
  "regulatory_system": "lighting_and_light_signalling"
}
```

Example with curl:

```bash
curl -X POST   http://127.0.0.1:8000/regulations/search   -H "Content-Type: application/json"   -d '{
    "query": "portable reflective warning triangle for a stopped vehicle",
    "top_k": 3,
    "regulatory_system": "lighting_and_light_signalling"
  }'
```

### Search regulation comparisons

```text
POST /regulations/comparisons/search
```

Supported request fields:

- `query`
- `top_k`
- `regulatory_system`

Example request:

```json
{
  "query": "compare European and United States warning triangle requirements",
  "top_k": 3
}
```

Example with curl:

```bash
curl -X POST   http://127.0.0.1:8000/regulations/comparisons/search   -H "Content-Type: application/json"   -d '{
    "query": "compare European and United States warning triangle requirements",
    "top_k": 3
  }'
```

Comparison responses preserve:

- the two source regulation IDs
- official identifiers
- regulatory system
- comparison focus
- comparison level
- overlap summary
- similarity score
- `legal_equivalence: false`

## Semantic retrieval

The semantic retrieval services use:

```text
sentence-transformers/all-MiniLM-L6-v2
```

The model may be downloaded from Hugging Face during first use.

Within a running application process:

- the embedding model is cached
- the validated regulation dataset is cached
- regulation and comparison embeddings are precomputed
- the semantic service instance is reused between requests

Similarity scores are ranking signals. They are not legal confidence, compliance approval, or certification.

## Technology stack

- Python 3.12+
- FastAPI
- Pydantic v2
- pandas
- NumPy
- scikit-learn
- SentenceTransformers
- JSON Schema
- pytest

## Project structure

```text
app/
├── main.py
├── routes/
│   ├── classification.py
│   ├── health.py
│   ├── regulations.py
│   └── retrieval.py
├── schemas/
│   ├── classification.py
│   ├── common.py
│   ├── regulation.py
│   └── retrieval.py
└── services/
    ├── base_retrieval_service.py
    ├── classification_service.py
    ├── regulation_data_loader.py
    ├── regulation_semantic_search_service.py
    ├── retrieval_registry.py
    ├── retrieval_service.py
    └── semantic_retrieval_service.py

data/
├── service_records.csv
├── processed/
└── regulations/
    ├── README.md
    ├── comparability_verification.md
    ├── data_contract.md
    ├── regulation_comparison_pairs.json
    ├── regulation_records.jsonl
    └── schemas/

scripts/
├── download_nhtsa_complaints.py
├── evaluate_retrieval.py
├── generate_regulation_data.py
├── prepare_nhtsa_data.py
├── train_classifier.py
└── validate_regulation_data.py
```

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
uvicorn app.main:app --reload
```

Open the interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## Regulation data generation and validation

Regenerate the committed structured regulation data:

```bash
python scripts/generate_regulation_data.py
```

Run the independent validator:

```bash
python scripts/validate_regulation_data.py
```

The validation process checks:

- JSON Schema compliance
- exact record and comparison counts
- canonical identifiers
- unique regulation and pair IDs
- pair-number uniqueness
- cross-file references
- jurisdiction direction
- regulatory-system consistency
- approved comparison mappings
- comparison level
- legal-equivalence safeguards

The runtime application loads only the committed JSONL and JSON data. It does not read the local research PDF, XML, HTML, DOCX, or TXT files.

## Tests

Run the complete test suite:

```bash
python -m pytest -q
```

At the completion of the Regulatory Management milestone:

```text
53 tests passed
```

The test strategy separates:

- structured-data and contract validation
- runtime loader validation
- deterministic semantic-service tests with fake embeddings
- API tests with FastAPI dependency overrides
- a separate real-model end-to-end smoke test

This keeps the automated suite reproducible and independent of network access while still verifying the real Hugging Face model separately.

## Documentation

- [Architecture](docs/architecture.md)
- [NHTSA data pipeline](docs/data_pipeline.md)
- [Evaluation](docs/evaluation.md)
- [Regulatory Management milestone](docs/regulatory_management.md)
- [Regulation dataset documentation](data/regulations/README.md)
- [Comparability verification](data/regulations/comparability_verification.md)
- [Regulation data contract](data/regulations/data_contract.md)

## Current limitations

- The regulation dataset covers 18 selected regulations, not the complete UNECE or FMVSS corpus.
- The 11 comparison pairs represent scoped technical overlap, not legal equivalence.
- Semantic similarity is a retrieval-ranking signal, not proof of compliance.
- Regulation retrieval has not yet been evaluated against a large labelled regulatory-query benchmark.
- Embeddings are stored in application memory.
- No persistent vector database is currently used.
- Authentication, Docker deployment, and continuous integration remain future work.

## Disclaimer

This project is an educational software prototype.

It does not provide:

- legal advice
- regulatory certification
- proof of legal equivalence
- vehicle diagnosis
- repair instructions
- safety-critical operational guidance

Users must consult the applicable official legal source and qualified regulatory, legal, compliance, or automotive professionals.
