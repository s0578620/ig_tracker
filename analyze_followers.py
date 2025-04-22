import json
import os


def load_followers(path):
    """Lädt eine Follower-Liste aus einer JSON-Datei."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return set(user["username"] for user in data)


def compare_followers(user, date1, date2):
    """Vergleicht zwei Follower-Datenstände."""
    base_path = os.path.join("data", user)
    file1 = os.path.join(base_path, date1, f"{date1}_followers.json")
    file2 = os.path.join(base_path, date2, f"{date2}_followers.json")

    if not (os.path.exists(file1) and os.path.exists(file2)):
        print("❌ Fehler: Eine oder beide Dateien existieren nicht!")
        return

    followers_old = load_followers(file1)
    followers_new = load_followers(file2)

    unfollowed = followers_old - followers_new
    new_followers = followers_new - followers_old

    print(f"\n📊 Vergleich für @{user}: {date1} ➔ {date2}")
    print(f"👋 Entfolgt: {len(unfollowed)} Nutzer")
    print(f"🎉 Neue Follower: {len(new_followers)} Nutzer")

    save_report(user, date1, date2, unfollowed, new_followers)


def save_report(user, date1, date2, unfollowed, new_followers):
    """Speichert einen Vergleichsreport."""
    os.makedirs("reports", exist_ok=True)
    filename = f"reports/{user}_{date1}_vs_{date2}_report.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"📊 Vergleich für @{user}\n")
        f.write(f"Von {date1} ➔ {date2}\n\n")

        f.write("👋 Entfolgt:\n")
        for u in sorted(unfollowed):
            f.write(f"- {u}\n")
        if not unfollowed:
            f.write("- Keine Entfolger!\n")

        f.write("\n🎉 Neue Follower:\n")
        for u in sorted(new_followers):
            f.write(f"+ {u}\n")
        if not new_followers:
            f.write("+ Keine neuen Follower!\n")

    print(f"✅ Report gespeichert: {filename}")


if __name__ == "__main__":
    # Beispiel Aufruf
    user = input("👤 Benutzername eingeben: ")
    date1 = input("📅 Altes Datum (YYYYMMDD): ")
    date2 = input("📅 Neues Datum (YYYYMMDD): ")

    compare_followers(user, date1, date2)
