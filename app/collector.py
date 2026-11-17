from datetime import datetime, timezone
from .db import connect, initialize
from .provider import fetch_segment_durations, ProviderNotConfigured

def run():
    initialize()
    started = datetime.now(timezone.utc)
    try:
        observations = fetch_segment_durations()
        # Il provider dovrà restituire record verificati:
        # [{"segment_id": 1, "duration_seconds": 420, "baseline_seconds": 300}, ...]
        with connect() as conn:
            for item in observations:
                conn.execute(
                    """INSERT INTO segment_observations
                    (segment_id, duration_seconds, baseline_seconds, deviation_pct)
                    VALUES (%s,%s,%s,%s)""",
                    (item["segment_id"], item["duration_seconds"], item.get("baseline_seconds"),
                     item.get("deviation_pct"))
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
