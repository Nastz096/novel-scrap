from bs4 import BeautifulSoup
from ebooklib import epub
import requests
base_url = "https://www.xinshuhaige.net"
url = "https://www.xinshuhaige.net/57876/773621.html"
html = requests.get(url)
soup = BeautifulSoup(html.content, "html.parser")

book = epub.EpubBook()

book.set_identifier("dauladailuc4")
book.set_title("Chung cực đấu la")
book.set_language("zh")
book.add_author("Đường Gia Tam Thiếu")

intro = epub.EpubHtml(title="Introduction",
                      file_name='intro.xhtml', lang='en')
intro.content = "<h1>About this book</h1><p>This is my web scraping epub book for my favorite novel Dau la dai luc IV</p>"
book.add_item(intro)

CHAPTERS = 10
myDict = {}
for i in range(CHAPTERS):
    chap = 39 + i
    if i != 0:
        page_navigation = soup.find("div", class_="pagego")
        chapter_urls = page_navigation.find_all("a")
        url = base_url + str(chapter_urls[2]["href"])
        html = requests.get(url)
        soup = BeautifulSoup(html.content, "html.parser")
        myTitle = soup.find("div", class_="read_title")
        myTitle = myTitle.find("h1")
        myContent = soup.find("div", class_="content")
        # except TypeError:
        #     print("THE END!")
        #     break
        print(f"Processing {chap}")
        myDict[f"chap{chap}"] = epub.EpubHtml(title=str(myTitle.get_text()),
                                              file_name=f"chap{chap}.xhtml", content=str(myTitle)+str(myContent))
    else:

        myTitle = soup.find("div", class_="read_title")
        myTitle = myTitle.find("h1")
        myContent = soup.find("div", class_="content")
        print(f"Processing {chap}")
        myDict[f"chap{chap}"] = epub.EpubHtml(title=str(myTitle.get_text()),
                                              file_name=f"chap{chap}.xhtml", content=str(myTitle) + str(myContent))

    book.add_item(myDict[f"chap{chap}"])

myChaptersList = list(myDict.keys())
myChaptersContent = [myDict[x] for x in myChaptersList]

book.toc = (epub.Link('intro.xhtml', "Introduction", 'intro'),
            (epub.Section("Chapters"),
             (myChaptersContent))
            )

book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

book.spine = [intro] + myChaptersContent

epub.write_epub("dau-la-dai-luc-4.epub", book, {})
