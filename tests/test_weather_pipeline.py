from datetime import date, datetime, timezone

from bixi_pulse.ingestion.weather_pipeline import keep_past_hours, parse_args


def test_keep_past_hours_drops_future_hours():
    now = datetime(2026, 11, 18, 18, 30, tzinfo=timezone.utc)
    rows = [
        {"observed_at": datetime(2026, 11, 18, 18, 0, tzinfo=timezone.utc), "ingested_at": now},
        {"observed_at": datetime(2026, 11, 18, 19, 0, tzinfo=timezone.utc), "ingested_at": now},
    ]

    kept = keep_past_hours(rows)

    assert [row["observed_at"].hour for row in kept] == [18]


def test_parse_args_reads_dates():
    args = parse_args(["--start", "2026-11-01", "--end", "2026-11-18"])

    assert args.start == date(2026, 11, 1)
    assert args.end == date(2026, 11, 18)