import psycopg2
import requests
from bs4 import BeautifulSoup


def take_price_steam(aid_game):
    url = f"https://store.steampowered.com/app/{aid_game}/"
    response = requests.get(url, headers={'Accept-Language': 'ru-Ru'})
    soup = BeautifulSoup(response.content, "lxml")
    if soup.find("div", class_="game_area_purchase_game_wrapper") is not None:
        if soup.find_all("div", class_="game_area_purchase_game_wrapper")[0].find("div", class_="discount_final_price") is not None:
            return soup.find_all("div", class_="game_area_purchase_game_wrapper")[0].find("div", class_="discount_final_price").text.split()[0] + "₽"
        elif soup.find_all("div", class_="game_area_purchase_game_wrapper")[0].find("div", class_="game_purchase_price price") is not None:
            return soup.find_all("div", class_="game_area_purchase_game_wrapper")[0].find("div", class_="game_purchase_price price").text.split()[0] + "₽"
    else:
        return "Нет в наличии "


if __name__ == "__main__":
    con = psycopg2.connect(dbname='rusync', user='admin',
                           password='1945', host='localhost')
    cursor = con.cursor()
    cursor.execute('SELECT aid FROM steam')

    aids = []
    for row in cursor.fetchall():
        aids.append(row[0])

    for aid in aids:
        take_price_steam(aid)