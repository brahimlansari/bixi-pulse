"""Tests du module d'écriture dans le data lake."""
from datetime import datetime, timezone

from bixi_pulse.ingestion.lake_writer import build_path


def test_build_path_is_partitioned_by_ingestion_date():
    ingested_at = datetime(2026, 11, 16, 16, 5, 8, tzinfo=timezone.utc)

    path = build_path("station_status", ingested_at)

    assert path == "station_status/ingestion_date=2026-11-16/2026-11-16T16-05-08.parquet"


def test_build_path_has_no_colon_for_windows():
    ingested_at = datetime(2026, 11, 16, 16, 5, 8, tzinfo=timezone.utc)

    assert ":" not in build_path("station_status", ingested_at)