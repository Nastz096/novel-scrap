import requests
from bs4 import BeautifulSoup
base_url = "https://bachngocsach.com"
url = "https://bachngocsach.com/reader/nhat-niem-vinh-hang/yfrd"
html = requests.get(url)
soup = BeautifulSoup(html.content, "html.parser")

CHAPTERS = 500
with open("Nhat-niem-vinh-hang.txt", "w", encoding="utf-8") as output:
    for i in range(CHAPTERS):
        title = soup.find("h1", id="chuong-title")
        content = soup.find("div", id="noi-dung")
        output.write(title.get_text() + "\n\n\n")
        for para in content.find_all("p"):
            output.write(para.get_text() + "\n\n")
            pass

        output.write("\n\n\n\n")
        try:
            next_chapter_button = soup.find(
                "a", class_="page-next captainicon chuong-button")
            url = base_url + next_chapter_button['href']
            html = requests.get(url)
            soup = BeautifulSoup(html.content, "html.parser")

        except TypeError:
            print("The END!")
            break
    pass
# # for i in range(CHAPTERS):
# parent_content = soup.find_all("div", class_="inner")
# title = soup.find_all("h1", class_="chapter-title")
# print(title)
# print(parent_content)
# pass
