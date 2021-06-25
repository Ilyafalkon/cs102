import requests
from bs4 import BeautifulSoup
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from db import News, session

Base = declarative_base()
engine = create_engine("sqlite:///news.db")
session = sessionmaker(bind=engine)


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    info = {}
    table = parser.find_all("td", "title")
    table_2 = parser.find_all("td", "subtext")
    signal_of_title = 1
    for i in range(1, len(table), 2):
        info["author"] = table_2[int(i / 2)].a.text

        if table_2[int(i / 2)].find_all("a")[-1].text == "discuss":
            info["comments"] = 0
        else:
            info["comments"] = int(table_2[int(i / 2)].find_all("a")[-1].text.split()[0])

        info["points"] = int(table_2[int(i / 2)].span.text.split()[0])

        info["title"] = table[i].a.text

        info["url"] = table[i].a.get("href")

        news_list.append(info)
        info = {}
    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    table = parser.find_all("td", "title")
    next_page = table[-1].a.get("href")
    return next_page


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news


if __name__ == "__main__":
    get_news("https://news.ycombinator.com/newest")
