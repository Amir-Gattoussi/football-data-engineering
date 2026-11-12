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
            }
        )
    return records
