from pathlib import Path

from fdf.statsbomb import load_matches

FIXTURE = Path(__file__).parent / "fixtures" / "match_sample.json"


def test_returns_one_record_per_match():
    assert len(load_matches(FIXTURE)) == 1


def test_team_names_are_plain_text():
    first = load_matches(FIXTURE)[0]
    assert first["home_team_name"] == "Russia"
    assert first["away_team_name"] == "Egypt"


def test_scores_match_the_fixture():
    first = load_matches(FIXTURE)[0]
    assert first["home_score"] == 3
    assert first["away_score"] == 1
