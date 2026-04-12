from __future__ import annotations

import argparse
from pathlib import Path

from app.database import SessionLocal
from app.services.csv_ingestion import ingest_csv_data


def _default_data_dir() -> Path:
    return Path(__file__).resolve().parents[2] / "data"


def main() -> None:
    parser = argparse.ArgumentParser(description="CSV ingestion into database")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=_default_data_dir(),
        help="Directory with CSV files (default: backend/data)",
    )
    parser.add_argument(
        "--truncate",
        action="store_true",
        help="Clean tables before loading",
    )
    args = parser.parse_args()

    session = SessionLocal()
    try:
        summary = ingest_csv_data(
            db=session,
            data_dir=args.data_dir,
            truncate_before_load=args.truncate,
        )
    finally:
        session.close()

    print("Load completed successfully.")
    for table_name, row_count in summary.items():
        print(f"- {table_name}: {row_count} processed rows")


if __name__ == "__main__":
    main()
