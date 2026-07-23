from __future__ import annotations

import argparse
import csv
import re
import zipfile
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_INPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "COMPLAINTS_RECEIVED_2025-2026.zip"
)

DEFAULT_OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "nhtsa_service_records.csv"
)


# Field order follows the official NHTSA complaint flat-file description.
NHTSA_COLUMNS = [
    "CMPLID",
    "ODINO",
    "MFR_NAME",
    "MAKETXT",
    "MODELTXT",
    "YEARTXT",
    "CRASH",
    "FAILDATE",
    "FIRE",
    "INJURED",
    "DEATHS",
    "COMPDESC",
    "CITY",
    "STATE",
    "VIN",
    "DATEA",
    "LDATE",
    "MILES",
    "OCCURENCES",
    "CDESCR",
    "CMPL_TYPE",
    "POLICE_RPT_YN",
    "PURCH_DT",
    "ORIG_OWNER_YN",
    "ANTI_BRAKES_YN",
    "CRUISE_CONT_YN",
    "NUM_CYLS",
    "DRIVE_TRAIN",
    "FUEL_SYS",
    "FUEL_TYPE",
    "TRANS_TYPE",
    "VEH_SPEED",
    "DOT",
    "TIRE_SIZE",
    "LOC_OF_TIRE",
    "TIRE_FAIL_TYPE",
    "ORIG_EQUIP_YN",
    "MANUF_DT",
    "SEAT_TYPE",
    "RESTRAINT_TYPE",
    "DEALER_NAME",
    "DEALER_TEL",
    "DEALER_CITY",
    "DEALER_STATE",
    "DEALER_ZIP",
    "PROD_TYPE",
    "REPAIRED_YN",
    "MEDICAL_ATTN",
    "VEHICLES_TOWED_YN",
    "STATE_OF_INCIDENT",
    "VEHICLE_OPERATOR",
]


CATEGORY_RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "Braking System",
        (
            "SERVICE BRAKES",
            "PARKING BRAKE",
            "BRAKE",
        ),
    ),
    (
        "Engine",
        (
            "ENGINE",
            "ENGINE COOLING",
        ),
    ),
    (
        "Electrical System",
        (
            "ELECTRICAL",
            "BATTERY",
            "ALTERNATOR",
            "STARTER",
        ),
    ),
    (
        "Air Bags",
        (
            "AIR BAG",
            "AIR BAGS",
        ),
    ),
    (
        "Steering",
        (
            "STEERING",
        ),
    ),
    (
        "Power Train",
        (
            "POWER TRAIN",
            "TRANSMISSION",
            "CLUTCH",
        ),
    ),
    (
        "Visibility",
        (
            "VISIBILITY",
            "WINDSHIELD",
            "WIPER",
        ),
    ),
    (
        "Fuel System",
        (
            "FUEL",
        ),
    ),
    (
        "Tires and Wheels",
        (
            "TIRE",
            "WHEEL",
        ),
    ),
    (
        "Seat Belts",
        (
            "SEAT BELT",
        ),
    ),
    (
        "Driver Assistance",
        (
            "FORWARD COLLISION",
            "LANE DEPARTURE",
            "BACK OVER PREVENTION",
            "ADAPTIVE CRUISE",
        ),
    ),
    (
        "Body and Structure",
        (
            "STRUCTURE",
            "LATCHES/LOCKS",
            "DOOR",
        ),
    ),
)


OUTPUT_COLUMNS = [
    "record_id",
    "title",
    "description",
    "category",
    "component",
    "make",
    "model",
    "model_year",
    "received_date",
    "crash",
    "fire",
    "injured",
    "deaths",
    "source",
]


