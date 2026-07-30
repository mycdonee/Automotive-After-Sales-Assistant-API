from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "regulations"

RECORDS_PATH = DATA_DIR / "regulation_records.jsonl"
PAIRS_PATH = DATA_DIR / "regulation_comparison_pairs.json"

RECORD_SCHEMA_PATH = (
    DATA_DIR / "schemas" / "regulation_record.schema.json"
)
PAIR_SCHEMA_PATH = (
    DATA_DIR
    / "schemas"
    / "regulation_comparison_pair.schema.json"
)

VERIFICATION_PATH = (
    DATA_DIR / "comparability_verification.md"
)


EXPECTED_RECORD_IDS = [
    "unece_r13h",
    "fmvss_135",
    "unece_r140",
    "fmvss_126",
    "unece_r14",
    "fmvss_210",
    "unece_r16",
    "fmvss_209",
    "unece_r145",
    "fmvss_225",
    "unece_r48",
    "unece_r148",
    "unece_r149",
    "unece_r150",
    "unece_r104",
    "unece_r27",
    "fmvss_108",
    "fmvss_125",
]


EXPECTED_PAIRS = [
    (
        1,
        "unece_r13h",
        "fmvss_135",
        "light_vehicle_braking",
    ),
    (
        2,
        "unece_r140",
        "fmvss_126",
        "electronic_stability_control",
    ),
    (
        3,
        "unece_r14",
        "fmvss_210",
        "seat_belt_anchorages",
    ),
    (
        4,
        "unece_r16",
        "fmvss_209",
        "seat_belt_assemblies",
    ),
    (
        5,
        "unece_r145",
        "fmvss_225",
        "child_restraint_anchorages",
    ),
    (
        6,
        "unece_r48",
        "fmvss_108",
        "vehicle_lighting_installation",
    ),
    (
        7,
        "unece_r148",
        "fmvss_108",
        "light_signalling_device_performance",
    ),
    (
        8,
        "unece_r149",
        "fmvss_108",
        "road_illumination_device_performance",
    ),
    (
        9,
        "unece_r150",
        "fmvss_108",
        "retro_reflective_device_performance",
    ),
    (
        10,
        "unece_r104",
        "fmvss_108",
        "vehicle_conspicuity_marking_requirements",
    ),
    (
        11,
        "unece_r27",
        "fmvss_125",
        "portable_advance_warning_triangle_performance",
    ),
]


def load_json(path: Path) -> Any:
    try:
        return json.loads(
            path.read_text(encoding="utf-8")
        )
    except FileNotFoundError as error:
        raise RuntimeError(
            f"Required file not found: {path}"
        ) from error
    except json.JSONDecodeError as error:
        raise RuntimeError(
            f"Invalid JSON in {path}: "
            f"line {error.lineno}, "
            f"column {error.colno}: "
            f"{error.msg}"
        ) from error


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    try:
        lines = path.read_text(
            encoding="utf-8"
        ).splitlines()
    except FileNotFoundError as error:
        raise RuntimeError(
            f"Required file not found: {path}"
        ) from error

    records: list[dict[str, Any]] = []

    for line_number, line in enumerate(
        lines,
        start=1,
    ):
        if not line.strip():
            raise RuntimeError(
                f"Blank line in {path} "
                f"at line {line_number}."
            )

        try:
            value = json.loads(line)
        except json.JSONDecodeError as error:
            raise RuntimeError(
                f"Invalid JSON in {path} "
                f"at line {line_number}, "
                f"column {error.colno}: "
                f"{error.msg}"
            ) from error

        if not isinstance(value, dict):
            raise RuntimeError(
                f"Line {line_number} in {path} "
                "must contain one JSON object."
            )

        records.append(value)

    return records


def format_error_path(error: Any) -> str:
    path = "$"

    for part in error.absolute_path:
        if isinstance(part, int):
            path += f"[{part}]"
        else:
            path += f".{part}"

    return path


def validate_schema_definition(
    schema: dict[str, Any],
    path: Path,
) -> None:
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as error:
        raise RuntimeError(
            f"Invalid JSON Schema in {path}: "
            f"{error.message}"
        ) from error


def collect_schema_errors(
    instances: list[dict[str, Any]],
    schema: dict[str, Any],
    label: str,
) -> list[str]:
    validator = Draft202012Validator(
        schema,
        format_checker=FormatChecker(),
    )

    errors: list[str] = []

    for index, instance in enumerate(instances):
        instance_id = (
            instance.get("regulation_id")
            or instance.get("pair_id")
            or f"index-{index}"
        )

        instance_errors = list(
            validator.iter_errors(instance)
        )

        instance_errors.sort(
            key=lambda error: (
                str(list(error.absolute_path)),
                error.message,
            )
        )

        for error in instance_errors:
            errors.append(
                f"{label} {instance_id} "
                f"at {format_error_path(error)}: "
                f"{error.message}"
            )

    return errors


