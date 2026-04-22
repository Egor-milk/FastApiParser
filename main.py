import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from dataclasses import dataclass
from pprint import pprint


main_page = 'https://habr.com/'
topic = 'ru/articles/top/daily/'


def get_url_html(url: str) -> str:
    res = requests.get(
        url,
        headers={
            'User-Agent': UserAgent().google
        }
    )
    return res.text

def get_soup(html_text: str) -> BeautifulSoup:
    return BeautifulSoup(html_text, 'lxml')

@dataclass
class ArticleData:
    title: str
    views: str
    link : str
    text : str


def get_all_text_from_posts(soup: BeautifulSoup):
    article_text = soup.find('div', class_ = 'article-body').text
    return article_text

def get_best_habr_posts() -> list[ArticleData]:
    posts_data = []
    topic_soup = get_soup(get_url_html(main_page + topic))
    all_articles_soup = topic_soup.find_all('article', class_ = 'tm-articles-list__item')
    for article_soup in all_articles_soup:
        article_title: str = article_soup.find('a', class_='tm-title__link').find('span').text
        article_views = article_soup.find('span', class_='tm-icon-counter__value').text
        article_link: str = str(article_soup.find('a', class_='tm-title__link')['href'])
        article_text = get_all_text_from_posts(get_soup(get_url_html(main_page + article_link)))
        posts_data.append(ArticleData(article_title, article_views, article_link, article_text))
    return posts_data

def main():
    pprint(get_best_habr_posts())

if __name__ == '__main__':
    main()