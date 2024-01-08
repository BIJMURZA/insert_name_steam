import requests
from bs4 import BeautifulSoup
import lxml


url = "https://store.steampowered.com/app/"
aid = 271590

url += str(aid)

response = requests.get(url, headers={'Accept-Language': 'ru-RU,ru;q=0'})
soup = BeautifulSoup(response.text, "lxml")

game_name = soup.find("div", class_="apphub_AppName").text
game_distription = soup.find("div", class_="game_description_snippet").text.strip()
game_developer = soup.find("div", id="developers_list").text.strip()

print("Game Name: " + game_name)
print("Game Description: " + game_distription)
print("Developer: " + game_developer)
