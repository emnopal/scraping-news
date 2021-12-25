import os
import json
import unittest
from scraping_manual import get_links_from_detik, get_news_content, save_to_json


class TestScrapingManual(unittest.TestCase):

    def test_get_links(self):
        self.assertIsNotNone(get_links_from_detik(is_pagination=False))
        self.assertIsInstance(get_links_from_detik(is_pagination=False), list)

    def test_get_links_time(self):
        self.assertIsNotNone(get_links_from_detik(is_pagination=False, date_of_news="12/12/2021"))
        self.assertIsInstance(get_links_from_detik(is_pagination=False, date_of_news="12/12/2021"), list)

    def test_get_links_pagination(self):
        self.assertIsNotNone(get_links_from_detik(is_pagination=True))
        self.assertIsInstance(get_links_from_detik(is_pagination=True), list)

    def test_get_links_time_pagination(self):
        self.assertIsNotNone(get_links_from_detik(is_pagination=True, date_of_news="12/12/2021"))
        self.assertIsInstance(get_links_from_detik(is_pagination=True, date_of_news="12/12/2021"), list)

    def test_get_contents(self):
        list_content = get_links_from_detik(is_pagination=False)
        self.assertIsNotNone(get_news_content(url=list_content))
        self.assertIsInstance(get_news_content(url=list_content), dict)

    def test_get_contents_time(self):
        list_content = get_links_from_detik(is_pagination=False, date_of_news="12/12/2021")
        self.assertIsNotNone(get_news_content(url=list_content))
        self.assertIsInstance(get_news_content(url=list_content), dict)

    def test_get_contents_pagination(self):
        list_content = get_links_from_detik(is_pagination=True)
        self.assertIsNotNone(get_news_content(url=list_content))
        self.assertIsInstance(get_news_content(url=list_content), dict)

    def test_get_contents_time_pagination(self):
        list_content = get_links_from_detik(is_pagination=True, date_of_news="12/12/2021")
        self.assertIsNotNone(get_news_content(url=list_content))
        self.assertIsInstance(get_news_content(url=list_content), dict)

    def test_json_write(self):
        mock_json = {
            "title": "test"
        }
        save_to_json(mock_json, "test")
        try:
            test_file = open(f"{os.getcwd()}/results/test.json", "r")
            w = json.load(test_file)
            self.assertDictEqual(mock_json, w)
            test_file.close()
        finally:
            os.remove(f"{os.getcwd()}/results/test.json")


if __name__ == '__main__':
    unittest.main()
