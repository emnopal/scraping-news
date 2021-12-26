import json
from typing import Dict, Union

import requests


# Create an index in Elasticsearch
def create_index(index_name: str) -> dict[str, Union[int, str]]:
    url = 'http://localhost:9200/' + index_name
    headers = {'Content-Type': 'application/json'}
    data = {
        "mappings": {
            "properties": {
                "url": {
                    "type": "text"
                },
                "title": {
                    "type": "text"
                },
                "location": {
                    "type": "text"
                },
                "author": {
                    "type": "text"
                },
                "date": {
                    "type": "text"
                },
                "content": {
                    "type": "text"
                }
            }
        }
    }
    response = requests.put(url, headers=headers, data=json.dumps(data))
    response_prop = {
        "status_code": response.status_code,
        "text": response.text
    }
    print(response_prop)
    return response_prop


# Add a document to an index in Elasticsearch
def add_document(index_name: str, document: Union[str, Dict[str, str]]) -> dict[str, Union[int, str]]:
    url = 'http://localhost:9200/' + index_name + '/_bulk'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=document)
    response_prop = {
        "status_code": response.status_code,
        "text": response.text
    }
    print(response_prop)
    return response_prop


# Get all Elasticsearch index records
def es_results(
        index_name: str,
        save_result_as_json: bool = False,
        data: Union[str, bool, dict] = False
) -> requests.Response:
    url = f'http://localhost:9200/{index_name}/_search?pretty=true'
    if not data:
        data = {
            "size": 3,
            "query": {
                "match_all": {}
            }
        }
    else:
        data = data
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if save_result_as_json:
        with open("es_records.json", "w") as f:
            json.dump(response.json(), f)
    return response.json()


if __name__ == '__main__':

    create_index('news')

    jsons_1 = []
    json_1 = json.load(open('26122021.json', 'rb'))
    for key, value in json_1.items():
        value['content'] = value['content'].replace('"', "").replace("'", "")
        _id = key.split("_")[-1]
        jsons_1.append(
            '{"index": {"_index":"news","_type":"_doc","_id":"news_26122021_%s"}}\n%s\n' % (_id, json.dumps(value))
        )
    data_1 = ''.join(jsons_1)
    add_document('news', data_1)

    jsons_2 = []
    json_2 = json.load(open('25122021.json', 'rb'))
    for key, value in json_2.items():
        value['content'] = value['content'].replace('"', "").replace("'", "")
        _id = key.split("_")[-1]
        jsons_2.append(
            '{"index": {"_index":"news","_type":"_doc","_id":"news_25122021_%s"}}\n%s\n' % (_id, json.dumps(value))
        )
    data_2 = ''.join(jsons_2)
    add_document('news', data_2)

    jsons_3 = []
    json_3 = json.load(open('24122021.json', 'rb'))
    for key, value in json_3.items():
        value['content'] = value['content'].replace('"', "").replace("'", "")
        _id = key.split("_")[-1]
        jsons_3.append(
            '{"index": {"_index":"news","_type":"_doc","_id":"news_24122021_%s"}}\n%s\n' % (_id, json.dumps(value))
        )
    data_3 = ''.join(jsons_3)
    add_document('news', data_3)

    # Default search query
    print(es_results('news'))
    print("total documents:", es_results('news')['hits']['total']['value'])

    # Searching 10 documents, sorted by default
    data = {
        "size": 10,
        "query": {
            "match_all": {}
        }
    }
    print(es_results('news', data=data))

    # Searching documents by specific field, for example, url
    data = {
        "size": 10,
        "query": {
            "match_all": {}
        },
        "_source": False,
        "fields": ["url"]
    }
    print(es_results('news', data=data))

    # Searching match documents in specific field, for example, searching word "Komika" in content field
    data = {
        "size": 10,
        "query": {
            "match": {
                "content": "Komika"
            }
        },
        "_source": False,
        "fields": ["content"]
    }
    print(es_results('news', data=data))

