# main.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from config import IG_USERNAME, IG_PASSWORD
from inject_script import inject_and_fetch

import time
import os

def setup_driver():
    """Setzt den ChromeDriver auf."""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", True)  # Browser bleibt nach Script offen
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def click_not_now_button(driver):
    """Sucht und klickt auf 'Jetzt nicht'-Button."""
    print("🔍 Suche nach 'Jetzt nicht' auf der Seite...")
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[text()='Jetzt nicht']"))
        )
        not_now_element = driver.find_element(By.XPATH, "//*[text()='Jetzt nicht']")
        not_now_element.click()
        print("✅ 'Jetzt nicht' erfolgreich geklickt!")
        time.sleep(2)
    except Exception as e:
        print(f"⚠️ Fehler beim Finden/Klicken auf 'Jetzt nicht': {e}")

def login_instagram(driver):
    driver.get("https://www.instagram.com/")
    time.sleep(3)

    try:
        accept_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Alle Cookies erlauben')]"))
        )
        accept_button.click()
        print("✅ Cookies akzeptiert.")
        time.sleep(2)
    except Exception:
        print("ℹ️ Kein Cookie-Banner gefunden oder bereits akzeptiert.")

    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")

    username_input.send_keys(IG_USERNAME)
    password_input.send_keys(IG_PASSWORD)
    password_input.send_keys(Keys.RETURN)

    print("🔐 Login abgeschickt...")
    time.sleep(5)

    click_not_now_button(driver)

    # 🚀 Danach direkt Profil aufrufen
    driver.get(f"https://www.instagram.com/{IG_USERNAME}/")
    print(f"🚀 Profilseite aufgerufen: {IG_USERNAME}")
    time.sleep(3)


def main():
    print(f"⚙️ IG_USERNAME geladen: {IG_USERNAME}")
    driver = setup_driver()

    try:
        login_instagram(driver)
        inject_and_fetch(driver, IG_USERNAME)
        #inject_and_fetch(driver, "shanabazi")
    finally:
        print("🚀 Bot Ablauf abgeschlossen!")
        driver.quit()

if __name__ == "__main__":
    main()
