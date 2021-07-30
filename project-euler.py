from bs4 import BeautifulSoup
from ebooklib import epub
import requests


book = epub.EpubBook()

# set metadata
if __name__ == '__main__':
    book.set_identifier("projecteulernet123")
    book.set_title("Project Euler")
    book.set_language("en")
    book.add_author("Colin Hughes")

    intro = epub.EpubHtml(title="Introduction",
                          file_name='intro.xhtml', lang='en')
    intro.content = "<h1>About this book</h1><p>This is my web scraping for Project Euler</p>"
    book.add_item(intro)

    myProblemsDict = {}
    problemsnumber = 2  
    for i in range(1, problemsnumber+1):
        try:
            url = f"https://projecteuler.net/problem={i}"
            html = requests.get(url).content
            soup = BeautifulSoup(html, "html.parser")
            problemName = soup.find("h2")
            theNumberProb = soup.find("h3")
            theContent = soup.find("div", class_="problem_content")

            print(f"Processing {theNumberProb.get_text()}")
            theText = str(problemName) + str(theNumberProb) + str(theContent)

            myProblemsDict[theNumberProb.get_text()] = epub.EpubHtml(title=str(theNumberProb.get_text(
            )), file_name=f"{theNumberProb.get_text()}.xhtml", content=theText)

            book.add_item(myProblemsDict[theNumberProb.get_text()])

        except Exception as e:
            print("The End!")

theProblemList = list(myProblemsDict.keys())
theProblemContent = [myProblemsDict[x] for x in theProblemList]

book.toc = (epub.Link("intro.xhtml", "Introduction", 'intro'),
            (epub.Section("Problems"),
             (theProblemContent)))
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

book.spine = [intro] + theProblemContent

epub.write_epub("Project Euler Problems List.epub", book, {})
