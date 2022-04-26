import os
import re
import sys
import json
import time
import asyncio
from typing import Union
from pathlib import Path
from aiohttp import ClientSession
from datetime import datetime, timedelta


async def get_links_from_detik(
    session: ClientSession,
    date_of_news: Union[datetime, str] = datetime.now(),
    is_pagination: bool = True,
    **kwargs
) -> list:
    await asyncio.sleep(1)
    news_url_result = []
    pagination_index = 1
    if isinstance(date_of_news, datetime):
        date_of_news = date_of_news.strftime("%m/%d/%Y")
    find_url_regex = re.compile(
        r'href=[\'"]?([^\'" >]+)[\'"] class="media__link" onclick=\'_pt\(this, \"news')
    while True:
        news_url_res = await session.request(method='GET', url=f"https://news.detik.com/indeks/{pagination_index}?date={date_of_news}", **kwargs)
        news_url = await news_url_res.text()
        news_url_list = find_url_regex.findall(news_url)
        if not news_url_list:
            break
        news_url_result += news_url_list
        if not is_pagination:
            break
        pagination_index += 1
    news_url_result = list(set(news_url_result))
    return news_url_result


async def get_news_content(
    session: ClientSession,
    url: list,
    **kwargs
) -> dict:
    await asyncio.sleep(1)
    get_text_from_html = re.compile(r"<p>(.+)</p>")
    get_date = re.compile(r'<div class="detail__date">(.+)</div>')
    get_title = re.compile(r'(?s)<h1 class="detail__title">(.+)</h1>')
    get_author = re.compile(r'<div class="detail__author">(.+)</div>')
    get_location = re.compile(r'<strong>([a-zA-Z0-9\s]+)</strong>')
    remove_html_tag = re.compile(r"<.*?>")
    get_news = await session.request(method='GET', url=url, **kwargs)
    get_news_contents = await get_news.text()
    parse_news_content = get_text_from_html.findall(get_news_contents)
    get_date_news = "".join(get_date.findall(get_news_contents)).strip()
    get_title_news = "".join(get_title.findall(get_news_contents)).strip()
    get_author_news = "".join(get_author.findall(get_news_contents)).strip()
    get_location_news = "".join(
        get_location.findall(get_news_contents)).strip()
    readable_news_content = "".join(
        [str_element for tuple_element in parse_news_content for str_element in tuple_element])
    readable_news_content = remove_html_tag.sub(" ", readable_news_content)
    readable_news_content = readable_news_content.replace('"', "").strip()

    final_news_content = {
        "url": url,
        "title": get_title_news,
        "location": get_location_news,
        "author": get_author_news,
        "date": get_date_news,
        "content": readable_news_content
    }

    return final_news_content


async def save_news_to_json(
    session: ClientSession,
    url: str,
    filename: str,
    num: Union[str, int, None] = None,
    **kwargs
) -> None:

    news_content = await get_news_content(session, url, **kwargs)

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


async def get_news(
    filename: str,
    date_of_news: Union[datetime, str] = datetime.now(),
    **kwargs
) -> int:
    async with ClientSession() as session:
        urls = await get_links_from_detik(session, date_of_news)
        tasks = []
        for num, url in enumerate(urls):
            print(f"Getting {num+1} news content from {url}")
            tasks.append(
                save_news_to_json(session, url, filename, num+1, **kwargs)
            )
        await asyncio.gather(*tasks)
    print(f"Generated JSON Files: {filename}! with {len(urls)} news content")
    return len(urls)

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

