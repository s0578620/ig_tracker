@echo off
echo =============================
echo Instagram Pro Bot Setup
echo =============================

REM Installiere Abhängigkeiten
pip install -r requirements.txt

REM Hinweis für Benutzer
echo -----------------------------------------
echo Bitte stelle sicher, dass deine .env Datei korrekt ausgefüllt ist!
echo -----------------------------------------

REM Starte das Hauptprogramm
python main.py

pause
