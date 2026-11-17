from dataclasses import dataclass

@dataclass
class Evaluation:
    status: str
    deviation_pct: float | None
    message: str

def evaluate(current_seconds: int, baseline_seconds: int,
             watch_pct: float = 20, alert_pct: float = 40) -> Evaluation:
    if current_seconds <= 0 or baseline_seconds <= 0:
        return Evaluation("invalid", None, "Durata corrente o baseline non valida")
    deviation = (current_seconds / baseline_seconds - 1) * 100
    if deviation >= alert_pct:
        return Evaluation("alert", deviation, "Tempo superiore alla soglia di allarme")
    if deviation >= watch_pct:
        return Evaluation("watch", deviation, "Tempo superiore alla soglia di attenzione")
    return Evaluation("normal", deviation, "Nessuna anomalia secondo le soglie correnti")
