from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.binary_location = "/usr/bin/google-chrome"

driver = webdriver.Chrome(options=options)

url = "https://www.investing.com/economic-calendar/"
driver.get(url)

time.sleep(5)
try :
    accept_button = driver.find_element(By.XPATH, "//button[contains(text(),'Accept')]")
    accept_button.click()
    time.sleep(2)
except:
    print("Pas de pop-up de cookies.")

events = driver.find_elements(By.CLASS_NAME, "js-event-item")

data = [ ]
for event in events:
    try:
        time_ = event.find_element(By.CLASS_NAME, "time").text
        currency = event.find_element(By.CLASS_NAME, "left.flagCur.noWrap").text
        event_name = event.find_element(By.CLASS_NAME, "event").text
        actual = event.find_element(By.CLASS_NAME, "act").text
        forecast = event.find_element(By.CLASS_NAME, "fore").text
        previous = event.find_element(By.CLASS_NAME, "prev").text
        data.append([time_, currency, event_name, actual, forecast, previous])
    except:
        continue

df = pd.DataFrame(data, columns=["Heure", "Devise", "Événement", "Actuel", "Prévision", "Précédent"])
df.to_csv("calendrier_economique.csv", index=False, encoding="utf-8") 
print("Données enregistrées avec succès !")

driver.quit()

df = pd.read_csv('calendrier_economique.csv')
print(df)



