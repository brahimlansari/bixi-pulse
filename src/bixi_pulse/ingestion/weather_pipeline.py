"""Charge la météo horaire historique de Montréal dans la couche bronze."""
from datetime import date

from bixi_pulse.ingestion.lake_writer import write_rows
from bixi_pulse.ingestion.weather import fetch_hourly_weather, to_rows

START_DATE = date(2024, 1, 1)
END_DATE = date(2025, 1, 1)


def main() -> None:
    rows = to_rows(fetch_hourly_weather(START_DATE, END_DATE))
    path = write_rows(rows, "weather_hourly")
    print(f"{len(rows)} heures de météo écrites dans bronze/{path}")


if __name__ == "__main__":
    main()