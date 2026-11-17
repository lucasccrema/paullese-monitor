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

## Interrogazione database (Neon)
https://console.neon.tech/app/projects/rough-tree-38372121/branches/br-misty-glade-ba3cb75f/sql-editor?database=neondb#plan
SELECT segment_id, duration_seconds FROM segment_observations
WHERE observed_at = (SELECT max(observed_at) FROM segment_observations)
ORDER BY segment_id;

## prova e numerazione tratte
Numerazione. La tratta N va dal punto N al punto N+1 della lista, nella direzione San Donato → Crema. Tempi del 17 novembre alle 17:51 italiane, velocità minime dalla distanza in linea retta (la strada reale è più lunga):

Tratta	Da → A	Tempo	Velocità minima
1	Parcheggio San Donato → Bugliano	486 s	14 km/h
2	Bugliano → Zeloforamagno	145 s	67 km/h
3	Zeloforamagno → Pantigliate	116 s	75 km/h
4	Pantigliate → Caleppio	132 s	70 km/h
5	Caleppio → Silos	147 s	29 km/h
6	Silos → Rondò TEEM Paullo	606 s	15 km/h
7	Rondò TEEM Paullo → Semaforo Zelo BP	163 s	12 km/h
8	Semaforo Zelo BP → Confluenza Quartieri	164 s	35 km/h
9	Confluenza Quartieri → Ingresso Spino	167 s	40 km/h
10	Ingresso Spino → Uscita Dovera	247 s	90 km/h
11	Uscita Dovera → Uscita Vaiano	124 s	102 km/h
12	Uscita Vaiano → Uscita Bagnolo	140 s	96 km/h
13	Uscita Bagnolo → Mezzo Via Milano	118 s	38 km/h
14	Mezzo Via Milano → Rondò Coop	103 s	49 km/h

Le due tratte lente di questa sera sono la 1 e la 6, con circa 8-10 minuti ciascuna. Quelle che dici critiche per gli incidenti sono le tratte 10, 11 e 12, tra Spino e Bagnolo.
