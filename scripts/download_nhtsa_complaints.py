from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "COMPLAINTS_RECEIVED_2025-2026.zip"
)

NHTSA_COMPLAINTS_URL = (
    "https://static.nhtsa.gov/odi/ffdd/cmpl/"
    "COMPLAINTS_RECEIVED_2025-2026.zip"
)


def download_file(
    url: str,
    output_path: Path,
    overwrite: bool = False,
) -> Path:
    """Download a public dataset while preserving the original ZIP file."""

    if output_path.exists() and not overwrite:
        print(f"Dataset already exists: {output_path}")
        return output_path

    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = output_path.with_suffix(f"{output_path.suffix}.part")

    # A user-agent avoids some servers rejecting the default Python request.
    request = Request(
        url,
        headers={
            "User-Agent": (
                "Automotive-After-Sales-Assistant-API/0.3 "
                "(educational project)"
            )
        },
    )

    print(f"Downloading NHTSA complaints from:\n{url}")
    print(f"Saving raw archive to:\n{output_path}")

    try:
        with urlopen(request, timeout=120) as response:
            with temporary_path.open("wb") as output_file:
                shutil.copyfileobj(response, output_file)

        temporary_path.replace(output_path)

    except (HTTPError, URLError, TimeoutError) as exc:
        temporary_path.unlink(missing_ok=True)
        raise RuntimeError(
            f"Could not download the NHTSA complaints archive: {exc}"
        ) from exc

    file_size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"Download complete: {file_size_mb:.1f} MB")

    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download a public NHTSA complaints archive."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Destination path for the downloaded ZIP archive.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Download the file again if it already exists.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    download_file(
        url=NHTSA_COMPLAINTS_URL,
        output_path=args.output,
        overwrite=args.overwrite,
    )


if __name__ == "__main__":
    main()
    