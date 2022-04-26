import os
import json
import time
import asyncio
from typing import Union
from bs4 import BeautifulSoup
from bs4.element import ResultSet
from aiohttp import ClientSession
from datetime import datetime
from pathlib import Path


class Scraping:

    def __init__(self):
        self.start_time = time.time()

    def __del__(self):
        end_time = time.time()
        total = int(end_time - self.start_time)
        print(f"Time taken: {total} seconds, approximate {total / 60} minutes")

    async def __get_html(
            self,
            session: ClientSession,
            endpoint_url: str,
            **kwargs
    ) -> ResultSet:
        res = await session.request(method='GET', url=endpoint_url, **kwargs)
        res.raise_for_status()
        html = await res.text()
        soup = BeautifulSoup(html, "html.parser")
        a_result = soup.findAll("a", class_="media__link")
        return a_result

    async def __get_next_urls(
        self,
        session: ClientSession,
        endpoint_url: str,
        **kwargs
    ) -> Union[str, None]:
        res = await session.request(method='GET', url=endpoint_url, **kwargs)
        res.raise_for_status()
        html = await res.text()
        soup = BeautifulSoup(html, "html.parser")
        result = soup.find_all("a", class_="pagination__item", href=True)
        if result[-1].text == "Next":
            print(f"Getting news url from {result[-1]['href']}")
            return result[-1]["href"]
        else:
            return None

    async def get_urls(
        self,
        session: ClientSession,
        endpoint_url: str,
        is_pagination: bool = False,
        date_of_news: Union[datetime, str] = datetime.now(),
        **kwargs
    ) -> list:

        if isinstance(date_of_news, datetime):
            date_of_news = date_of_news.strftime("%m/%d/%Y")

        endpoint_url = f"{endpoint_url}?date={date_of_news}"
        print(f"Getting news url from {endpoint_url}")

        urls_result = []

        while True:
            # server will refuse if too many requests, set a delay to avoid that
            await asyncio.sleep(1)
            result = await self.__get_html(session, endpoint_url, **kwargs)
            if not result:
                break
            for get_url_result in result:
                urls_result.append(get_url_result.get("href"))
            if not is_pagination:
                return list(set(urls_result))
            endpoint_url = await self.__get_next_urls(session, endpoint_url, **kwargs)
            if not endpoint_url:
                return list(set(urls_result))

        return list(set(urls_result))

    async def get_news_content(
        self,
        session: ClientSession,
        url: str,
        **kwargs
    ) -> dict:

        # server will refuse if too many requests, set a delay to avoid that
        await asyncio.sleep(1)

        res = await session.request(method='GET', url=url, **kwargs)
        res.raise_for_status()
        html = await res.text()
        soup = BeautifulSoup(html, "html.parser")
        content = soup.find_all("p")
        content_clean = "".join(
            [i.text for i in content]).replace("\n", "").strip()

        try:
            get_date = soup.find("div", class_="detail__date").text
            get_title = soup.find(
                "h1", class_="detail__title").text.replace("\n", "").strip()
            get_author = soup.find("div", class_="detail__author").text
            get_location = soup.find("strong").text
        except:
            get_date = ""
            get_title = ""
            get_author = ""
            get_location = ""

        news_contents = {
            "url": url,
            "title": get_title,
            "location": get_location,
            "author": get_author,
            "date": get_date,
            "content": content_clean
        }

        return news_contents

    async def save_news_to_json(
        self,
        session: ClientSession,
        url: str,
        filename: str,
        num: Union[str, int, None] = None,
        **kwargs
    ) -> None:

        news_content = await self.get_news_content(session, url, **kwargs)

        abs_path = Path(__file__).parent.parent
        folder_path = f'{abs_path}/results/'
        filename_path = f"{folder_path}{filename}.json"

        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)

        try:
            with open(filename_path) as r:
                news_contents = json.load(r)
        except FileNotFoundError:
            with open(filename_path, 'w') as r:
                json.dump({}, r)
            with open(filename_path) as r:
                news_contents = json.load(r)

        news_contents.update({
            f"news_{num}": news_content
        })

        with open(filename_path, "w") as json_file:
            json.dump(news_contents, json_file)

    async def get_all_news_data(
        self,
        endpoint_url: str,
        is_pagination: bool = False,
        date_of_news: Union[datetime, str] = datetime.now(),
        filename: Union[str, None] = None,
        **kwargs
    ) -> None:
        async with ClientSession() as session:
            if not filename:
                filename = str(date_of_news)

            tasks = []
            urls = await self.get_urls(session, endpoint_url, is_pagination, date_of_news)
            for num, url in enumerate(urls):
                print(f"Getting {num+1} news content from {url}")
                tasks.append(
                    self.save_news_to_json(
                        session, url, filename, num+1, **kwargs)
                )
            await asyncio.gather(*tasks)
        print(f"Generated JSON Files: {filename}!")

