import json
import os
from datetime import datetime

def update_growth(username):
    """Aktualisiert oder erstellt growth.json mit aktuellem Follower- und Following-Count."""
    date_stamp = datetime.now().strftime("%Y%m%d")
    user_folder = os.path.join("data", username)
    growth_file = os.path.join(user_folder, "growth.json")

    # Daten laden
    today_folder = os.path.join(user_folder, date_stamp)
    followers_file = os.path.join(today_folder, f"{date_stamp}_followers.json")
    followings_file = os.path.join(today_folder, f"{date_stamp}_followings.json")

    if not os.path.exists(followers_file) or not os.path.exists(followings_file):
        print("⚠️ Followers oder Followings Dateien fehlen, Growth-Update übersprungen.")
        return

    with open(followers_file, "r", encoding="utf-8") as f:
        followers = json.load(f)

    with open(followings_file, "r", encoding="utf-8") as f:
        followings = json.load(f)

    follower_count = len(followers)
    following_count = len(followings)

    # Growth-Daten laden oder neu erstellen
    if os.path.exists(growth_file):
        with open(growth_file, "r", encoding="utf-8") as f:
            growth_data = json.load(f)
    else:
        growth_data = []

    # Neuen Eintrag anhängen
    growth_data.append({
        "date": date_stamp,
        "followers": follower_count,
        "followings": following_count
    })

    # Speichern
    os.makedirs(user_folder, exist_ok=True)
    with open(growth_file, "w", encoding="utf-8") as f:
        json.dump(growth_data, f, indent=2, ensure_ascii=False)

    print(f"📈 Growth updated: {follower_count} followers, {following_count} followings on {date_stamp}")
