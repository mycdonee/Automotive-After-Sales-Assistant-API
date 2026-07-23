import pandas as pd

from scripts.prepare_nhtsa_data import (
    clean_text,
    map_category,
    transform_chunk,
)


def test_clean_text_normalizes_whitespace() -> None:
    raw_text = "Brake failure\n  while driving\tat highway speed."

    assert clean_text(raw_text) == (
        "Brake failure while driving at highway speed."
    )


def test_map_category_maps_known_components() -> None:
    assert (
        map_category("SERVICE BRAKES, HYDRAULIC")
        == "Braking System"
    )
    assert (
        map_category("ELECTRICAL SYSTEM")
        == "Electrical System"
    )
    assert map_category("UNKNOWN COMPONENT") is None


def test_transform_chunk_creates_project_records() -> None:
    raw_data = pd.DataFrame(
        [
            {
                "CMPLID": "123456789",
                "ODINO": "987654321",
                "MAKETXT": "EXAMPLE",
                "MODELTXT": "MODEL A",
                "YEARTXT": "2024",
                "CRASH": "N",
                "FIRE": "N",
                "INJURED": "0",
                "DEATHS": "0",
                "COMPDESC": "SERVICE BRAKES",
                "CDESCR": (
                    "The brake pedal became soft and the vehicle "
                    "required a much longer stopping distance."
                ),
                "LDATE": "20260115",
                "PROD_TYPE": "V",
            }
        ]
    )

    transformed = transform_chunk(raw_data)

    assert len(transformed) == 1

    record = transformed.iloc[0]

    assert record["record_id"] == "NHTSA-123456789"
    assert record["category"] == "Braking System"
    assert record["make"] == "EXAMPLE"
    assert record["received_date"] == "2026-01-15"
    assert record["source"] == "NHTSA Consumer Complaints"


def test_transform_chunk_excludes_non_vehicle_records() -> None:
    raw_data = pd.DataFrame(
        [
            {
                "CMPLID": "123456789",
                "ODINO": "987654321",
                "MAKETXT": "EXAMPLE",
                "MODELTXT": "TIRE",
                "YEARTXT": "2024",
                "CRASH": "N",
                "FIRE": "N",
                "INJURED": "0",
                "DEATHS": "0",
                "COMPDESC": "TIRES",
                "CDESCR": (
                    "The tire developed a visible defect during use."
                ),
                "LDATE": "20260115",
                "PROD_TYPE": "T",
            }
        ]
    )

    transformed = transform_chunk(raw_data)

    assert transformed.empty
    