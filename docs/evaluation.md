# Evaluation

## 1. Evaluation Scope

This document reports the current evaluation results for the Complaint Intelligence branch of the project.

The evaluated capabilities are:

- TF-IDF service-record retrieval
- sentence-embedding semantic retrieval
- multi-class automotive issue classification
- confidence-based human-review routing
- API validation through automated tests

The retrieval and classification evaluations use different datasets and serve different purposes.

The retrieval benchmark uses the small synthetic service-record dataset so that expected records can be labelled and reproduced deterministically.

The classification evaluation uses processed public NHTSA Consumer Complaint records to provide a more realistic automotive text-classification experiment.

These results represent an evaluated project baseline. They are not presented as production-level performance.

## 2. Evaluation Data

### 2.1 Synthetic Retrieval Dataset

The retrieval development benchmark uses 30 manually created synthetic automotive service records.

The synthetic dataset is retained because it provides:

- stable record identifiers
- deterministic automated tests
- manually verifiable expected results
- controlled natural-language query examples
- reproducible TF-IDF and semantic retrieval comparison

It is not intended to represent the full variety or difficulty of real automotive service data.

### 2.2 NHTSA Classification Dataset

The classification dataset contains 1,998 processed NHTSA Consumer Complaint records distributed across 12 issue categories.

| Property | Value |
|---|---:|
| Total records | 1,998 |
| Training records | 1,598 |
| Test records | 400 |
| Test fraction | 20% |
| Categories | 12 |
| Random state | 42 |

The categories are:

- Air Bags
- Body and Structure
- Braking System
- Driver Assistance
- Electrical System
- Engine
- Fuel System
- Power Train
- Seat Belts
- Steering
- Tires and Wheels
- Visibility

The processed dataset is approximately balanced, with between 160 and 180 records per category.

Category labels were derived during preprocessing from the NHTSA component information. The classifier itself is trained only on complaint narratives.

The component and title fields are deliberately excluded from model input because using fields involved in constructing the target category would cause label leakage and produce misleadingly high evaluation results.

## 3. Retrieval Evaluation

### 3.1 Benchmark Design

The retrieval benchmark contains ten manually labelled natural-language queries.

Each query has an expected synthetic service-record identifier.

Examples include:

```text
The vehicle takes much longer to stop.
The battery is dead every morning.
The dashboard goes completely dark.
The steering wheel shakes at motorway speed.
```

For each query and retrieval method, the evaluation script records:

- expected record identifier
- top-ranked record identifier
- three highest-ranked record identifiers
- top-1 hit
- top-3 hit
- request latency in milliseconds

The benchmark compares:

```text
TF-IDF retrieval
SentenceTransformer semantic retrieval
```

### 3.2 Retrieval Results

| Method | Queries | Top-1 accuracy | Top-3 accuracy | Average latency |
|---|---:|---:|---:|---:|
| TF-IDF | 10 | 90% | 100% | 0.659 ms |
| Semantic | 10 | 100% | 100% | 195.395 ms |

TF-IDF retrieved the expected record first for nine of the ten queries. The remaining expected record still appeared within the top three.

Semantic retrieval returned the expected record first for all ten benchmark queries.

### 3.3 Interpretation

The benchmark illustrates the different strengths of the two retrieval approaches.

TF-IDF is:

- fast
- transparent
- effective when queries share terminology with stored records
- inexpensive to initialize and execute

Semantic retrieval is:

- better suited to natural-language paraphrases
- capable of matching related meanings with less exact lexical overlap
- more computationally expensive
- dependent on a pretrained sentence-embedding model

The results do not demonstrate that semantic retrieval will always outperform TF-IDF.

The benchmark is intentionally small and based on synthetic records. It is primarily used to verify system behaviour and make retrieval comparison repeatable.

### 3.4 Latency Limitations

The latency values were collected in a local development environment.

Semantic retrieval latency showed substantial variation between queries. This can be affected by:

- model initialization and warm-up
- local CPU performance
- background processes
- Python and machine-learning library caching
- the small number of measured requests

The reported latency should therefore not be interpreted as a production performance guarantee.

A production benchmark would require:

- separate cold-start and warm-request measurements
- repeated runs
- percentile latency statistics
- controlled hardware
- concurrent requests
- a larger document collection

## 4. Classification Evaluation

### 4.1 Model Pipeline

The classification baseline uses one scikit-learn pipeline:

```text
Complaint narrative
→ TF-IDF vectorization
→ Logistic Regression
→ category probabilities
```

The TF-IDF vectorizer uses word unigrams and bigrams.

Logistic Regression was selected as the first baseline because it:

- performs effectively on sparse text features
- trains quickly on the current dataset size
- supports multi-class classification
- provides `predict_proba()`
- can be saved and deployed as a lightweight artifact
- is easier to inspect than a more complex neural model

The vectorizer and classifier are stored together in one serialized pipeline to prevent preprocessing and model-version mismatches during inference.

### 4.2 Data Split

The dataset is divided using a stratified train-test split:

```text
Training records: 1,598
Test records:       400
Test fraction:      20%
Random state:       42
```

Stratification preserves approximately the same class distribution in the training and test portions.

The held-out test records are not used to fit the vectorizer or classification model.

### 4.3 Classification Results

| Metric | Result |
|---|---:|
| Accuracy | 0.6425 |
| Macro F1 | 0.6451 |
| Weighted F1 | 0.6458 |

The accuracy means that approximately 64.25% of the held-out complaint records received the expected category.

Macro F1 gives equal importance to every category, regardless of its number of records.

Weighted F1 accounts for category size when combining class-level F1 scores.

