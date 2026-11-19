import json
from pathlib import Path
from typing import Any


def load_events(path: str | Path) -> list[dict[str, Any]]:
    """Read a StatsBomb events file and return one flat record per event."""
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)

    records = []
    for event in raw:
        location = event.get("location")
        end_location = event.get("pass", {}).get("end_location")
        xg = event.get("shot", {}).get("statsbomb_xg")
        records.append(
            {
                "event_id": event["id"],
                "index": event["index"],
                "period": event["period"],
                "minute": event["minute"],
                "second": event["second"],
                "timestamp": event["timestamp"],
                "type": event["type"]["name"],
                "team": event["team"]["name"],
                "player": event.get("player", {}).get("name"),
                "x": location[0] if location else None,
                "y": location[1] if location else None,
                "end_x": end_location[0] if end_location else None,
                "end_y": end_location[1] if end_location else None,
                "xg": xg,
            }
        )
    return records


def load_matches(path: str | Path) -> list[dict[str, Any]]:
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    records = []
    for match in raw:
        kick_off_time = match.get("kick_off")
        date = match.get("match_date")
        records.append(
            {
                "match_ID": match["match_id"],
                "date": date,
                "kick-off_time": kick_off_time,
                "home_team_name": match["home_team"]["home_team_name"],
                "away_team_name": match["away_team"]["away_team_name"],
                "home_score": match["home_score"],
                "away_score": match["away_score"],
            }
        )
    return records
