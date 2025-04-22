from dotenv import load_dotenv
import os

load_dotenv()  # .env Datei laden

IG_USERNAME = os.getenv("IG_USERNAME")
IG_PASSWORD = os.getenv("IG_PASSWORD")
SCROLL_MIN_PAUSE = float(os.getenv("SCROLL_MIN_PAUSE", 1.5))
SCROLL_MAX_PAUSE = float(os.getenv("SCROLL_MAX_PAUSE", 3.0))

print(f"⚙️ IG_USERNAME geladen: {IG_USERNAME}")
