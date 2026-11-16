"""Tests du client GBFS (sans aucun appel réseau réel)."""
from datetime import timezone

import pytest
import requests

from bixi_pulse.ingestion import gbfs


class FakeResponse:
    """Imite une réponse de requests, avec un JSON fixé à l'avance."""

    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        pass

    def json(self):
        return self._payload


def test_to_rows_adds_utc_timestamps_to_each_station():
    feed = {
        "last_updated": 1763309108,
        "data": {"stations": [{"station_id": "1"}, {"station_id": "2"}]},
    }

    rows = gbfs.to_rows(feed)

    assert [row["station_id"] for row in rows] == ["1", "2"]
    assert rows[0]["source_last_updated"].tzinfo == timezone.utc
    assert rows[0]["ingested_at"] >= rows[0]["source_last_updated"]


def test_get_json_retries_then_succeeds(monkeypatch):
    calls = {"count": 0}

    def flaky_get(url, timeout):
        calls["count"] += 1
        if calls["count"] < 3:
            raise requests.ConnectionError("réseau coupé")
        return FakeResponse({"ok": True})

    monkeypatch.setattr(gbfs.requests, "get", flaky_get)
    monkeypatch.setattr(gbfs.time, "sleep", lambda seconds: None)

    assert gbfs._get_json("https://exemple.test") == {"ok": True}
    assert calls["count"] == 3


def test_get_json_gives_up_after_max_attempts(monkeypatch):
    def always_down(url, timeout):
        raise requests.ConnectionError("panne")

    monkeypatch.setattr(gbfs.requests, "get", always_down)
    monkeypatch.setattr(gbfs.time, "sleep", lambda seconds: None)

    with pytest.raises(requests.ConnectionError):
        gbfs._get_json("https://exemple.test")