import json
import os

def find_last_two_dates(username):
    """Finde die letzten zwei Datumsordner für den Benutzer."""
    user_folder = os.path.join("data", username)
    if not os.path.exists(user_folder):
        return None, None

    dates = [d for d in os.listdir(user_folder) if os.path.isdir(os.path.join(user_folder, d)) and d.isdigit()]
    dates = sorted(dates)

    if len(dates) < 2:
        return None, None

    return dates[-2], dates[-1]

def load_followers(username, date_stamp):
    """Lädt follower.json für ein gegebenes Datum."""
    path = os.path.join("data", username, date_stamp, f"{date_stamp}_followers.json")
    if not os.path.exists(path):
        return []

    with open(path, "r", encoding="utf-8") as f:
        followers = json.load(f)

    return [user['username'] for user in followers]
def generate_report(username):
    """Vergleicht zwei Snapshots und erstellt einen Report."""
    date_old, date_new = find_last_two_dates(username)

    if not date_old or not date_new:
        print("⚠️ Nicht genug Daten für Report.")
        return

    followers_old = load_followers(username, date_old)
    followers_new = load_followers(username, date_new)

    unfollowers = list(set(followers_old) - set(followers_new))
    new_followers = list(set(followers_new) - set(followers_old))

    report = {
        "date_from": date_old,
        "date_to": date_new,
        "unfollowers": unfollowers,
        "new_followers": new_followers
    }

    # Speichern
    report_folder = os.path.join("data", username, date_new)
    os.makedirs(report_folder, exist_ok=True)
    report_path = os.path.join(report_folder, f"{date_new}_report.json")

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"📋 Report gespeichert: {report_path}")

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
