import requests
from bs4 import BeautifulSoup
import time
import logging


def extract_news(url):
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')

    articles_list = []

    articles = soup.find_all('div', {'class': 'list-item'})
    for article in articles:
        title_element = article.find('a', {'class': 'list-item__title color-font-hover-only'})
        annotation_element = article.find('p', class_='annotation')
        authors_element = article.find('div', class_='authors')

        title = title_element.text if title_element else "No title"
        annotation = annotation_element.text if annotation_element else "No annotation"
        authors = authors_element.text if authors_element else "No authors"

        articles_list.append((title, annotation, authors))

    return articles_list


def write_to_log(news):
    logger = logging.getLogger('news_logger')
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler('news.log')
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    for news_item in news:
        logger.info(news_item)


if __name__ == "__main__":
    url = 'https://ria.ru/world/'

    run_time = 4 * 60 * 60

    news_set = set()
    start_time = time.time()

    existing_news_set = extract_news(url)

    while time.time() - start_time < run_time:

        articles_list = extract_news(url)

        for article in articles_list:
            title = article[0]
            if 'США' in title or 'НАТО' in title or 'Украин' in title or 'Путин' in title:
                if article not in existing_news_set:
                    news_set.add(article)

        time.sleep(60)

    write_to_log(news_set)