def validate_record_invariants(
    records: list[dict[str, Any]],
) -> list[str]:
    errors: list[str] = []

    if len(records) != 18:
        errors.append(
            f"Expected 18 regulation records, "
            f"found {len(records)}."
        )

    record_ids = [
        record.get("regulation_id")
        for record in records
    ]

    if record_ids != EXPECTED_RECORD_IDS:
        errors.append(
            "Regulation records are not in the "
            "canonical ID order or the locked set changed."
        )

    if len(set(record_ids)) != len(record_ids):
        errors.append(
            "Regulation IDs are not unique."
        )

    for record in records:
        regulation_id = record.get(
            "regulation_id",
            "<missing>",
        )

        jurisdiction = record.get("jurisdiction")
        source_format = record.get("source_format")
        content_date = record.get(
            "source_content_date"
        )

        if record.get("verification_status") != "verified":
            errors.append(
                f"{regulation_id}: "
                "verification_status must be verified."
            )

        if jurisdiction == "UNECE":
            if not str(regulation_id).startswith(
                "unece_"
            ):
                errors.append(
                    f"{regulation_id}: UNECE IDs must "
                    "start with unece_."
                )

            if source_format not in {"pdf", "mixed"}:
                errors.append(
                    f"{regulation_id}: UNECE source_format "
                    "must be pdf or mixed."
                )

            if content_date is not None:
                errors.append(
                    f"{regulation_id}: UNECE "
                    "source_content_date must be null "
                    "when no single date applies."
                )

        elif jurisdiction == "United States":
            if not str(regulation_id).startswith(
                "fmvss_"
            ):
                errors.append(
                    f"{regulation_id}: United States IDs "
                    "must start with fmvss_."
                )

            if source_format != "xml":
                errors.append(
                    f"{regulation_id}: FMVSS "
                    "source_format must be xml."
                )

            if content_date is None:
                errors.append(
                    f"{regulation_id}: date-versioned "
                    "eCFR records must have "
                    "source_content_date."
                )

    return errors


def validate_pair_invariants(
    records: list[dict[str, Any]],
    pairs: list[dict[str, Any]],
    verification_text: str,
) -> list[str]:
    errors: list[str] = []

    if len(pairs) != 11:
        errors.append(
            f"Expected 11 comparison pairs, "
            f"found {len(pairs)}."
        )

    record_by_id = {
        record["regulation_id"]: record
        for record in records
        if "regulation_id" in record
    }

    pair_ids = [
        pair.get("pair_id")
        for pair in pairs
    ]

    if len(set(pair_ids)) != len(pair_ids):
        errors.append(
            "Comparison-pair IDs are not unique."
        )

    for index, expected in enumerate(
        EXPECTED_PAIRS
    ):
        if index >= len(pairs):
            break

        (
            expected_number,
            expected_left,
            expected_right,
            expected_focus,
        ) = expected

        pair = pairs[index]

        expected_pair_id = (
            f"{expected_left}__{expected_right}"
        )

        if pair.get("pair_number") != expected_number:
            errors.append(
                f"Pair array index {index} must use "
                f"pair_number {expected_number}."
            )

        if pair.get("pair_id") != expected_pair_id:
            errors.append(
                f"Pair {expected_number} must use "
                f"pair_id {expected_pair_id}."
            )

        if (
            pair.get("left_regulation_id")
            != expected_left
        ):
            errors.append(
                f"Pair {expected_number} has an "
                "unexpected left regulation."
            )

        if (
            pair.get("right_regulation_id")
            != expected_right
        ):
            errors.append(
                f"Pair {expected_number} has an "
                "unexpected right regulation."
            )

        if (
            pair.get("comparison_focus")
            != expected_focus
        ):
            errors.append(
                f"Pair {expected_number} has an "
                "unexpected comparison focus."
            )

    referenced_ids: set[str] = set()

    for pair in pairs:
        pair_id = pair.get(
            "pair_id",
            "<missing>",
        )

        left_id = pair.get("left_regulation_id")
        right_id = pair.get("right_regulation_id")
        pair_number = pair.get("pair_number")

        expected_pair_id = (
            f"{left_id}__{right_id}"
        )

        if pair_id != expected_pair_id:
            errors.append(
                f"{pair_id}: pair_id does not match "
                "left and right regulation IDs."
            )

        left_record = record_by_id.get(left_id)
        right_record = record_by_id.get(right_id)

        if left_record is None:
            errors.append(
                f"{pair_id}: unknown left regulation "
                f"{left_id}."
            )
        else:
            referenced_ids.add(left_id)

            if (
                left_record.get("jurisdiction")
                != "UNECE"
            ):
                errors.append(
                    f"{pair_id}: left regulation "
                    "must be UNECE."
                )

            if (
                pair.get("regulatory_system")
                != left_record.get("regulatory_system")
            ):
                errors.append(
                    f"{pair_id}: regulatory_system "
                    "does not match the left record."
                )

        if right_record is None:
            errors.append(
                f"{pair_id}: unknown right regulation "
                f"{right_id}."
            )
        else:
            referenced_ids.add(right_id)

            if (
                right_record.get("jurisdiction")
                != "United States"
            ):
                errors.append(
                    f"{pair_id}: right regulation "
                    "must be United States."
                )

            if (
                pair.get("regulatory_system")
                != right_record.get("regulatory_system")
            ):
                errors.append(
                    f"{pair_id}: regulatory_system "
                    "does not match the right record."
                )

        if pair.get("status") != "approved":
            errors.append(
                f"{pair_id}: status must be approved."
            )

        if pair.get("comparison_level") != "partial":
            errors.append(
                f"{pair_id}: comparison_level must "
                "be partial for the locked dataset."
            )

        if pair.get("legal_equivalence") is not False:
            errors.append(
                f"{pair_id}: legal_equivalence "
                "must be false."
            )

        expected_reference = (
            "data/regulations/"
            "comparability_verification.md "
            f"— Pair {pair_number}"
        )

        if (
            pair.get("verification_reference")
            != expected_reference
        ):
            errors.append(
                f"{pair_id}: invalid "
                "verification_reference."
            )

        heading = f"## Pair {pair_number} —"

        if heading not in verification_text:
            errors.append(
                f"{pair_id}: corresponding heading "
                "not found in "
                "comparability_verification.md."
            )

    expected_ids = set(EXPECTED_RECORD_IDS)

    if referenced_ids != expected_ids:
        missing = sorted(
            expected_ids - referenced_ids
        )
        unexpected = sorted(
            referenced_ids - expected_ids
        )

        errors.append(
            "Comparison-pair coverage mismatch: "
            f"unreferenced={missing}, "
            f"unexpected={unexpected}."
        )

    return errors


