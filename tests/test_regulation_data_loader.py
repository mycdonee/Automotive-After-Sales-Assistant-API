import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from app.services.regulation_data_loader import (
    REGULATION_COMPARISON_PAIRS_PATH,
    REGULATION_RECORDS_PATH,
    build_comparison_search_text,
    build_regulation_search_text,
    get_regulation_dataset,
    load_regulation_comparison_pairs,
    load_regulation_dataset,
    load_regulation_records,
)


def test_load_regulation_dataset() -> None:
    dataset = load_regulation_dataset()

    assert len(dataset.records) == 18
    assert len(dataset.comparison_pairs) == 11

    assert (
        len(dataset.regulation_search_documents)
        == len(dataset.records)
    )

    assert (
        len(dataset.comparison_search_documents)
        == len(dataset.comparison_pairs)
    )

    assert (
        dataset.records[0].regulation_id
        == "unece_r13h"
    )

    assert (
        dataset.records[-1].regulation_id
        == "fmvss_125"
    )

    assert (
        dataset.comparison_pairs[-1].pair_id
        == "unece_r27__fmvss_125"
    )


def test_get_regulation_dataset_is_cached() -> None:
    get_regulation_dataset.cache_clear()

    first = get_regulation_dataset()
    second = get_regulation_dataset()

    assert first is second

    cache_info = get_regulation_dataset.cache_info()

    assert cache_info.misses == 1
    assert cache_info.hits == 1


def test_regulation_models_are_frozen() -> None:
    dataset = load_regulation_dataset()
    record = dataset.records[0]

    with pytest.raises(
        ValidationError,
        match="frozen",
    ):
        record.title = "Modified title"


def test_regulation_search_text_contains_required_fields() -> None:
    records = load_regulation_records()

    record = next(
        item
        for item in records
        if item.regulation_id == "unece_r27"
    )

    search_text = build_regulation_search_text(
        record
    )

    assert "UN Regulation No. 27" in search_text
    assert "UN R27" in search_text
    assert "Advance warning triangles" in search_text
    assert "lighting and light signalling" in search_text
    assert "Portable advance warning triangles" in search_text
    assert "equilateral-triangle shape" in search_text
    assert "Revision 3, 05 series" in search_text
    assert "transitional provisions" in search_text


def test_comparison_search_text_contains_both_regulations() -> None:
    records = load_regulation_records()
    pairs = load_regulation_comparison_pairs()

    record_by_id = {
        record.regulation_id: record
        for record in records
    }

    pair = next(
        item
        for item in pairs
        if item.pair_number == 11
    )

    search_text = build_comparison_search_text(
        pair,
        record_by_id,
    )

    assert "UN Regulation No. 27" in search_text
    assert "FMVSS No. 125" in search_text

    assert (
        "portable advance warning triangle performance"
        in search_text
    )

    assert "equilateral-triangle configuration" in search_text
    assert "10,000 pounds GVWR" in search_text


def test_duplicate_regulation_ids_are_rejected(
    tmp_path: Path,
) -> None:
    lines = REGULATION_RECORDS_PATH.read_text(
        encoding="utf-8"
    ).splitlines()

    duplicate_path = (
        tmp_path / "duplicate_records.jsonl"
    )

    duplicate_path.write_text(
        "\n".join(
            [
                lines[0],
                lines[0],
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="Regulation IDs must be unique",
    ):
        load_regulation_records(
            duplicate_path
        )


def test_extra_regulation_fields_are_rejected(
    tmp_path: Path,
) -> None:
    first_line = (
        REGULATION_RECORDS_PATH
        .read_text(encoding="utf-8")
        .splitlines()[0]
    )

    record = json.loads(first_line)
    record["unexpected_field"] = "not allowed"

    invalid_path = (
        tmp_path / "invalid_record.jsonl"
    )

    invalid_path.write_text(
        json.dumps(record) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="Invalid regulation record",
    ):
        load_regulation_records(
            invalid_path
        )


def test_unknown_comparison_reference_is_rejected(
    tmp_path: Path,
) -> None:
    pairs = json.loads(
        REGULATION_COMPARISON_PAIRS_PATH
        .read_text(encoding="utf-8")
    )

    pairs[0]["right_regulation_id"] = "fmvss_999"
    pairs[0]["pair_id"] = (
        "unece_r13h__fmvss_999"
    )

    invalid_pairs_path = (
        tmp_path / "invalid_pairs.json"
    )

    invalid_pairs_path.write_text(
        json.dumps(
            pairs,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="references unknown right regulation",
    ):
        load_regulation_dataset(
            records_path=REGULATION_RECORDS_PATH,
            pairs_path=invalid_pairs_path,
        )
