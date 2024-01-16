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


def take_price_steampay(cursor):
    update = f"UPDATE {marketplace} SET price = %s WHERE game_name = %s"
    cursor.execute('SELECT game_name FROM steampay')
    games = []
    for row in cursor.fetchall():
        games.append(row[0])

    for game in games:
        url = f"https://steampay.com/game/{game}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "lxml")
        if soup.find("div", class_="product__current-price"):
            price = soup.find("div", class_="product__current-price").text.split()[0]
            if price != "СКОРО":
                cursor.execute(update, (price, game))
            else:
                cursor.execute(update, ("Нет в наличии", game))
        elif game == "-":
            cursor.execute(update, ("-", game))
        else:
            cursor.execute(update, ("Нет в наличии", game))


def take_price_steambuy(cursor):
    update = f"UPDATE {marketplace} SET price = %s WHERE game_name = %s"
    cursor.execute('SELECT game_name FROM steambuy')
    games = []
    for row in cursor.fetchall():
        games.append(row[0])

    for game in games:
        url = f"https://steambuy.com/{game}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "lxml")
        if soup.find("div", class_="product-price__action").text.strip() != "Нет в наличии":
            price = soup.find("div", class_="product-price__cost").text.split()[0]
            cursor.execute(update, (price, game))
        elif game == "-":
            cursor.execute(update, ("-", game))
        else:
            cursor.execute(update, ("Нет в наличии", game))
         

def take_price_zaka_zaka(cursor):
    update = f"UPDATE {marketplace} SET price = %s WHERE game_name = %s"
    cursor.execute('SELECT game_name FROM zaka_zaka')
    games = []
    for row in cursor.fetchall():
        games.append(row[0])

    for game in games:
        url = f"https://zaka-zaka.com/game/{game}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "lxml")
        print(url)
        if soup.find("div", class_="price"):
            price = soup.find("div", class_="price").text.split()[0]
            cursor.execute(update, (price, game))
        elif game == "-":
            cursor.execute(update, ("-", game))
        else:
            cursor.execute(update, ("Нет в наличии", game))


def take_price_gabestore(cursor):
    update = f"UPDATE {marketplace} SET price = %s WHERE game_name = %s"
    cursor.execute('SELECT game_name FROM gabestore')

    games = []
    for row in cursor.fetchall():
        games.append(row[0])

    for game in games:
        url = f"https://gabestore.ru/game/{game}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "lxml")
        if soup.find("div", class_="b-card__price-currentprice"):
            price = soup.find("div", class_="b-card__price-currentprice").text.split()[0]
            cursor.execute(update, (price, game))
        elif game == "-":
            cursor.execute(update, ("-", game))
        else:
            cursor.execute(update, ("Нет в наличии", game))


def take_games_gamerz(cursor):
    update = f"UPDATE {marketplace} SET price = %s WHERE game_name = %s"
    cursor.execute('SELECT game_name FROM gamerz')

    games = []
    for row in cursor.fetchall():
        games.append(row[0])

    for game in games:
        url = f"https://gamerz.online/game/{game}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "lxml")
        if soup.find("p", class_="price"):
            price = soup.find("p", class_="price").text.split()[0]
            cursor.execute(update, (price, game))
        elif game == "-":
            cursor.execute(update, ("-", game))
        else:
            cursor.execute(update, ("Нет в наличии", game))


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
                take_price_steampay(cursor)
                con.commit()
            case 'STEAMBUY':
                take_price_steambuy(cursor)
                con.commit()
            case 'ZAKA_ZAKA':
                take_price_zaka_zaka(cursor)
                con.commit()
            case 'GABESTORE':
                take_price_gabestore(cursor)
                con.commit()
            case 'GAMERZ':
                take_games_gamerz(cursor)
                con.commit()

    cursor.close()
    con.close()