import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":
    app = "2050650"
    url = f"https://store.steampowered.com/app/{app}"
    response = requests.get(url, headers={'Accept-Language': 'ru-Ru'})
    soup = BeautifulSoup(response.content, "lxml")

    print("Минимальные: ")
    min_div = soup.find("div", class_="game_area_sys_req_leftCol")
    min_ul = min_div.find_all("ul", class_="bb_ul")
    for min_li in min_ul:
        min_req = min_li.find_all("li")
        for minimum_req in min_req:
            print(minimum_req.text.strip())

    print("\nРекомендованные: ")
    rec_div = soup.find("div", class_="game_area_sys_req_rightCol")
    rec_ul = rec_div.find_all("ul", class_="bb_ul")
    for rec_li in rec_ul:
        rec_req = rec_li.find_all("li")
        for recommended_req in rec_req:
         print(recommended_req.text.strip())