The similar macro and weighted F1 values are consistent with the approximately balanced category distribution.

### 4.4 Interpretation

This is a credible first baseline for a 12-class problem based on a relatively small set of user-written complaint narratives.

The task is difficult because:

- complaint language is noisy and inconsistent
- a complaint may mention multiple vehicle systems
- categories such as Engine, Power Train, and Electrical System may overlap
- labels are generated from normalized component mappings
- each category contains only approximately 160 to 180 records
- complaint narratives may omit important technical context

The model is therefore not presented as production-ready.

Its purpose is to demonstrate an end-to-end applied-AI workflow:

```text
public automotive data
→ preprocessing
→ supervised model training
→ held-out evaluation
→ saved model artifact
→ API inference
→ structured probability output
→ human-review routing
```

Potential future improvement work includes:

- confusion-matrix analysis
- inspection of incorrectly classified records
- refinement of noisy category mappings
- word and character n-gram comparison
- Linear SVM evaluation
- probability calibration
- transformer-based model comparison
- training on a larger labelled dataset

These improvements should be evaluated using a fixed test set rather than selected according to training performance.

## 5. Confidence and Human Review

The classification endpoint returns:

```json
{
  "predicted_category": "Braking System",
  "confidence": 0.6202,
  "review_required": false
}
```

The confidence value is the highest class probability returned by the Logistic Regression pipeline.

The current review rule is:

```text
confidence below 0.60
→ review_required = true

confidence at or above 0.60
→ review_required = false
```

This creates a basic human-in-the-loop workflow.

A low-confidence prediction is not rejected by the API. Instead, it is returned with a flag indicating that a person should review the result before it is trusted or used in a downstream process.

For example:

```json
{
  "predicted_category": "Electrical System",
  "confidence": 0.1136,
  "review_required": true
}
```

This is useful when the input text is vague and several categories receive similar probabilities.

The current threshold of 0.60 is an initial operational rule. It has not yet been selected through a formal coverage-versus-accepted-accuracy analysis.

A later evaluation could measure:

```text
coverage
= proportion of predictions accepted automatically

accepted accuracy
= accuracy among predictions accepted automatically

review rate
= proportion of predictions sent for human review
```

This would allow the threshold to be selected according to the risk and automation requirements of a specific business process.

## 6. Similarity Score and Classification Confidence

Retrieval similarity and classification confidence represent different concepts.

### Retrieval similarity

```text
similarity_score
```

describes how close a query representation is to a stored record representation.

It is used to rank retrieval results.

It is not a calibrated probability that a retrieved result is correct.

### Classification confidence

```text
confidence
```

is the highest category probability returned by the classification pipeline.

It is used by the current business rule to determine whether human review is required.

Although it is a probability output, it should not automatically be treated as perfectly calibrated. Formal calibration would require additional evaluation.

The API therefore keeps the two fields separate and does not describe retrieval similarity as confidence.

## 7. Generated Evaluation Artifacts

The training and evaluation scripts generate:

```text
models/issue_classifier.joblib
models/classifier_metadata.json
evaluation/classification_report.json
evaluation/classification_confusion_matrix.csv
evaluation/retrieval_benchmark.csv
```

The model metadata records:

- model version
- model type
- feature representation
- training data source
- training timestamp
- scikit-learn version
- random state
- train-test split
- review threshold
- category names
- class distribution
- evaluation metrics

The confusion matrix and complete classification report are retained for more detailed error analysis.

## 8. Reproducibility

Run the retrieval benchmark from the project root:

```bash
python -m scripts.evaluate_retrieval
```

Train and evaluate the issue classifier:

```bash
python -m scripts.train_classifier
```

Run all automated tests:

```bash
python -m pytest -v
```

At the completion of the classification milestone, the project test suite contained 21 passing tests.

The project uses a fixed random state for the train-test split and model training to improve reproducibility.

Exact runtime and latency values may still vary across operating systems, library versions, and hardware.

## 9. Known Limitations

### Retrieval

- The labelled retrieval benchmark contains only ten queries.
- The benchmark uses synthetic records rather than NHTSA complaints.
- NHTSA retrieval has not yet been evaluated with a manually labelled public-data query set.
- Semantic embeddings are currently computed and stored in memory.
- Embeddings are not persisted in a vector database.
- Latency measurements are based on one local development environment.
- No hybrid lexical-semantic ranking has been implemented.

### Classification

- The training dataset contains fewer than 2,000 records.
- The task contains 12 potentially overlapping categories.
- Category labels depend on rule-based component normalization.
- Complaint narratives may describe multiple issues.
- The model has not undergone probability calibration.
- The 0.60 review threshold is an initial rule rather than an optimized business threshold.
- No model-comparison experiment has yet been performed.
- The classifier is not intended for safety-critical automatic decision-making.

### System

- Data is currently loaded from processed files rather than PostgreSQL.
- Authentication and authorization have not been implemented.
- The API has not yet been connected to Power Apps or Dataverse.
- Production monitoring, drift detection, and audit logging are not yet implemented.
- Docker and continuous integration are planned for later milestones.

## 10. Responsible Use

This project is an educational and portfolio prototype.

It must not be used as:

- an official vehicle diagnosis system
- a replacement for qualified technical inspection
- a safety-critical decision system
- an authoritative legal or regulatory source
- an automatic approval mechanism without human oversight

NHTSA complaint narratives describe reported events and may not represent confirmed defects or final technical findings.

Model outputs should be treated as search assistance and classification suggestions. Low-confidence predictions should be reviewed by a person, and even higher-confidence predictions may require review when used in a high-risk process.
