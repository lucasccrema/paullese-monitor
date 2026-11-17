# Creato il: 2026-11-17 22:50
from datetime import datetime, timezone
from .db import connect, initialize
from .provider import fetch_segment_durations, ProviderNotConfigured

def run():
    initialize()
    try:
        # Ora reale della richiesta a Google e ora di ricezione della risposta (UTC).
        request_started_at = datetime.now(timezone.utc)
        observations = fetch_segment_durations()
        response_received_at = datetime.now(timezone.utc)
        # Il provider restituisce, per ogni tratta, i campi: segment_id, duration_seconds,
        # static_duration_seconds (tempo senza traffico), traffic_delay_seconds, distance_meters.
        # baseline_seconds e deviation_pct non sono ancora calcolati e restano vuoti.
        with connect() as conn:
            for item in observations:
                conn.execute(
                    """INSERT INTO segment_observations
                    (segment_id, duration_seconds, baseline_seconds, deviation_pct,
                     static_duration_seconds, request_started_at, response_received_at)
                    VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                    (item["segment_id"], item["duration_seconds"], item.get("baseline_seconds"),
                     item.get("deviation_pct"), item.get("static_duration_seconds"),
                     request_started_at, response_received_at)
                )
            conn.execute(
                "INSERT INTO collection_runs(status, detail, finished_at) VALUES ('ok', %s, now())",
                (f"{len(observations)} segmenti acquisiti",)
            )
    except ProviderNotConfigured as exc:
        with connect() as conn:
            conn.execute(
                "INSERT INTO collection_runs(status, detail, finished_at) VALUES ('blocked', %s, now())",
                (str(exc),)
            )
        print(f"Raccolta non eseguita: {exc}")
    except Exception as exc:
        with connect() as conn:
            conn.execute(
                "INSERT INTO collection_runs(status, detail, finished_at) VALUES ('error', %s, now())",
                (repr(exc),)
            )
        raise

if __name__ == "__main__":
    run()
