from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse, Response
from .config import ADMIN_TOKEN
from .db import connect, initialize

app = FastAPI(title="Paullese Monitor", docs_url=None, redoc_url=None)

def require_admin(authorization: str | None):
    if not ADMIN_TOKEN or authorization != f"Bearer {ADMIN_TOKEN}":
        raise HTTPException(status_code=401, detail="Autenticazione richiesta")

@app.get("/health")
def health():
    return {"status": "ok", "provider": "not exposed"}

@app.get("/admin/status")
def status(authorization: str | None = Header(default=None)):
    require_admin(authorization)
    initialize()
    with connect() as conn:
        runs = conn.execute(
            "SELECT started_at, finished_at, status, detail FROM collection_runs ORDER BY id DESC LIMIT 30"
        ).fetchall()
        alerts = conn.execute(
            "SELECT created_at, segment_id, severity, message, active FROM alert_events ORDER BY id DESC LIMIT 50"
        ).fetchall()
        sends = conn.execute(
            "SELECT created_at, channel, recipient, status, detail FROM notification_log ORDER BY id DESC LIMIT 50"
        ).fetchall()
    return {"recent_runs": runs, "recent_alerts": alerts, "recent_notifications": sends}

@app.get("/admin", response_class=HTMLResponse)
def dashboard():
    return HTMLResponse("""<!doctype html><html lang="it"><meta charset="utf-8">
<title>Paullese Monitor - controllo</title><body style="font:16px system-ui;max-width:1100px;margin:40px auto">
<h1>Paullese Monitor</h1><p>Tabella privata di controllo. Inserire il token amministrativo.</p>
<input id="token" type="password" placeholder="ADMIN_TOKEN" style="width:28em">
<button onclick="loadData()">Carica</button><pre id="out">In attesa di autenticazione</pre>
<script>
async function loadData(){
 const token=document.getElementById('token').value;
 const r=await fetch('/admin/status',{headers:{Authorization:'Bearer '+token}});
 document.getElementById('out').textContent=r.ok?JSON.stringify(await r.json(),null,2):'Errore '+r.status;
}
</script></body></html>""")

@app.get("/feed.xml")
def feed():
    # RSS corrente: nessuno storico. Sarà popolato con allarmi attivi reali.
    if not ADMIN_TOKEN:
        raise HTTPException(status_code=503, detail="Servizio non configurato")
    return Response(
        '<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel>'
        '<title>Paullese Monitor</title><description>Allarmi correnti SS415</description>'
        '</channel></rss>', media_type="application/rss+xml"
    )
