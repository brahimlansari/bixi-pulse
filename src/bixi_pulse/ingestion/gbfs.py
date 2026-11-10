from datetime import datetime, timezone
from typing import Any

import time

import requests

GBFS_URL = "https://gbfs.velobixi.com/gbfs/gbfs.json"
REQUEST_TIMEOUT_SECONDS = 10  # seconds
MAX_ATTEMPTS = 3
RETRY_BACKOFF_SECONDS = 5

def _get_json(url: str) -> dict[str, Any]:
    """Télécharge un JSON, avec plusieurs tentatives en cas d'erreur réseau."""
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = requests.get(url, timeout=REQUEST_TIMEOUT_SECONDS)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            if attempt == MAX_ATTEMPTS:
                raise
            wait = RETRY_BACKOFF_SECONDS * attempt
            print(f"Tentative {attempt}/{MAX_ATTEMPTS} échouée ({error}). Nouvel essai dans {wait} s...")
            time.sleep(wait)
    raise RuntimeError("Inaccessible")

def get_feed_urls(lang: str = "fr") -> dict[str, Any]:
    
    discovery = _get_json(GBFS_URL)
    languages = discovery["data"]
    if lang not in languages:
        raise ValueError(f"Language '{lang}' indisponible. Choix : {list(languages)}")
    return {feed["name"]: feed["url"] for feed in languages[lang]["feeds"]}

def fetch_feed(feed_name: str, lang: str = "fr") -> dict[str, Any]:
    """Fetch a specific feed by name."""
    feed_urls = get_feed_urls(lang)
    if feed_name not in feed_urls:
        raise ValueError(f"Flux '{feed_name}' introuvable. Choix : {list(feed_urls)}")
    return _get_json(feed_urls[feed_name])


def to_rows(feed_json: dict[str, Any]) -> list[dict[str, Any]]:
    """Convert feed JSON data to a list of rows."""
    source_last_updated = datetime.fromtimestamp(feed_json["last_updated"], tz=timezone.utc)
    ingested_at = datetime.now(tz=timezone.utc)
    return [
        {    
             **station,
            "source_last_updated": source_last_updated,
            "ingested_at": ingested_at,
        } for station in feed_json["data"]["stations"]
    ]
    
    
if __name__ == "__main__":
    status = fetch_feed("station_status")
    rows = to_rows(status)
    print(f"{len(rows)} stations récupérées.")
    print(rows[0])  # Affiche la première station pour vérification