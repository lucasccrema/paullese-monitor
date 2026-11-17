import json
from pathlib import Path

CONFIG = Path(__file__).resolve().parent.parent / "config" / "segments.json"

def load_segments():
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    points = {p["id"]: p for p in data["points"]}
    result = []
    for segment in data["segments"]:
        a, b = points[segment["from_point"]], points[segment["to_point"]]
        result.append({
            "id": segment["id"],
            "name": f'{a["name"]} – {b["name"]}',
            "from": a,
            "to": b,
        })
    return result
