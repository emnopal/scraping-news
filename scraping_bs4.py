import json
import os
import time
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet
from typing import Union


class Scraping:

    def __init__(self):
        self.start_time = time.time()

    def __del__(self):
        end_time = time.time()
        total = int(end_time - self.start_time)
        print(f"Time taken: {total} seconds, approximate {total / 60} minutes")

    def __get_html(
            self,
            endpoint_url: str
    ) -> ResultSet:

        res = requests.get(endpoint_url)
        html = res.content
        soup = BeautifulSoup(html, "html.parser")
        a_result = soup.findAll("a", class_="media__link")

        return a_result

    def __get_next_urls(
            self,
            endpoint_url: str
    ) -> Union[str, None]:

        res = requests.get(endpoint_url)
        html = res.content
        soup = BeautifulSoup(html, "html.parser")
        result = soup.find_all("a", class_="pagination__item", href=True)

        if result[-1].text == "Next":
            print(f"Getting news url from {result[-1]['href']}")
            return result[-1]["href"]

        else:
            return None

    def get_urls(
            self,
            endpoint_url: str,
            is_pagination: bool = False,
            date_of_news: Union[datetime, str] = datetime.now()
    ) -> list:

        if isinstance(date_of_news, datetime):
            date_of_news = date_of_news.strftime("%m/%d/%Y")

        endpoint_url = f"{endpoint_url}?date={date_of_news}"
        print(f"Getting news url from {endpoint_url}")

        urls_result = []

        while True:
            time.sleep(1)  # server will refuse if too many requests, set a delay to avoid that
            result = self.__get_html(endpoint_url)
            if not result:
                break
            for get_url_result in result:
                urls_result.append(get_url_result.get("href"))
            if not is_pagination:
                return list(set(urls_result))
            endpoint_url = self.__get_next_urls(endpoint_url)
            if not endpoint_url:
                return list(set(urls_result))

        return list(set(urls_result))

    def get_news_content(
            self,
            endpoint_url: str,
            is_pagination: bool = False,
            date_of_news: Union[datetime, str] = datetime.now()
    ) -> dict:

        news_contents = {}

        for num, url in enumerate(self.get_urls(endpoint_url, is_pagination, date_of_news)):
            print(f"Getting {num+1} news content from {url}")
            time.sleep(1)  # server will refuse if too many requests, set a delay to avoid that
            res = requests.get(url)
            html = res.content
            soup = BeautifulSoup(html, "html.parser")
            content = soup.find_all("p")
            content_clean = "".join([i.text for i in content]).replace("\n", "").strip()

            try:
                get_date = soup.find("div", class_="detail__date").text
                get_title = soup.find("h1", class_="detail__title").text.replace("\n", "").strip()
                get_author = soup.find("div", class_="detail__author").text
                get_location = soup.find("strong").text
            except:
                get_date = ""
                get_title = ""
                get_author = ""
                get_location = ""

            news_contents[f"news_{num + 1}"] = {
                "url": url,
                "title": get_title,
                "location": get_location,
                "author": get_author,
                "date": get_date,
                "content": content_clean
            }

        print(f"{len(news_contents)} news content generated!")

        return news_contents

    @staticmethod
    def save_to_json(
            news_content_real: Union[list, dict],
            filename="test"
    ) -> None:

        with open(f"{os.getcwd()}/results/{filename}.json", "w") as json_file:
            json.dump(news_content_real, json_file)

        print("JSON files generated!")


if __name__ == "__main__":

    scraping = Scraping()
    date = datetime.now()

    # urls = scraping.get_urls("https://news.detik.com/indeks", is_pagination=False)
    # scraping.save_to_json(urls, filename="no_pagination")

    # urls = scraping.get_urls("https://news.detik.com/indeks", is_pagination=True)
    # scraping.save_to_json(urls, filename="pagination")

    # news_content = scraping.get_news_content("https://news.detik.com/indeks", is_pagination=False)
    # scraping.save_to_json(news_content, filename="news_content_bs4_no_pagination")

    # Bad idea for getting all the news content for 7 days in one run,
    # so use one day in one run (until 7x runs) instead

    # Get one week news content

    # day 1st
    news_content_now = scraping.get_news_content(
        "https://news.detik.com/indeks", is_pagination=True, date_of_news=date)
    scraping.save_to_json(news_content_now, filename="today_news_content")

    # day 2nd
    # news_content_yesterday = scraping.get_news_content(
    #     "https://news.detik.com/indeks", is_pagination=True, date_of_news=date - timedelta(days=1))
    # scraping.save_to_json(news_content_now, filename="yesterday_news_content")

    # day 3rd
    # news_content_2days = scraping.get_news_content(
    #     "https://news.detik.com/indeks", is_pagination=True, date_of_news=date - timedelta(days=2))
    # scraping.save_to_json(news_content_now, filename="two_days_ago_news_content")

    # day 4th
    # news_content_3days = scraping.get_news_content(
    #     "https://news.detik.com/indeks", is_pagination=True, date_of_news=date - timedelta(days=3))
    # scraping.save_to_json(news_content_now, filename="three_days_ago_news_content")

    # day 5th
    # news_content_4days = scraping.get_news_content(
    #     "https://news.detik.com/indeks", is_pagination=True, date_of_news=date - timedelta(days=4))
    # scraping.save_to_json(news_content_now, filename="four_days_ago_news_content")

    # day 6th
    # news_content_5days = scraping.get_news_content(
    #     "https://news.detik.com/indeks", is_pagination=True, date_of_news=date - timedelta(days=5))
    # scraping.save_to_json(news_content_now, filename="five_days_ago_news_content")

    # day 7th
    # news_content_6days = scraping.get_news_content(
    #     "https://news.detik.com/indeks", is_pagination=True, date_of_news=date - timedelta(days=6))
    # scraping.save_to_json(news_content_now, filename="six_days_ago_news_content")