def main() -> int:
    try:
        record_schema = load_json(
            RECORD_SCHEMA_PATH
        )
        pair_schema = load_json(
            PAIR_SCHEMA_PATH
        )

        if not isinstance(record_schema, dict):
            raise RuntimeError(
                "Regulation record schema must "
                "be a JSON object."
            )

        if not isinstance(pair_schema, dict):
            raise RuntimeError(
                "Comparison pair schema must "
                "be a JSON object."
            )

        validate_schema_definition(
            record_schema,
            RECORD_SCHEMA_PATH,
        )

        validate_schema_definition(
            pair_schema,
            PAIR_SCHEMA_PATH,
        )

        records = load_jsonl(RECORDS_PATH)
        pairs_data = load_json(PAIRS_PATH)

        if not isinstance(pairs_data, list):
            raise RuntimeError(
                f"{PAIRS_PATH} must contain "
                "one JSON array."
            )

        if not all(
            isinstance(pair, dict)
            for pair in pairs_data
        ):
            raise RuntimeError(
                f"Every item in {PAIRS_PATH} "
                "must be a JSON object."
            )

        pairs: list[dict[str, Any]] = pairs_data

        verification_text = (
            VERIFICATION_PATH.read_text(
                encoding="utf-8"
            )
        )

    except (
        RuntimeError,
        FileNotFoundError,
    ) as error:
        print(
            f"Validation setup failed: {error}",
            file=sys.stderr,
        )
        return 1

    errors: list[str] = []

    errors.extend(
        collect_schema_errors(
            records,
            record_schema,
            "Regulation record",
        )
    )

    errors.extend(
        collect_schema_errors(
            pairs,
            pair_schema,
            "Comparison pair",
        )
    )

    errors.extend(
        validate_record_invariants(records)
    )

    errors.extend(
        validate_pair_invariants(
            records,
            pairs,
            verification_text,
        )
    )

    if errors:
        print(
            f"Validation failed with "
            f"{len(errors)} error(s):",
            file=sys.stderr,
        )

        for error in errors:
            print(
                f"- {error}",
                file=sys.stderr,
            )

        return 1

    print("Regulation data validation passed.")
    print(f"Records: {len(records)}")
    print(f"Unique record IDs: {len(EXPECTED_RECORD_IDS)}")
    print(f"Comparison pairs: {len(pairs)}")
    print("JSON Schema validation: passed")
    print("Cross-reference validation: passed")
    print("Contract invariants: passed")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
