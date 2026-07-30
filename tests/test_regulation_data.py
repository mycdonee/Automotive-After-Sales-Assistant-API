import json

from scripts.validate_regulation_data import (
    EXPECTED_PAIRS,
    EXPECTED_RECORD_IDS,
    PAIRS_PATH,
    RECORDS_PATH,
    load_json,
    load_jsonl,
    main,
)


def test_regulation_data_validator_passes(
    capsys,
) -> None:
    exit_code = main()

    captured = capsys.readouterr()

    assert exit_code == 0
    assert (
        "Regulation data validation passed."
        in captured.out
    )
    assert "JSON Schema validation: passed" in captured.out
    assert "Cross-reference validation: passed" in captured.out
    assert "Contract invariants: passed" in captured.out
    assert captured.err == ""


def test_regulation_record_set_is_complete() -> None:
    records = load_jsonl(RECORDS_PATH)

    record_ids = [
        record["regulation_id"]
        for record in records
    ]

    assert len(records) == 18
    assert record_ids == EXPECTED_RECORD_IDS
    assert len(set(record_ids)) == 18

    assert all(
        record["verification_status"] == "verified"
        for record in records
    )


def test_comparison_pair_set_is_complete() -> None:
    pairs = load_json(PAIRS_PATH)

    assert isinstance(pairs, list)
    assert len(pairs) == 11

    pair_ids = [
        pair["pair_id"]
        for pair in pairs
    ]

    assert len(set(pair_ids)) == 11

    assert [
        pair["pair_number"]
        for pair in pairs
    ] == list(range(1, 12))

    assert all(
        pair["status"] == "approved"
        for pair in pairs
    )

    assert all(
        pair["comparison_level"] == "partial"
        for pair in pairs
    )

    assert all(
        pair["legal_equivalence"] is False
        for pair in pairs
    )


def test_comparison_pairs_reference_known_records() -> None:
    records = load_jsonl(RECORDS_PATH)
    pairs = load_json(PAIRS_PATH)

    record_ids = {
        record["regulation_id"]
        for record in records
    }

    referenced_ids: set[str] = set()

    for pair in pairs:
        left_id = pair["left_regulation_id"]
        right_id = pair["right_regulation_id"]

        assert left_id in record_ids
        assert right_id in record_ids

        assert pair["pair_id"] == (
            f"{left_id}__{right_id}"
        )

        referenced_ids.update(
            {
                left_id,
                right_id,
            }
        )

    assert referenced_ids == record_ids


def test_comparison_pairs_match_locked_mapping() -> None:
    pairs = load_json(PAIRS_PATH)

    actual_mapping = [
        (
            pair["pair_number"],
            pair["left_regulation_id"],
            pair["right_regulation_id"],
            pair["comparison_focus"],
        )
        for pair in pairs
    ]

    assert actual_mapping == EXPECTED_PAIRS


def test_regulation_data_files_are_valid_json() -> None:
    records = load_jsonl(RECORDS_PATH)
    pairs = load_json(PAIRS_PATH)

    for record in records:
        serialized = json.dumps(
            record,
            ensure_ascii=False,
        )

        assert json.loads(serialized) == record

    serialized_pairs = json.dumps(
        pairs,
        ensure_ascii=False,
    )

    assert json.loads(serialized_pairs) == pairs
