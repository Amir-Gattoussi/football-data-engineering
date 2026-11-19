from pathlib import Path

from fdf.statsbomb import load_events

FIXTURE = Path(__file__).parent / "fixtures" / "events_sample.json"


def test_returns_one_record_per_event():
    assert len(load_events(FIXTURE)) == 5


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


def test_pass_end_location_is_extracted():
    record = load_events(FIXTURE)[3]
    assert record["end_x"] == 75.0
    assert record["end_y"] == 30.0


def test_shot_xg_is_extracted():
    assert load_events(FIXTURE)[4]["xg"] == 0.12


def test_events_without_pass_or_shot_data_have_none():
    record = load_events(FIXTURE)[2]
    assert record["end_x"] is None
    assert record["xg"] is None
