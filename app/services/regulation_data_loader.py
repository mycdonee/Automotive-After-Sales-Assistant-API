from __future__ import annotations

import json
from collections.abc import Mapping
from functools import lru_cache
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from app.schemas.regulation import (
    RegulationComparisonPair,
    RegulationDataset,
    RegulationRecord,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

REGULATION_DATA_DIR = (
    PROJECT_ROOT
    / "data"
    / "regulations"
)

REGULATION_RECORDS_PATH = (
    REGULATION_DATA_DIR
    / "regulation_records.jsonl"
)

REGULATION_COMPARISON_PAIRS_PATH = (
    REGULATION_DATA_DIR
    / "regulation_comparison_pairs.json"
)


def _read_jsonl_objects(
    path: Path,
) -> list[tuple[int, dict[str, Any]]]:
    if not path.exists():
        raise FileNotFoundError(
            f"Regulation records file not found: {path}"
        )

    entries: list[
        tuple[int, dict[str, Any]]
    ] = []

    for line_number, line in enumerate(
        path.read_text(
            encoding="utf-8"
        ).splitlines(),
        start=1,
    ):
        if not line.strip():
            raise ValueError(
                f"Blank JSONL line in {path} "
                f"at line {line_number}."
            )

        try:
            value = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError(
                f"Invalid JSON in {path} "
                f"at line {line_number}, "
                f"column {error.colno}: "
                f"{error.msg}"
            ) from error

        if not isinstance(value, dict):
            raise ValueError(
                f"Line {line_number} in {path} "
                "must contain one JSON object."
            )

        entries.append(
            (
                line_number,
                value,
            )
        )

    if not entries:
        raise ValueError(
            "Regulation records dataset must not be empty."
        )

    return entries


def _read_json_array(
    path: Path,
) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(
            f"Regulation comparison file not found: {path}"
        )

    try:
        value = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON in {path}: "
            f"line {error.lineno}, "
            f"column {error.colno}: "
            f"{error.msg}"
        ) from error

    if not isinstance(value, list):
        raise ValueError(
            f"{path} must contain one JSON array."
        )

    if not value:
        raise ValueError(
            "Regulation comparison dataset "
            "must not be empty."
        )

    if not all(
        isinstance(item, dict)
        for item in value
    ):
        raise ValueError(
            f"Every item in {path} "
            "must be a JSON object."
        )

    return value


def _validate_unique(
    values: list[str | int],
    label: str,
) -> None:
    if len(values) != len(set(values)):
        raise ValueError(
            f"{label} must be unique."
        )


def load_regulation_records(
    path: Path = REGULATION_RECORDS_PATH,
) -> tuple[RegulationRecord, ...]:
    """Load and validate committed regulation records."""

    records: list[RegulationRecord] = []

    for line_number, value in _read_jsonl_objects(
        path
    ):
        try:
            record = RegulationRecord.model_validate(
                value
            )
        except ValidationError as error:
            raise ValueError(
                f"Invalid regulation record in {path} "
                f"at line {line_number}: {error}"
            ) from error

        records.append(record)

    _validate_unique(
        [
            record.regulation_id
            for record in records
        ],
        "Regulation IDs",
    )

    return tuple(records)


def load_regulation_comparison_pairs(
    path: Path = REGULATION_COMPARISON_PAIRS_PATH,
) -> tuple[RegulationComparisonPair, ...]:
    """Load and validate committed comparison pairs."""

    pairs: list[
        RegulationComparisonPair
    ] = []

    for index, value in enumerate(
        _read_json_array(path),
    ):
        try:
            pair = (
                RegulationComparisonPair
                .model_validate(value)
            )
        except ValidationError as error:
            raise ValueError(
                f"Invalid comparison pair in {path} "
                f"at array index {index}: {error}"
            ) from error

        pairs.append(pair)

    _validate_unique(
        [
            pair.pair_id
            for pair in pairs
        ],
        "Comparison-pair IDs",
    )

    _validate_unique(
        [
            pair.pair_number
            for pair in pairs
        ],
        "Comparison-pair numbers",
    )

    return tuple(pairs)


