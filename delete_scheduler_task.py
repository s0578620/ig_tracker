import subprocess

def delete_task():
    task_name = "Instagram_Tracker_Bot"

    command = f'schtasks /Delete /TN "{task_name}" /F'

    print("⚙️ Lösche geplante Aufgabe...")
    print(f"📜 Befehl: {command}")

    try:
        subprocess.run(command, check=True, shell=True)
        print(f"✅ Aufgabe '{task_name}' erfolgreich gelöscht!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Fehler beim Löschen der Aufgabe: {e}")

if __name__ == "__main__":
    delete_task()
