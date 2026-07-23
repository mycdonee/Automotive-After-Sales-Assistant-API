from __future__ import annotations

import argparse
import json
from pathlib import Path
from time import perf_counter

import pandas as pd

from app.services.base_retrieval_service import (
    SYNTHETIC_DATA_PATH,
)
from app.services.retrieval_service import (
    TfidfRetrievalService,
)
from app.services.semantic_retrieval_service import (
    SemanticRetrievalService,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_QUERY_PATH = (
    PROJECT_ROOT
    / "evaluation"
    / "retrieval_queries.json"
)

DEFAULT_OUTPUT_PATH = (
    PROJECT_ROOT
    / "evaluation"
    / "retrieval_benchmark.csv"
)


def load_evaluation_queries(
    query_path: Path,
) -> list[dict[str, str]]:
    """Load manually labelled natural-language retrieval queries."""

    if not query_path.exists():
        raise FileNotFoundError(
            f"Evaluation query file not found: {query_path}"
        )

    with query_path.open(
        "r",
        encoding="utf-8",
    ) as query_file:
        queries = json.load(query_file)

    if not isinstance(queries, list) or not queries:
        raise ValueError(
            "Evaluation query file must contain a non-empty list."
        )

    return queries


def evaluate_service(
    method: str,
    service: (
        TfidfRetrievalService
        | SemanticRetrievalService
    ),
    evaluation_queries: list[dict[str, str]],
) -> pd.DataFrame:
    """Measure top-k retrieval hits and per-query search latency."""

    rows: list[dict[str, object]] = []

    for case in evaluation_queries:
        query = case["query"]
        expected_record_id = case["expected_record_id"]

        start_time = perf_counter()

        results = service.search(
            query=query,
            top_k=3,
        )

        latency_ms = (
            perf_counter() - start_time
        ) * 1000

        returned_ids = [
            result.record_id
            for result in results
        ]

        rows.append(
            {
                "method": method,
                "query": query,
                "expected_record_id": expected_record_id,
                "top_1_record_id": (
                    returned_ids[0]
                    if returned_ids
                    else ""
                ),
                "top_3_record_ids": "|".join(returned_ids),
                "top_1_hit": (
                    bool(returned_ids)
                    and returned_ids[0]
                    == expected_record_id
                ),
                "top_3_hit": (
                    expected_record_id in returned_ids
                ),
                "latency_ms": round(
                    latency_ms,
                    3,
                ),
            }
        )

    return pd.DataFrame(rows)


def print_summary(results: pd.DataFrame) -> None:
    summary = (
        results
        .groupby("method")
        .agg(
            top_1_accuracy=("top_1_hit", "mean"),
            top_3_accuracy=("top_3_hit", "mean"),
            average_latency_ms=("latency_ms", "mean"),
        )
        .reset_index()
    )

    summary["top_1_accuracy"] = (
        summary["top_1_accuracy"] * 100
    ).round(1)

    summary["top_3_accuracy"] = (
        summary["top_3_accuracy"] * 100
    ).round(1)

    summary["average_latency_ms"] = (
        summary["average_latency_ms"]
        .round(3)
    )

    print("\nRetrieval benchmark summary")
    print("---------------------------")
    print(summary.to_string(index=False))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compare TF-IDF and semantic retrieval "
            "on labelled natural-language queries."
        )
    )
    parser.add_argument(
        "--queries",
        type=Path,
        default=DEFAULT_QUERY_PATH,
        help="Path to the labelled retrieval query JSON file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Path for the detailed benchmark CSV.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    evaluation_queries = load_evaluation_queries(
        args.queries
    )

    tfidf_service = TfidfRetrievalService(
        data_path=SYNTHETIC_DATA_PATH,
        default_source="Synthetic service records",
    )

    semantic_service = SemanticRetrievalService(
        data_path=SYNTHETIC_DATA_PATH,
        default_source="Synthetic service records",
    )

    tfidf_results = evaluate_service(
        method="tfidf",
        service=tfidf_service,
        evaluation_queries=evaluation_queries,
    )

    semantic_results = evaluate_service(
        method="semantic",
        service=semantic_service,
        evaluation_queries=evaluation_queries,
    )

    combined_results = pd.concat(
        [
            tfidf_results,
            semantic_results,
        ],
        ignore_index=True,
    )

    args.output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    combined_results.to_csv(
        args.output,
        index=False,
    )

    print_summary(combined_results)
    print(f"\nDetailed results saved to: {args.output}")


if __name__ == "__main__":
    main()
    