def _validate_pair_references(
    records: tuple[
        RegulationRecord,
        ...,
    ],
    pairs: tuple[
        RegulationComparisonPair,
        ...,
    ],
) -> dict[str, RegulationRecord]:
    record_by_id = {
        record.regulation_id: record
        for record in records
    }

    for pair in pairs:
        left_record = record_by_id.get(
            pair.left_regulation_id
        )

        if left_record is None:
            raise ValueError(
                f"{pair.pair_id} references unknown "
                f"left regulation "
                f"{pair.left_regulation_id}."
            )

        right_record = record_by_id.get(
            pair.right_regulation_id
        )

        if right_record is None:
            raise ValueError(
                f"{pair.pair_id} references unknown "
                f"right regulation "
                f"{pair.right_regulation_id}."
            )

        expected_pair_id = (
            f"{pair.left_regulation_id}__"
            f"{pair.right_regulation_id}"
        )

        if pair.pair_id != expected_pair_id:
            raise ValueError(
                f"{pair.pair_id} does not match "
                "its referenced regulation IDs."
            )

        if left_record.jurisdiction != "UNECE":
            raise ValueError(
                f"{pair.pair_id} must use a UNECE "
                "record on the left."
            )

        if (
            right_record.jurisdiction
            != "United States"
        ):
            raise ValueError(
                f"{pair.pair_id} must use a United States "
                "record on the right."
            )

        if (
            pair.regulatory_system
            != left_record.regulatory_system
        ):
            raise ValueError(
                f"{pair.pair_id} regulatory system "
                "does not match its left record."
            )

        if (
            pair.regulatory_system
            != right_record.regulatory_system
        ):
            raise ValueError(
                f"{pair.pair_id} regulatory system "
                "does not match its right record."
            )

    return record_by_id


def _display_label(value: str) -> str:
    return value.replace(
        "_",
        " ",
    )


def _format_values(
    values: tuple[str, ...],
) -> str:
    return "; ".join(values)


def build_regulation_search_text(
    record: RegulationRecord,
) -> str:
    """Build derived searchable text for one regulation."""

    parts = [
        (
            "Official identifier: "
            f"{record.official_identifier}."
        ),
        (
            "Aliases: "
            f"{_format_values(record.aliases)}."
        ),
        f"Title: {record.title}.",
        (
            "Regulatory system: "
            f"{_display_label(record.regulatory_system)}."
        ),
        (
            "Regulated object: "
            f"{record.regulated_object}."
        ),
        (
            "Scope: "
            f"{record.scope_summary}"
        ),
    ]

    if record.vehicle_applicability:
        parts.append(
            "Vehicle applicability: "
            f"{_format_values(record.vehicle_applicability)}."
        )

    parts.extend(
        [
            (
                "Requirement topics: "
                f"{_format_values(record.requirement_topics)}."
            ),
            (
                "Reviewed version: "
                f"{record.reviewed_version}."
            ),
        ]
    )

    if record.special_status_notes:
        parts.append(
            "Special status notes: "
            f"{_format_values(record.special_status_notes)}."
        )

    return " ".join(parts)


def build_comparison_search_text(
    pair: RegulationComparisonPair,
    record_by_id: Mapping[
        str,
        RegulationRecord,
    ],
) -> str:
    """Build derived searchable text for one comparison pair."""

    left_record = record_by_id[
        pair.left_regulation_id
    ]

    right_record = record_by_id[
        pair.right_regulation_id
    ]

    return " ".join(
        [
            (
                "Left regulation: "
                f"{build_regulation_search_text(left_record)}"
            ),
            (
                "Right regulation: "
                f"{build_regulation_search_text(right_record)}"
            ),
            (
                "Comparison focus: "
                f"{_display_label(pair.comparison_focus)}."
            ),
            (
                "Overlap summary: "
                f"{pair.overlap_summary}"
            ),
            (
                "Comparable topics: "
                f"{_format_values(pair.comparable_topics)}."
            ),
            (
                "Scope differences: "
                f"{_format_values(pair.scope_differences)}."
            ),
        ]
    )


def load_regulation_dataset(
    records_path: Path = REGULATION_RECORDS_PATH,
    pairs_path: Path = (
        REGULATION_COMPARISON_PAIRS_PATH
    ),
) -> RegulationDataset:
    """Load, validate, and prepare the complete dataset."""

    records = load_regulation_records(
        records_path
    )

    pairs = load_regulation_comparison_pairs(
        pairs_path
    )

    record_by_id = _validate_pair_references(
        records,
        pairs,
    )

    regulation_search_documents = tuple(
        build_regulation_search_text(record)
        for record in records
    )

    comparison_search_documents = tuple(
        build_comparison_search_text(
            pair,
            record_by_id,
        )
        for pair in pairs
    )

    if (
        len(regulation_search_documents)
        != len(records)
    ):
        raise ValueError(
            "Regulation search-document count mismatch."
        )

    if (
        len(comparison_search_documents)
        != len(pairs)
    ):
        raise ValueError(
            "Comparison search-document count mismatch."
        )

    return RegulationDataset(
        records=records,
        comparison_pairs=pairs,
        regulation_search_documents=(
            regulation_search_documents
        ),
        comparison_search_documents=(
            comparison_search_documents
        ),
    )


@lru_cache(maxsize=1)
def get_regulation_dataset() -> RegulationDataset:
    """Load the committed regulation dataset once per process."""

    return load_regulation_dataset()
