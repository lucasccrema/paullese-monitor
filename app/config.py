import os
from dotenv import load_dotenv

load_dotenv()

def env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()

DATABASE_URL = env("DATABASE_URL")
TRAFFIC_PROVIDER = env("TRAFFIC_PROVIDER", "disabled").lower()
ADMIN_TOKEN = env("ADMIN_TOKEN")
TELEGRAM_BOT_TOKEN = env("TELEGRAM_BOT_TOKEN")
TELEGRAM_ADMIN_CHAT_IDS = [x.strip() for x in env("TELEGRAM_ADMIN_CHAT_IDS").split(",") if x.strip()]
WATCH_THRESHOLD_PCT = float(env("WATCH_THRESHOLD_PCT", "20"))
ALERT_THRESHOLD_PCT = float(env("ALERT_THRESHOLD_PCT", "40"))
ALERT_PERSISTENCE_SAMPLES = int(env("ALERT_PERSISTENCE_SAMPLES", "2"))
