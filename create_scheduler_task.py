import os
import sys
import subprocess
import getpass

def create_task():
    username = getpass.getuser()
    project_path = os.path.abspath(os.path.dirname(__file__))
    python_path = os.path.join(project_path, ".venv", "Scripts", "python.exe")
    script_path = os.path.join(project_path, "main.py")

    task_name = "Instagram_Tracker_Bot"

    command = (
        f'schtasks /Create /TN "{task_name}" /TR "\\"{python_path}\\" \\"{script_path}\\"" '
        f'/SC DAILY /ST 06:00 /F /RL HIGHEST /RU {username}'
    )

    print("⚙️ Erstelle geplante Aufgabe...")
    print(f"📜 Befehl: {command}")

    try:
        subprocess.run(command, check=True, shell=True)
        print("✅ Aufgabe erfolgreich erstellt! Bot l\u00e4uft jetzt jeden Tag um 06:00 Uhr morgens.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Fehler beim Erstellen der Aufgabe: {e}")

if __name__ == "__main__":
    create_task()
