"""One-shot diagnostic: fetch and print current Google Routes leg times.

No database connection, file logging, or historical storage is performed.
Run from the repository root with: python -m app.google_routes_test
"""
from __future__ import annotations

import json
from datetime import datetime, timezone

from .provider import GoogleRoutesError, fetch_segment_durations


def main() -> int:
    try:
        rows = fetch_segment_durations()
    except GoogleRoutesError as exc:
        print(f"ERRORE: {exc}")
        return 1

    print("Paullese Monitor - rilevazione Google Routes")
    print("Istante richiesta (UTC):", datetime.now(timezone.utc).isoformat())
    print("Risultati transitori: non vengono salvati.")
    print()
    print(json.dumps(rows, ensure_ascii=False, indent=2))
    print()
    print("Totale traffico:", sum(x["duration_seconds"] for x in rows), "secondi")
    print("Totale statico:", sum(x["static_duration_seconds"] for x in rows), "secondi")
    print("Ritardo rispetto al tempo statico:",
          sum(x["traffic_delay_seconds"] for x in rows), "secondi")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
