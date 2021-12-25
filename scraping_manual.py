import os

import requests
import re
import json
import time
from datetime import datetime, timedelta
from typing import Union


def get_links_from_detik(
        date_of_news: Union[datetime, str] = datetime.now(),
        is_pagination: bool = True
) -> list:

    news_url_result = []
    pagination_index = 1

    if isinstance(date_of_news, datetime):
        date_of_news = date_of_news.strftime("%m/%d/%Y")

    find_url_regex = re.compile(r'href=[\'"]?([^\'" >]+)[\'"] class="media__link" onclick=\'_pt\(this, \"news')

    while True:
        news_url = requests.get(f"https://news.detik.com/indeks/{pagination_index}?date={date_of_news}").text
        news_url_list = find_url_regex.findall(news_url)
        if not news_url_list:
            break
        news_url_result += news_url_list
        if not is_pagination:
            break
        pagination_index += 1

    news_url_result = list(set(news_url_result))
    return news_url_result


def get_news_content(
        url: list
) -> dict:

    get_text_from_html = re.compile(r"<p>(.+)</p>")
    get_date = re.compile(r'<div class="detail__date">(.+)</div>')
    get_title = re.compile(r'(?s)<h1 class="detail__title">(.+)</h1>')
    get_author = re.compile(r'<div class="detail__author">(.+)</div>')
    get_location = re.compile(r'<strong>([a-zA-Z0-9\s]+)</strong>')
    remove_html_tag = re.compile(r"<.*?>")
    final_news_content = {}

    for num, news_url_data in enumerate(url):
        get_news_contents = requests.get(news_url_data).text

        parse_news_content = get_text_from_html.findall(get_news_contents)
        get_date_news = "".join(get_date.findall(get_news_contents)).strip()
        get_title_news = "".join(get_title.findall(get_news_contents)).strip()
        get_author_news = "".join(get_author.findall(get_news_contents)).strip()
        get_location_news = "".join(get_location.findall(get_news_contents)).strip()

        readable_news_content = "".join([str_element for tuple_element in parse_news_content
                                          for str_element in tuple_element])
        readable_news_content = remove_html_tag.sub(" ", readable_news_content)
        readable_news_content = readable_news_content.replace('"', "").strip()

        final_news_content[f"news_{num + 1}"] = {
            "url": news_url_data,
            "title": get_title_news,
            "location": get_location_news,
            "author": get_author_news,
            "date": get_date_news,
            "content": readable_news_content
        }

    return final_news_content


def save_to_json(
        news_content_real: dict, filename="news_content"
) -> None:

    with open(f"{os.getcwd()}/results/{filename}.json", "w") as json_file:
        json.dump(news_content_real, json_file)
    print("JSON files generated!")


if __name__ == "__main__":
    start_time = time.time()
    date = datetime.now()
    today_news = get_links_from_detik(date)
    yesterday_news = get_links_from_detik(date - timedelta(days=1))
    two_days_ago_news = get_links_from_detik(date - timedelta(days=2))
    three_days_ago_news = get_links_from_detik(date - timedelta(days=3))
    all_news_url = today_news + yesterday_news + two_days_ago_news + three_days_ago_news
    news_content = get_news_content(all_news_url)
    save_to_json(news_content)
    # JSON file generated!

    print(
        f"""Total execution time: {(time.time() - start_time) / 60} minute(s) 
        and get {len(all_news_url)} news from detik.com""".strip())
    # Total execution time: 33.306561779975894 minute(s) and get 1813 news from detik.com
