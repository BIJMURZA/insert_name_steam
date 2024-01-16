import psycopg2
import pandas as pd


def take_games(market):
    df = pd.read_excel('Games.xlsx')
    return df[market].tolist()


def take_aid():
    df = pd.read_excel('Games.xlsx')
    return df['AID'].tolist()


def insert_game_name_marketplace(market, game, aid, cursor):
    update = f"UPDATE {market} SET game_name = %s WHERE aid = %s;"
    return cursor.execute(update, (game, aid))


if __name__ == "__main__":
    con = psycopg2.connect(dbname='rusync', user='admin',
                           password='1945', host='localhost')
    cursor = con.cursor()

    marketplaces = ['STEAM', 'STEAMPAY', 'GAMERZ', 'ZAKA_ZAKA', 'GABESTORE', 'GAME_MAG', 'STEAMBUY']
    aid = take_aid()

    for marketplace in marketplaces:
        games = take_games(marketplace)
        for i in range(len(games)):
            insert_game_name_marketplace(marketplace, games[i], aid[i], cursor)
            con.commit()
        games.clear()

    cursor.close()
    con.close()
