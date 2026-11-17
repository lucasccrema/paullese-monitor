"""Google Routes API v2 provider for the evening Paullese route.

This module fetches live route information and returns it in memory.
It deliberately does not persist Google Maps Content or derive historical
statistics from it.
"""
from __future__ import annotations

import os
import re
from typing import Any

import httpx

GOOGLE_ROUTES_URL = "https://routes.googleapis.com/directions/v2:computeRoutes"

# Evening direction: San Donato Milanese -> Crema.
# 15 fixed points produce 14 route legs.
POINTS: list[tuple[str, float, float]] = [
    ("Parcheggio San Donato", 45.432540, 9.262713),
    ("Bugliano", 45.422099, 9.282389),
    ("Zeloforamagno", 45.427529, 9.315989),
    ("Pantigliate", 45.430090, 9.346976),
    ("Caleppio", 45.428594, 9.380019),
    ("Silos", 45.427226, 9.395182),
    ("Rondo TEEM Paullo", 45.418792, 9.426090),
    ("Semaforo Zelo BP", 45.416216, 9.431733),
    ("Confluenza Quartieri", 45.406700, 9.446636),
    ("Ingresso Spino", 45.402336, 9.469861),
    ("Uscita Dovera", 45.385844, 9.544930),
    ("Uscita Vaiano", 45.379430, 9.589031),
    ("Uscita Bagnolo", 45.364094, 9.631819),
    ("Mezzo Via Milano", 45.359472, 9.646279),
    ("Rondo Coop", 45.359988, 9.664386),
]


class GoogleRoutesError(RuntimeError):
    """Raised when Google Routes cannot provide a valid response."""


def _location(point: tuple[str, float, float]) -> dict[str, Any]:
    _, lat, lng = point
    return {"location": {"latLng": {"latitude": lat, "longitude": lng}}}


def _seconds(value: str, field: str) -> int:
    # Routes API durations are protobuf strings, e.g. "123s" or "123.4s".
    match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)s", value or "")
    if not match:
        raise GoogleRoutesError(f"Formato {field} non riconosciuto: {value!r}")
    return round(float(match.group(1)))


def fetch_segment_durations(api_key: str | None = None) -> list[dict[str, Any]]:
    """Fetch the 14 live leg durations; results remain in memory only."""
    key = api_key or os.getenv("GOOGLE_MAPS_API_KEY", "").strip()
    if not key:
        raise GoogleRoutesError(
            "GOOGLE_MAPS_API_KEY non configurata. Impostare la variabile d'ambiente."
        )

    body = {
        "origin": _location(POINTS[0]),
        "destination": _location(POINTS[-1]),
        "intermediates": [_location(p) for p in POINTS[1:-1]],
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE",
        "languageCode": "it-IT",
        "units": "METRIC",
    }
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": key,
        "X-Goog-FieldMask": (
            "routes.legs.duration,"
            "routes.legs.staticDuration,"
            "routes.legs.distanceMeters"
        ),
    }

    try:
        response = httpx.post(
            GOOGLE_ROUTES_URL,
            json=body,
            headers=headers,
            timeout=30.0,
        )
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        detail = exc.response.text[:1500]
        raise GoogleRoutesError(
            f"Google Routes ha risposto HTTP {exc.response.status_code}: {detail}"
        ) from exc
    except httpx.HTTPError as exc:
        raise GoogleRoutesError(f"Errore di rete verso Google Routes: {exc}") from exc

    try:
        payload = response.json()
        legs = payload["routes"][0]["legs"]
    except (ValueError, KeyError, IndexError, TypeError) as exc:
        raise GoogleRoutesError(
            f"Risposta Google Routes incompleta o inattesa: {response.text[:1500]}"
        ) from exc

    expected = len(POINTS) - 1
    if len(legs) != expected:
        raise GoogleRoutesError(
            f"Attesi {expected} segmenti, ricevuti {len(legs)}. "
            "Controllare waypoint e risposta API."
        )

    results = []
    for index, leg in enumerate(legs):
        start = POINTS[index][0]
        end = POINTS[index + 1][0]
        duration = _seconds(leg.get("duration", ""), "duration")
        static_duration = _seconds(leg.get("staticDuration", ""), "staticDuration")
        distance = int(leg.get("distanceMeters", 0))
        results.append({
            "segment_id": index + 1,
            "from": start,
            "to": end,
            "duration_seconds": duration,
            "static_duration_seconds": static_duration,
            "traffic_delay_seconds": duration - static_duration,
            "distance_meters": distance,
        })
    return results
