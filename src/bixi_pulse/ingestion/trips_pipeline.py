"""Charge les trajets historiques BIXI dans la couche bronze du data lake."""
from pathlib import Path

from bixi_pulse.ingestion.lake_writer import upload_directory
from bixi_pulse.ingestion.trips import convert_csv_to_parquet

RAW_CSV = Path("data/raw/bixi_trips_2024.csv")
STAGING_DIR = Path("data/staging/bixi_trips")


def main() -> None:
    print("Conversion CSV → Parquet...")
    convert_csv_to_parquet(RAW_CSV, STAGING_DIR)
    print("Envoi vers Azure...")
    count = upload_directory(STAGING_DIR, "bixi_trips")
    print(f"{count} fichiers Parquet envoyés dans bronze/bixi_trips/")


if __name__ == "__main__":
    main()