def clean_text(value: object) -> str:
    """Normalize whitespace and remove control characters from text."""

    if value is None or pd.isna(value):
        return ""

    text = str(value)
    text = re.sub(r"[\r\n\t]+", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def map_category(component: object) -> str | None:
    """Map detailed NHTSA component labels to broader issue categories."""

    normalized_component = clean_text(component).upper()

    if not normalized_component:
        return None

    for category, keywords in CATEGORY_RULES:
        if any(keyword in normalized_component for keyword in keywords):
            return category

    return None


def build_title(component: object) -> str:
    """Create a readable title from the NHTSA component description."""

    normalized_component = clean_text(component)

    if not normalized_component:
        return "Automotive safety complaint"

    readable_component = normalized_component.replace(":", " - ")
    readable_component = readable_component.replace("_", " ")

    return readable_component.title()


def parse_received_date(value: object) -> str:
    """Convert NHTSA YYYYMMDD dates to ISO format where possible."""

    raw_date = clean_text(value)

    if not raw_date or len(raw_date) != 8:
        return ""

    parsed_date = pd.to_datetime(
        raw_date,
        format="%Y%m%d",
        errors="coerce",
    )

    if pd.isna(parsed_date):
        return ""

    return parsed_date.strftime("%Y-%m-%d")


def transform_chunk(chunk: pd.DataFrame) -> pd.DataFrame:
    """Clean one raw-data chunk and convert it to the project schema."""

    required_columns = {
        "CMPLID",
        "ODINO",
        "MAKETXT",
        "MODELTXT",
        "YEARTXT",
        "CRASH",
        "FIRE",
        "INJURED",
        "DEATHS",
        "COMPDESC",
        "CDESCR",
        "LDATE",
        "PROD_TYPE",
    }

    missing_columns = required_columns.difference(chunk.columns)

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Raw NHTSA data is missing columns: {missing}")

    working = chunk.copy()

    # Only vehicle complaints are relevant to this application.
    working = working[
        working["PROD_TYPE"].fillna("").str.upper().eq("V")
    ].copy()

    working["description"] = working["CDESCR"].map(clean_text)
    working["component"] = working["COMPDESC"].map(clean_text)
    working["category"] = working["component"].map(map_category)

    # Very short narratives carry little value for retrieval or training.
    working = working[
        working["description"].str.len().ge(40)
        & working["component"].ne("")
        & working["category"].notna()
    ].copy()

    transformed = pd.DataFrame(
        {
            "record_id": (
                "NHTSA-"
                + working["CMPLID"].fillna(
                    working["ODINO"]
                ).map(clean_text)
            ),
            "title": working["component"].map(build_title),
            "description": working["description"],
            "category": working["category"],
            "component": working["component"],
            "make": working["MAKETXT"].map(clean_text),
            "model": working["MODELTXT"].map(clean_text),
            "model_year": working["YEARTXT"].map(clean_text),
            "received_date": working["LDATE"].map(
                parse_received_date
            ),
            "crash": working["CRASH"].map(clean_text),
            "fire": working["FIRE"].map(clean_text),
            "injured": working["INJURED"].map(clean_text),
            "deaths": working["DEATHS"].map(clean_text),
            "source": "NHTSA Consumer Complaints",
        }
    )

    transformed = transformed[
        transformed["record_id"].ne("NHTSA-")
    ].copy()

    return transformed[OUTPUT_COLUMNS]


def find_data_member(archive: zipfile.ZipFile) -> str:
    """Find the tab-delimited complaint file inside the ZIP archive."""

    candidates = [
        name
        for name in archive.namelist()
        if not name.endswith("/")
        and Path(name).suffix.lower() in {".txt", ".csv", ".lst"}
    ]

    if not candidates:
        raise ValueError(
            "No complaint data file was found inside the archive."
        )

    # The largest text-like member is normally the complaint data file.
    return max(
        candidates,
        key=lambda name: archive.getinfo(name).file_size,
    )


def read_and_transform_archive(
    input_path: Path,
    chunk_size: int = 50_000,
) -> pd.DataFrame:
    """Read the compressed flat file in chunks to control memory use."""

    if not input_path.exists():
        raise FileNotFoundError(
            f"NHTSA archive not found: {input_path}"
        )

    transformed_chunks: list[pd.DataFrame] = []

    with zipfile.ZipFile(input_path) as archive:
        member_name = find_data_member(archive)

        print(f"Reading archive member: {member_name}")

        with archive.open(member_name) as raw_file:
            reader = pd.read_csv(
                raw_file,
                sep="\t",
                names=NHTSA_COLUMNS,
                dtype=str,
                chunksize=chunk_size,
                keep_default_na=False,
                on_bad_lines="skip",
                quoting=csv.QUOTE_NONE,
                low_memory=False,
            )

            for chunk_number, chunk in enumerate(reader, start=1):
                transformed = transform_chunk(chunk)

                if not transformed.empty:
                    transformed_chunks.append(transformed)

                print(
                    "Processed chunk "
                    f"{chunk_number}: "
                    f"{len(transformed):,} usable records"
                )

    if not transformed_chunks:
        raise ValueError(
            "No usable vehicle complaints remained after cleaning."
        )

    return pd.concat(
        transformed_chunks,
        ignore_index=True,
    )


def create_balanced_sample(
    records: pd.DataFrame,
    max_records: int,
    max_per_category: int,
    random_state: int,
) -> pd.DataFrame:
    """Create a deterministic sample without one category dominating."""

    records = records.drop_duplicates(
        subset=[
            "record_id",
            "component",
            "description",
        ]
    ).copy()

    sampled_groups: list[pd.DataFrame] = []

    for _, category_records in records.groupby(
        "category",
        sort=True,
    ):
        sample_size = min(
            len(category_records),
            max_per_category,
        )

        sampled_groups.append(
            category_records.sample(
                n=sample_size,
                random_state=random_state,
            )
        )

    sampled = pd.concat(
        sampled_groups,
        ignore_index=True,
    )

    if len(sampled) > max_records:
        sampled = sampled.sample(
            n=max_records,
            random_state=random_state,
        )

    return sampled.sort_values(
        by=["category", "record_id"],
        kind="stable",
    ).reset_index(drop=True)


def save_processed_data(
    records: pd.DataFrame,
    output_path: Path,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    temporary_path = output_path.with_suffix(
        f"{output_path.suffix}.tmp"
    )

    records.to_csv(
        temporary_path,
        index=False,
    )

    temporary_path.replace(output_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Clean and sample public NHTSA consumer complaint data."
        )
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT_PATH,
        help="Path to the downloaded NHTSA ZIP archive.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Path for the processed CSV dataset.",
    )
    parser.add_argument(
        "--max-records",
        type=int,
        default=2_000,
        help="Maximum number of processed records to keep.",
    )
    parser.add_argument(
        "--max-per-category",
        type=int,
        default=250,
        help="Maximum records retained for each broad category.",
    )
    parser.add_argument(
        "--random-state",
        type=int,
        default=42,
        help="Random seed used for reproducible sampling.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    records = read_and_transform_archive(
        input_path=args.input,
    )

    sampled_records = create_balanced_sample(
        records=records,
        max_records=args.max_records,
        max_per_category=args.max_per_category,
        random_state=args.random_state,
    )

    save_processed_data(
        records=sampled_records,
        output_path=args.output,
    )

    print("\nProcessed dataset summary")
    print("-------------------------")
    print(f"Total records: {len(sampled_records):,}")
    print(f"Output path: {args.output}")
    print("\nCategory distribution:")
    print(
        sampled_records["category"]
        .value_counts()
        .sort_index()
        .to_string()
    )


if __name__ == "__main__":
    main()
    