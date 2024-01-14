import psycopg2
import requests
from bs4 import BeautifulSoup


def take_price_steam(cursor):
    update = f"UPDATE {marketplace} SET price = %s WHERE aid = %s"
    cursor.execute('SELECT * FROM steam')
    aid = []
    for row in cursor.fetchall():
        aid.append(row[0])
    for aid_game in aid:
        url = f"https://store.steampowered.com/app/{aid_game}/"
        response = requests.get(url, headers={'Accept-Language': 'ru-Ru'})
        soup = BeautifulSoup(response.content, "lxml")
        if soup.find("div", class_="game_area_purchase_game_wrapper") is not None:
            if soup.find_all("div", class_="game_area_purchase_game_wrapper")[0].find("div", class_="discount_final_price") is not None:
                price = soup.find_all("div", class_="game_area_purchase_game_wrapper")[0].find("div", class_="discount_final_price").text.split()[0]
                cursor.execute(update, (price, aid_game))
            elif soup.find_all("div", class_="game_area_purchase_game_wrapper")[0].find("div", class_="game_purchase_price price") is not None:
                price = soup.find_all("div", class_="game_area_purchase_game_wrapper")[0].find("div", class_="game_purchase_price price").text.split()[0]
                cursor.execute(update, (price, aid_game))
        else:
            price = "Нет в наличии"
            cursor.execute(update, (price, aid_game))


if __name__ == "__main__":
    con = psycopg2.connect(dbname='rusync', user='admin',
                           password='1945', host='localhost')
    cursor = con.cursor()

    marketplaces = ['STEAM', 'STEAMPAY', 'GAMERZ', 'ZAKA_ZAKA', 'GABESTORE', 'STEAMBUY']

    for marketplace in marketplaces:
        match marketplace:
            case 'STEAM':
                take_price_steam(cursor)
                con.commit()
            case 'STEAMPAY':
                print("STEAMPAY")

    cursor.close()
    con.close()