import psycopg2
import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":
    con = psycopg2.connect(dbname='rusync', user='admin',
                           password='1945', host='localhost')
    cursor = con.cursor()
    cursor.execute('SELECT * FROM games')
    aid = []
    for row in cursor.fetchall():
        aid.append(row[0])

    update = f"UPDATE games SET min_req = %s, rec_req = %s WHERE aid = %s "
    data_min = []
    data_rec = []
    for i in range(len(aid)):
        url = f"https://store.steampowered.com/app/{aid[i]}"
        response = requests.get(url, headers={'Accept-Language': 'ru-Ru'})
        soup = BeautifulSoup(response.content, "lxml")
        print(aid[i])
        print("Минимальные: ")
        min_div = soup.find("div", class_="game_area_sys_req_leftCol")
        min_ul = min_div.find_all("ul", class_="bb_ul")
        for min_li in min_ul:
            min_req = min_li.find_all("li")
            for minimum_req in min_req:
                data_min.append(minimum_req.text.strip())
        print("\nРекомендованные: ")
        rec_div = soup.find("div", class_="game_area_sys_req_rightCol")
        rec_ul = rec_div.find_all("ul", class_="bb_ul")
        for rec_li in rec_ul:
            rec_req = rec_li.find_all("li")
            for recommended_req in rec_req:
                data_rec.append(recommended_req.text.strip())
        cursor.execute(update, ('\n'.join(data_min), '\n'.join(data_rec), aid[i]))
        data_min = []
        data_rec = []
        con.commit()
        #         data_req.append(recommended_req.text.strip())
        # cursor.execute(update, (data_min, data_req, aid[i]))


    cursor.close()
    con.close()