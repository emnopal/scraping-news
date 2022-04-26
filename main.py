import sys
import time
import json
import asyncio
from src import scraping as sc
from src import manual_scraping as msc
from src import es_processing as esp
from datetime import datetime, timedelta

if __name__ == "__main__":

    # set event loop policy for windows user
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # Using manual scraping

    # start_time = time.time()
    # date = datetime.now()
    # length_url = asyncio.run(get_news(f"test{date.strftime('%d%m%Y')}"))
    # print(f"""Total execution time: {(time.time() - start_time) / 60} minute(s) ({time.time() - start_time} s) and get {sum(length_url)} news""")

    # Total execution time: 0.29508498509724934 minute(s) (17.70509910583496 s) and get 182 news

    # Example of 10 days news

    # length_data = []
    # for i in range(10):
    #     if i == 0:
    #         length_url = asyncio.run(msc.get_news(f"{date.strftime('%d%m%Y')}"))
    #         length_data.append(length_url)
    #     else:
    #         length_url = asyncio.run(msc.get_news(
    #             f"{(date - timedelta(days=i)).strftime('%d%m%Y')}", date - timedelta(days=i)))
    #         length_data.append(length_url)

    # print(
    #     f"""
    #     Total execution time: {(time.time() - start_time) / 60} minute(s)
    #     ({time.time() - start_time} s) and get {sum(length_data)} news
    #     """.strip()
    # )

    # Total execution time: 12.5 minute(s) (750 s) and get 4212 news

    # Using beautifulsoup scraping
    scraping = sc.Scraping()
    date = datetime.now()

    # Get today news
    # asyncio.run(
    #     scraping.get_all_news_data(
    #         "https://news.detik.com/indeks",
    #         is_pagination=True,
    #         date_of_news=date,
    #         filename=date.strftime('%d%m%Y')
    #     )
    # )

    # Get 10 Days News
    for i in range(10):
        if i == 0:
            asyncio.run(
                scraping.get_all_news_data(
                    "https://news.detik.com/indeks",
                    is_pagination=True,
                    date_of_news=date,
                    filename=date.strftime('%d%m%Y')
                )
            )
        else:
            asyncio.run(
                scraping.get_all_news_data(
                    "https://news.detik.com/indeks",
                    is_pagination=True,
                    date_of_news=date - timedelta(days=i),
                    filename=(date - timedelta(days=i)).strftime('%d%m%Y')
                )
            )

    # Time taken: 735 seconds, approximate 12.25 minutes
    # saving almost 2 Hours than previous version (not using asynchronous)

    # elasticsearch processing
    # esp.create_index('news')

    # jsons_1 = []
    # json_1 = json.load(open('26122021.json', 'rb'))
    # for key, value in json_1.items():
    #     value['content'] = value['content'].replace('"', "").replace("'", "")
    #     _id = key.split("_")[-1]
    #     jsons_1.append(
    #         '{"index": {"_index":"news","_type":"_doc","_id":"news_26122021_%s"}}\n%s\n' % (_id, json.dumps(value))
    #     )
    # data_1 = ''.join(jsons_1)
    # esp.add_document('news', data_1)

    # jsons_2 = []
    # json_2 = json.load(open('25122021.json', 'rb'))
    # for key, value in json_2.items():
    #     value['content'] = value['content'].replace('"', "").replace("'", "")
    #     _id = key.split("_")[-1]
    #     jsons_2.append(
    #         '{"index": {"_index":"news","_type":"_doc","_id":"news_25122021_%s"}}\n%s\n' % (_id, json.dumps(value))
    #     )
    # data_2 = ''.join(jsons_2)
    # esp.add_document('news', data_2)

    # jsons_3 = []
    # json_3 = json.load(open('24122021.json', 'rb'))
    # for key, value in json_3.items():
    #     value['content'] = value['content'].replace('"', "").replace("'", "")
    #     _id = key.split("_")[-1]
    #     jsons_3.append(
    #         '{"index": {"_index":"news","_type":"_doc","_id":"news_24122021_%s"}}\n%s\n' % (_id, json.dumps(value))
    #     )
    # data_3 = ''.join(jsons_3)
    # esp.add_document('news', data_3)

    # # Default search query
    # print(esp.es_results('news'))
    # print("total documents:", esp.es_results('news')['hits']['total']['value'])

    # # Searching 10 documents, sorted by default
    # data = {
    #     "size": 10,
    #     "query": {
    #         "match_all": {}
    #     }
    # }
    # print(esp.es_results('news', data=data))

    # # Searching documents by specific field, for example, url
    # data = {
    #     "size": 10,
    #     "query": {
    #         "match_all": {}
    #     },
    #     "_source": False,
    #     "fields": ["url"]
    # }
    # print(esp.es_results('news', data=data))

    # # Searching match documents in specific field, for example, searching word "Komika" in content field
    # data = {
    #     "size": 10,
    #     "query": {
    #         "match": {
    #             "content": "Komika"
    #         }
    #     },
    #     "_source": False,
    #     "fields": ["content"]
    # }
    # print(esp.es_results('news', data=data))

