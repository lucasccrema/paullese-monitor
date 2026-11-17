# Paullese Monitor

Prima base del monitoraggio comunitario della SS415, direzione serale San Donato → Crema.

## Cosa contiene
- 15 punti GPS e 14 segmenti consecutivi.
- Modello di configurazione dei pendolari: orario per giorno, smart working e intervallo ferie.
- Motore iniziale di confronto con baseline, con soglie configurabili.
- Registro tecnico di rilevazioni, anomalie e invii.
- Endpoint protetti per dashboard e feed RSS corrente.
- Workflow GitHub Actions ogni 5 minuti.
- Test automatici.

## Cosa NON è ancora attivo
Non è collegato alcun fornitore di traffico. `TRAFFIC_PROVIDER=disabled` è intenzionale: prima bisogna verificare licenza, conservazione privata e pubblicazione dei valori correnti. Senza provider non vengono inventati tempi o allarmi.
La persistenza online richiede un PostgreSQL esterno. Non usare SQLite su GitHub Actions come archivio: il filesystem del runner è effimero.

## Avvio e test
Python 3.11+.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python -m unittest discover -s tests -v
```

## Segreti e variabili
Copiare `.env.example` in `.env` per lo sviluppo locale. Non committare mai `.env`.

- `DATABASE_URL`: URL PostgreSQL.
- `TRAFFIC_PROVIDER`: lasciare `disabled` fino alla scelta del provider.
- `ADMIN_TOKEN`: token lungo e casuale per gli endpoint amministrativi.
- `TELEGRAM_BOT_TOKEN`: token bot.
- `TELEGRAM_ADMIN_CHAT_IDS`: chat ID amministrative, separati da virgola.

Per GitHub Actions, impostare i valori come Repository Secrets. Il workflow fallisce in modo esplicito se mancano configurazioni essenziali.

## Endpoint
Con `uvicorn app.web:app --host 0.0.0.0 --port 8000`:
- `GET /health` stato applicativo senza dati sensibili.
- `GET /admin/status` registro operativo, richiede `Authorization: Bearer <ADMIN_TOKEN>`.
- `GET /admin/commuters` riepilogo profili (non espone token).
- `GET /feed.xml` feed RSS pubblico con soli allarmi correnti; vuoto finché non esistono dati reali.

La dashboard tabellare è in `/admin` e richiede autenticazione Bearer via header; per uso ordinario va collocata dietro un reverse proxy con autenticazione o un identity-aware proxy. Non pubblicarla su GitHub Pages.

## Calendario pendolari
Il modello supporta orario abituale distinto per giorno della settimana, giorni non lavorati e intervallo ferie. Non sono previsti override occasionali per singolo giorno.

## Attenzione alla pianificazione
GitHub Actions `schedule` ogni 5 minuti è soggetto a ritardi e non garantisce puntualità assoluta. Il feed RSS può essere aggiornato dai lettori con frequenze diverse; Telegram è il canale più adatto agli avvisi tempestivi.
