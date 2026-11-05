"""Client pour l'API historique d'Open-Meteo (météo horaire de Montréal)."""
from datetime import date, datetime, timezone
from typing import Any

import requests

ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"
MONTREAL_LATITUDE = 45.5017
MONTREAL_LONGITUDE = -73.5673
HOURLY_VARIABLES = [
    "temperature_2m",
    "precipitation",
    "wind_speed_10m",
    "relative_humidity_2m",
]
REQUEST_TIMEOUT_SECONDS = 30


def fetch_hourly_weather(start: date, end: date) -> dict[str, Any]:
    """Télécharge la météo horaire de Montréal entre deux dates (incluses)."""
    params = {
        "latitude": MONTREAL_LATITUDE,
        "longitude": MONTREAL_LONGITUDE,
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "hourly": ",".join(HOURLY_VARIABLES),
        "timezone": "UTC",
    }
    response = requests.get(ARCHIVE_URL, params=params, timeout=REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()
    return response.json()


def to_rows(weather_json: dict[str, Any]) -> list[dict[str, Any]]:
    """Transforme la réponse (format colonnes) en une liste de lignes (une par heure)."""
    hourly = weather_json["hourly"]
    ingested_at = datetime.now(timezone.utc)
    rows = []
    for i, time_str in enumerate(hourly["time"]):
        row: dict[str, Any] = {
            "observed_at": datetime.fromisoformat(time_str).replace(tzinfo=timezone.utc)
        }
        for variable in HOURLY_VARIABLES:
            row[variable] = hourly[variable][i]
        row["ingested_at"] = ingested_at
        rows.append(row)
    return rows


if __name__ == "__main__":
    data = fetch_hourly_weather(date(2024, 7, 1), date(2024, 7, 1))
    rows = to_rows(data)
    print(f"{len(rows)} heures récupérées")
    print(rows[0])