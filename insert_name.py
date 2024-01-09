import psycopg2
import requests
from bs4 import BeautifulSoup

app_id = "730"
url = "https://store.steampowered.com/app/" + app_id + "'"

response = requests.get(url, headers={'Accept-Language': 'ru-Ru'})
soup = BeautifulSoup(response.content, "lxml")
title = soup.find("div", class_="apphub_AppName").text
description = soup.find("div", class_="game_description_snippet").text.strip()
developer = soup.find("div", id="developers_list").text.strip()
publisher = soup.find_all("div", class_="dev_row")[1].find("div", class_="summary").text.strip()

print(url)
print("Название игры:", title)
print("Описание игры:", description)
print("Разработчик:", developer)
print("Издатель:", publisher)