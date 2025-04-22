#!/bin/bash

echo "============================="
echo " Instagram Pro Bot Setup"
echo "============================="

# Install dependencies
pip install -r requirements.txt

echo "-----------------------------------------"
echo "Bitte stelle sicher, dass deine .env Datei korrekt ausgefüllt ist!"
echo "-----------------------------------------"

# Start main program
python3 main.py
