"""Charge la météo horaire de Montréal dans la couche bronze, pour une période donnée."""
import argparse
from datetime import date
from typing import Any

from bixi_pulse.ingestion.lake_writer import write_rows
from bixi_pulse.ingestion.weather import fetch_hourly_weather, to_rows


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Lit les dates de début et de fin passées sur la ligne de commande."""
    parser = argparse.ArgumentParser(description="Charge la météo horaire dans bronze.")
    parser.add_argument("--start", type=date.fromisoformat, required=True, help="Date de début (AAAA-MM-JJ)")
    parser.add_argument("--end", type=date.fromisoformat, required=True, help="Date de fin incluse (AAAA-MM-JJ)")
    return parser.parse_args(argv)


def keep_past_hours(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Retire les heures situées dans le futur (des prévisions, pas des observations)."""
    return [row for row in rows if row["observed_at"] <= row["ingested_at"]]


def main() -> None:
    args = parse_args()
    rows = keep_past_hours(to_rows(fetch_hourly_weather(args.start, args.end)))
    path = write_rows(rows, "weather_hourly")
    print(f"{len(rows)} heures de météo écrites dans bronze/{path}")


if __name__ == "__main__":
    main()