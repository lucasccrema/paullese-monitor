# Creato il: 2026-11-17 22:50
from .config import DATABASE_URL

SCHEMA = """
CREATE TABLE IF NOT EXISTS collection_runs (
 id BIGSERIAL PRIMARY KEY, started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
 finished_at TIMESTAMPTZ, status TEXT NOT NULL, detail TEXT
);
CREATE TABLE IF NOT EXISTS segment_observations (
 id BIGSERIAL PRIMARY KEY, observed_at TIMESTAMPTZ NOT NULL DEFAULT now(),
 segment_id INTEGER NOT NULL, duration_seconds INTEGER NOT NULL,
 baseline_seconds INTEGER, deviation_pct DOUBLE PRECISION
);
-- Colonne aggiunte in seguito: modifiche solo additive, le righe già presenti restano valide (valore NULL).
ALTER TABLE segment_observations ADD COLUMN IF NOT EXISTS static_duration_seconds INTEGER;
ALTER TABLE segment_observations ADD COLUMN IF NOT EXISTS request_started_at TIMESTAMPTZ;
ALTER TABLE segment_observations ADD COLUMN IF NOT EXISTS response_received_at TIMESTAMPTZ;
CREATE INDEX IF NOT EXISTS idx_observations_segment_time ON segment_observations(segment_id, observed_at DESC);
CREATE TABLE IF NOT EXISTS alert_events (
 id BIGSERIAL PRIMARY KEY, created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
 segment_id INTEGER NOT NULL, severity TEXT NOT NULL, message TEXT NOT NULL,
 active BOOLEAN NOT NULL DEFAULT TRUE
);
CREATE TABLE IF NOT EXISTS notification_log (
 id BIGSERIAL PRIMARY KEY, created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
 channel TEXT NOT NULL, recipient TEXT, alert_id BIGINT,
 status TEXT NOT NULL, detail TEXT
);
"""

def connect():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL non configurato: serve un PostgreSQL persistente.")
    import psycopg
    return psycopg.connect(DATABASE_URL)

def initialize():
    with connect() as conn:
        conn.execute(SCHEMA)
