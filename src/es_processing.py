import json
from typing import Dict, Union

import requests

# TODO: Implement Asynchronous here

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
