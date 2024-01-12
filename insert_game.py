import psycopg2
import requests
from bs4 import BeautifulSoup


def insert_game(app):
    url = "https://store.steampowered.com/app/" + app + "'"
    response = requests.get(url, headers={'Accept-Language': 'ru-Ru'})
    soup = BeautifulSoup(response.content, "lxml")
    title = soup.find("div", class_="apphub_AppName").text
    description = soup.find("div", class_="game_description_snippet").text.strip()
    developer = soup.find("div", id="developers_list").text.strip()
    publisher = soup.find_all("div", class_="dev_row")[1].find("div", class_="summary").text.strip()



con = psycopg2.connect(dbname='rusync', user='admin',
                       password='1945', host='localhost')
cursor = con.cursor()
cursor.execute('SELECT * FROM games')
aid = []
for row in cursor.fetchall():
    aid.append(row[0])

for i in range(len(aid)):
    insert_game(str(aid[i]))

cursor.close()
con.close()
