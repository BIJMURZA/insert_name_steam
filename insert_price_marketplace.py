import psycopg2
import requests
from bs4 import BeautifulSoup


def take_price_steam(aid_game):
    url = f"https://store.steampowered.com/app/{aid_game}/"
    response = requests.get(url, headers={'Accept-Language': 'ru-Ru'})
    soup = BeautifulSoup(response.content, "lxml")
    if soup.find("div", class_="game_area_purchase_game_wrapper") is not None:
        if soup.find_all("div", class_="game_area_purchase_game_wrapper")[0].find("div", class_="discount_final_price") is not None:
            return soup.find_all("div", class_="game_area_purchase_game_wrapper")[0].find("div", class_="discount_final_price").text.split()[0]
        elif soup.find_all("div", class_="game_area_purchase_game_wrapper")[0].find("div", class_="game_purchase_price price") is not None:
            return soup.find_all("div", class_="game_area_purchase_game_wrapper")[0].find("div",  class_="game_purchase_price price").text.split()[0]
    else:
        return "Нет в наличии"


def take_price_steampay(game_name):
    url = f"https://steampay.com/game/{game_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")
    if soup.find("div", class_="product__current-price"):
        price = soup.find("div", class_="product__current-price").text.split()[0]
        if price != "СКОРО":
            return price
        else:
            return "Нет в наличии"
    elif game_name == "-":
        return "-"
    else:
        return "Нет в наличии"


def take_price_steambuy(game_name):
    url = f"https://steambuy.com/{game_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")
    if soup.find("div", class_="product-price__action").text.strip() != "Нет в наличии":
        return soup.find("div", class_="product-price__cost").text.split()[0]
    elif game_name == "-":
        return "-"
    else:
        return "Нет в наличии"
         

def take_price_zaka_zaka(game_name):
    url = f"https://zaka-zaka.com/game/{game_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")
    if soup.find("div", class_="price"):
        return soup.find("div", class_="price").text.split()[0]
    elif game_name == "-":
        return "-"
    else:
        return "Нет в наличии"


def take_price_gabestore(game_name):
    url = f"https://gabestore.ru/game/{game_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")
    if soup.find("div", class_="b-card__price-currentprice"):
        return soup.find("div", class_="b-card__price-currentprice").text.split()[0]
    elif game_name == "-":
        return "-"
    else:
        return "Нет в наличии"


def take_price_gamerz(game_name):
    url = f"https://gamerz.online/game/{game_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")
    if soup.find("p", class_="price"):
        return soup.find("p", class_="price").text.split()[0]
    elif game_name == "-":
        return "-"
    else:
        return "Нет в наличии"


if __name__ == "__main__":
    con = psycopg2.connect(dbname='rusync', user='admin',
                           password='1945', host='localhost')
    cursor = con.cursor()

    marketplaces = ['steam', 'steampay', 'gamerz', 'zaka_zaka', 'gabestore', 'steambuy']

    for marketplace in marketplaces:
        update = f"UPDATE {marketplace} SET price = %s WHERE game_name = %s"
        cursor.execute(f"SELECT aid FROM games")
        aids = [row[0] for row in cursor.fetchall()]
        cursor.execute(f"SELECT game_name FROM {marketplace}")
        games = [row[0] for row in cursor.fetchall()]
        match marketplace:
            case 'steam':
                for aid in aids:
                    cursor.execute(f"UPDATE steam SET price = %s WHERE aid = %s", (take_price_steam(aid), aid))
            case 'steampay':
                for game in games:
                    cursor.execute(update, (take_price_steampay(game), game))
            case 'steambuy':
                for game in games:
                    cursor.execute(update, (take_price_steambuy(game), game))
            case 'zaka_zaka':
                for game in games:
                    cursor.execute(update, (take_price_zaka_zaka(game), game))
            case 'gabestore':
                for game in games:
                    cursor.execute(update, (take_price_gabestore(game), game))
            case 'gamerz':
                for game in games:
                    cursor.execute(update, (take_price_gamerz(game), game))
        con.commit()

    cursor.close()
    con.close()