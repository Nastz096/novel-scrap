import requests
from ebooklib import epub
from bs4 import BeautifulSoup
base_url = "https://bachngocsach.com"
url = input("Copy your URL: ")
html = requests.get(url)
soup = BeautifulSoup(html.content, "html.parser")

book_identifier = input("Enter your book identifier: ")
book_title = input("Enter your book title: ")
book_author = input("Enter your book author: ")
if __name__ == '__main__':

    book = epub.EpubBook()

# set metadata
    book.set_identifier(book_identifier)
    book.set_title(book_title)
    book.set_language("vn")
    book.add_author(book_author)
    beginningChapter = int(input("Enter your beginning Chapter: ")) - 1

    file_name = input("Enter your ebook file name: ")

    CHAPTERS = int(input("How many chapters do you want? "))
    intro = epub.EpubHtml(title="Introduction",
                          file_name='intro.xhtml', lang='en')
    intro.content = "<h1>About this book</h1><p>This is my web scraping epub book for my favorite novel</p>"
    book.add_item(intro)
    myDict = {}
    for i in range(1, CHAPTERS + 1):
        if i != 1:
            try:
                next_chapter_button = soup.find(
                    "a", class_="page-next captainicon chuong-button")
                url = base_url + next_chapter_button['href']
                html = requests.get(url)
                soup = BeautifulSoup(html.content, "html.parser")
                myTitle = soup.find("h1", id="chuong-title")
                myInfo = soup.find("div", id="info")
                myContent = soup.find("div", id="noi-dung")
            except TypeError:
                print("THE END!")
                break

            chap = beginningChapter + i
            print(f"Processing {chap}")
            myDict[f"chap{chap}"] = epub.EpubHtml(title=str(myTitle.get_text()),
                                                  file_name=f"chap{chap}.xhtml", content=str(myTitle) + str(myInfo) + str(myContent))
        else:
            chap = beginningChapter + i

            myTitle = soup.find("h1", id="chuong-title")
            myInfo = soup.find("div", id="info")

            myContent = soup.find("div", id="noi-dung")
            print(f"Processing {chap}")
            myDict[f"chap{chap}"] = epub.EpubHtml(title=str(myTitle.get_text()),
                                                  file_name=f"chap{chap}.xhtml", content=str(myTitle) + str(myInfo) + str(myContent))

        book.add_item(myDict[f"chap{chap}"])

    myChapters = list(myDict.keys())
    myChaptersContent = [myDict[x] for x in myChapters]
    book.toc = (epub.Link('intro.xhtml', "Introduction", 'intro'),
                (epub.Section("Chapters"),
                 (myChaptersContent))
                )

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    style = '''
@namespace epub "http://www.idpf.org/2007/ops";

body {
    font-family: Cambria, Liberation Serif, Bitstream Vera Serif, Georgia, Times, Times New Roman, serif;
}

h2 {
     text-align: left;
     text-transform: uppercase;
     font-weight: 200;     
}

ol {
        list-style-type: none;
}

ol > li:first-child {
        margin-top: 0.3em;
}


nav[epub|type~='toc'] > ol > li > ol  {
    list-style-type:square;
}


nav[epub|type~='toc'] > ol > li > ol > li {
        margin-top: 0.3em;
}

'''
    nav_css = epub.EpubItem(
        uid='style_nav', file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)
    book.spine = ['nav', intro] + myChaptersContent

    epub.write_epub(f"{file_name}.epub", book, {})
