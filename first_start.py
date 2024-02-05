import psycopg2
import requests
import pandas as pd
from bs4 import BeautifulSoup

def take_aid():
    df = pd.read_excel('Games.xlsx')
    return df['AID'].tolist()

def take_genre():
    df = pd.read_excel('Games.xlsx')
    return df['Жанр'].tolist()


def take_aid_gfn():
    df = pd.read_excel('Games.xlsx')
    return df['AID GFN'].tolist()

def insert_aid(game, genre, gfn, cursor):
    update = """INSERT INTO games (aid, genre, aid_gfn) VALUES (%s, %s, %s);"""
    cursor.execute(update, (game, genre, gfn, ))


if __name__ == "__main__":
    con = psycopg2.connect(dbname='rusync', user='admin',
                           password='1945', host='localhost')
    cursor = con.cursor()
    aid_list = take_aid()
    aid_list_gfn = take_aid_gfn()
    genre_list = take_genre()

    for game in range(len(aid_list)):
        print("aid: ", aid_list[game])
        print("genre: ", genre_list[game])
        print("gfn: ", aid_list_gfn[game])
        print(" ")
        insert_aid(aid_list[game], genre_list[game], aid_list_gfn[game], cursor)
        con.commit()

    cursor.close()
    con.close()
