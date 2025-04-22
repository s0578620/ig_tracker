import json
import os
from glob import glob
from datetime import datetime

DATA_DIR = "data"
REPORTS_DIR = "reports"

def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_usernames(user_list):
    return set(user['username'] for user in user_list)

def compare_snapshots(old_file, new_file):
    old_data = load_data(old_file)
    new_data = load_data(new_file)

    old_followers = extract_usernames(old_data['followers'])
    new_followers = extract_usernames(new_data['followers'])

    old_followings = extract_usernames(old_data['followings'])
    new_followings = extract_usernames(new_data['followings'])

    return {
        "new_followers": new_followers - old_followers,
        "lost_followers": old_followers - new_followers,
        "new_followings": new_followings - old_followings,
        "unfollowed": old_followings - new_followings
    }

def save_report(content, filename):
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)
    path = os.path.join(REPORTS_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Bericht gespeichert unter {path}")

def main():
    files = sorted(glob(os.path.join(DATA_DIR, "*.json")))
    if len(files) < 2:
        print("❗ Mindestens zwei Datensätze im /data/ Ordner erforderlich!")
        return

    old_file = files[-2]
    new_file = files[-1]

    print(f"Vergleiche {old_file} 🆚 {new_file}...\n")
    result = compare_snapshots(old_file, new_file)

    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_content = f"""
Instagram Vergleichsbericht - {now}

Neue Follower:
{', '.join(result["new_followers"]) if result["new_followers"] else 'Keine'}

Entfolgte Follower:
{', '.join(result["lost_followers"]) if result["lost_followers"] else 'Keine'}

Neu Gefolgt:
{', '.join(result["new_followings"]) if result["new_followings"] else 'Keine'}

Entfolgte Followings:
{', '.join(result["unfollowed"]) if result["unfollowed"] else 'Keine'}
"""

    save_report(report_content, f"report_{now}.txt")

if __name__ == "__main__":
    main()
