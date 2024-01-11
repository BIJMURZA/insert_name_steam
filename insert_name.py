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

print("_______________Steam_______________")
print("Название игры:", title)
print("Описание игры:", description)
print("Разработчик:", developer)
print("Издатель:", publisher)
print("                                   ")

app_name = "need-for-speed-unbound"
url = "https://steampay.com/game/" + app_name
response = requests.get(url)
soup = BeautifulSoup(response.content, "lxml").find("div", class_="product__current-price").text.split()[0]
if soup != "СКОРО":
    print("Цена Steampay: ", soup)
else:
    print("Цена Steampay: Нет в наличии")


app_name = "need-for-speed-unbound"
url = "https://steambuy.com/steam/" + app_name
response = requests.get(url)
soup = BeautifulSoup(response.content, "lxml")
if soup.find("div", class_="product-price__action").text.strip() != "Нет в наличии":
    print("Цена Steambuy: ", soup.find("div", class_="product-price__cost").text.split()[0])
else:
    print("Цена Steambuy: Нет в наличии")

app_name = "elden-ring"
url = "https://zaka-zaka.com/game/" + app_name
response = requests.get(url)
soup = BeautifulSoup(response.content, "lxml")
if soup.find("div", class_="price"):
    print("Zaka-Zaka: ", soup.find("div", class_="price"))
else:
    print("Zaka-Zaka: Нет в наличии")
