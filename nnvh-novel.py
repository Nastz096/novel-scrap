import requests
from bs4 import BeautifulSoup

# input_url = input("Paste the your chapter URL: ")
# input_character = int(input("Enter the chapter number: "))
url = requests.get(
    "https://truyenyy.vip/truyen/nhat-niem-vinh-hang-dich/chuong-1350.html")
soup = BeautifulSoup(url.content, "html.parser")


CHAPTERS = 100
# # for i in range(CHAPTERS):
# parent_content = soup.find_all("div", class_="inner")
# title = soup.find_all("h1", class_="chapter-title")
# print(title)
# print(parent_content)
# pass
