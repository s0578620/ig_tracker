# utils.py

import time
import random
from telnetlib import EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def random_sleep(min_sec=1.5, max_sec=3.0):
    """Menschlich wirkende Zufallspausen"""
    sleep_time = random.uniform(min_sec, max_sec)
    time.sleep(sleep_time)


def human_scroll(driver, element, total_expected=0, min_pause=1.5, max_pause=3.0):
    """Scrollt menschlich durch Instagram Listen und zeigt Fortschritt an"""
    last_height = driver.execute_script("return arguments[0].scrollHeight", element)
    scroll_attempts = 0
    usernames_count = 0
    fetched_usernames = set()

    while True:
        # Alle aktuell sichtbaren Usernamen extrahieren
        users = element.find_elements(By.TAG_NAME, "a")
        for user in users:
            username = user.text.strip()
            if username and username not in fetched_usernames:
                fetched_usernames.add(username)

        # Fortschritt anzeigen
        usernames_count = len(fetched_usernames)
        if total_expected > 0:
            percentage = (usernames_count / total_expected) * 100
            print(f"📈 {usernames_count}/{total_expected} Nutzer geladen ({percentage:.2f}%)", end="\r")
        else:
            print(f"📈 {usernames_count} Nutzer geladen...", end="\r")

        # Scrollen
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", element)
        random_sleep(min_pause, max_pause)

        new_height = driver.execute_script("return arguments[0].scrollHeight", element)
        if new_height == last_height:
            scroll_attempts += 1
            if scroll_attempts > 2:
                break
        else:
            scroll_attempts = 0
        last_height = new_height

    print("\n✅ Scrollen abgeschlossen.")
