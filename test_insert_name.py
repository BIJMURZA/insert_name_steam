import psycopg2
import requests
from bs4 import BeautifulSoup

con = psycopg2.connect(dbname='rusync', user='admin',
                       password='1945', host='localhost')
cursor = con.cursor()
cursor.execute('SELECT * FROM games')
aid = []
for row in cursor.fetchall():
    aid.append(row[0])
for i in range (len(aid)):
    print(aid[i])


app_id = "2138330"
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

app_name = "cyberpunk-2077-phantom-liberty"
url = "https://steampay.com/game/" + app_name
response = requests.get(url)
soup = BeautifulSoup(response.content, "lxml")
if soup.find("div", class_="product__current-price"):
    print("Steampay: ", soup.find("div", class_="product__current-price").text.split()[0])
else:
    print("Steampay: Нет в наличии")


app_name = "need-for-speed-unbound"
url = "https://steambuy.com/steam/" + app_name
response = requests.get(url)
soup = BeautifulSoup(response.content, "lxml")
if soup.find("div", class_="product-price__action").text.strip() != "Нет в наличии":
    print("Steambuy: ", soup.find("div", class_="product-price__cost").text.split()[0])
else:
    print("Steambuy: Нет в наличии")

app_name = "Rage"
url = "https://zaka-zaka.com/game/" + app_name
response = requests.get(url)
soup = BeautifulSoup(response.content, "lxml")
if soup.find("div", class_="price"):
    print("Zaka-Zaka: ", soup.find("div", class_="price"))
else:
    print("Zaka-Zaka: Нет в наличии")

app_name = "rage"
url = "https://gabestore.ru/game/" + app_name
response = requests.get(url)
soup = BeautifulSoup(response.content, "lxml")
if soup.find("div", class_="b-card__price-currentprice"):
    print("Gabestore: ", soup.find("div", class_="b-card__price-currentprice").text.split()[0])
else:
    print("Gabestore: Нет в наличии")

app_name = "steam/a-plague-tale-innocence"
url = "https://game-mag.ru/shop/" + app_name
response = requests.get(url)
soup = BeautifulSoup(response.content, "lxml")
if soup.find("p", class_="price"):
    print("Game-mag: ", soup.find("p", class_="price").text.split()[0])
else:
    print("Game-mag: Нет в наличии")

app_name = "the_callisto_protocol"
url = "https://gamerz.online/product/" + app_name
response = requests.get(url)
soup = BeautifulSoup(response.content, "lxml")
if soup.find("p", class_="price"):
    print("GamerZ: ", soup.find("p", class_="price").text.split()[0])
else:
    print("GamerZ: Нет в наличии")
