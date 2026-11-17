from datetime import date, datetime
from typing import Optional

WEEKDAYS = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")

def is_commuting(profile: dict, at: datetime) -> bool:
    """True se il profilo prevede il viaggio in quel giorno e orario."""
    day = WEEKDAYS[at.weekday()]
    schedule = profile.get("weekly_schedule", {}).get(day)
    if not schedule or schedule.get("work_from_home"):
        return False
    start, end = profile.get("vacation_from"), profile.get("vacation_to")
    today = at.date()
    if start and end and date.fromisoformat(start) <= today <= date.fromisoformat(end):
        return False
    departure = schedule.get("departure")
    if not departure:
        return False
    # La fascia di preallarme è una finestra di 90 minuti prima della partenza.
    dep = datetime.combine(today, datetime.strptime(departure, "%H:%M").time(), tzinfo=at.tzinfo)
    delta = (dep - at).total_seconds() / 60
    return -15 <= delta <= 90
