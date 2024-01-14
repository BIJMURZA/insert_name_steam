import psycopg2
import requests
from bs4 import BeautifulSoup


if __name__ == "__main__":
    con = psycopg2.connect(dbname='rusync', user='admin',
                           password='1945', host='localhost')
    cursor = con.cursor()

    cursor.execute('SELECT aid FROM steam')
    aid = []
    for row in cursor.fetchall():
        aid.append(row[0])

    marketplaces = ['STEAM', 'STEAMPAY', 'STEAMBUY', 'GAMERZ', 'ZAKA_ZAKA', 'GABESTORE', 'GAME_MAG']
    for marketplace in marketplaces:
        if marketplace == 'STEAM':
            for aids in aid:
                url = f"https://store.steampowered.com/app/{aids}/"
                response = requests.get(url, headers={'Accept-Language': 'ru-Ru'})
                soup = BeautifulSoup(response.content, "lxml")
                if soup.find("div", class_="game_area_purchase_game_wrapper") is not None:
                    if soup.find_all("div", class_="game_area_purchase_game_wrapper")[0].find("div", class_="discount_final_price") is not None:
                        print(url, soup.find_all("div", class_="game_area_purchase_game_wrapper")[0].find("div", class_="discount_final_price").text)
                    elif soup.find_all("div", class_="game_area_purchase_game_wrapper")[0].find("div", class_="game_purchase_price price") is not None:
                        print(url, soup.find_all("div", class_="game_area_purchase_game_wrapper")[0].find("div", class_="game_purchase_price price").text)
                else:
                    print("No game found")