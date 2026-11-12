from pathlib import Path

from fdf.statsbomb import load_events

FIXTURE = Path(__file__).parent / "fixtures" / "events_sample.json"


def test_returns_one_record_per_event():
    assert len(load_events(FIXTURE)) == 3


def test_flattens_nested_fields():
    first = load_events(FIXTURE)[0]
    assert first["type"] == "Pass"
    assert first["team"] == "Russia"


def test_missing_location_becomes_none():
    records = load_events(FIXTURE)
    assert records[2]["x"] is None
    assert records[2]["y"] is None


def test_missing_player_becomes_none():
    records = load_events(FIXTURE)
    assert records[1]["player"] is None
