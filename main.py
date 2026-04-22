from typing import Any

import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from dataclasses import dataclass
from pprint import pprint



class Habr:
    main_page = 'https://habr.com/'
    topic = 'https://habr.com/ru/articles/top/daily/'

    @dataclass
    class __ArticleData:
        title: str
        views: str
        link: str
        text: str

    class Page(BeautifulSoup):
        def __init__(self, url: str, **kwargs: Any):
            super().__init__(**kwargs)
            self.url = url

        @property
        def html(self) -> str:
            res = requests.get(
                self.url,
                headers={
                    'User-Agent': UserAgent().google
                }
            )
            return res.text

        @property
        def soup(self) -> BeautifulSoup:
            return BeautifulSoup(self.html, 'lxml')


    @staticmethod
    def get_best_posts() -> list[__ArticleData]:
        posts_data = []
        topic_page = Habr.Page(Habr.topic)
        all_articles_soup = topic_page.soup.find_all('article', class_='tm-articles-list__item')

        for article_soup in all_articles_soup:
            article_title = article_soup.find('a', class_='tm-title__link').find('span').text
            article_views = article_soup.find('span', class_='tm-icon-counter__value').text
            article_link = str(article_soup.find('a', class_='tm-title__link')['href'])

            article_page = Habr.Page(Habr.main_page + article_link)
            article_text = article_page.soup.find('div', class_='article-body').text

            posts_data.append(Habr.__ArticleData(article_title, article_views, article_link, article_text))
        return posts_data

def main():
    pprint(Habr.get_best_posts())

if __name__ == '__main__':
    main()