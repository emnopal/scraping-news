import os
import json
import unittest
from scraping_bs4 import Scraping


class TestScrapingBS4(unittest.TestCase):

    def setUp(self) -> None:
        self.scraping = Scraping()
        self.url = "https://news.detik.com/indeks"

    def test_get_urls_today(self):
        self.assertIsNotNone(
            self.scraping.get_urls(self.url, is_pagination=False))
        self.assertIsInstance(
            self.scraping.get_urls(self.url, is_pagination=False), list)

    def test_get_urls_desired_time(self):
        self.assertIsNotNone(
            self.scraping.get_urls(self.url, is_pagination=False, date_of_news="12/12/2021"))
        self.assertIsInstance(
            self.scraping.get_urls(self.url, is_pagination=False, date_of_news="12/12/2021"), list)

    def test_get_urls_today_pagination(self):
        self.assertIsNotNone(
            self.scraping.get_urls(self.url, is_pagination=True))
        self.assertIsInstance(
            self.scraping.get_urls(self.url, is_pagination=True), list)

    def test_get_urls_desired_time_pagination(self):
        self.assertIsNotNone(
            self.scraping.get_urls(self.url, is_pagination=True, date_of_news="12/12/2021"))
        self.assertIsInstance(
            self.scraping.get_urls(self.url, is_pagination=True, date_of_news="12/12/2021"), list)

    def test_get_news_today(self):
        self.assertIsNotNone(
            self.scraping.get_news_content(self.url, is_pagination=False))
        self.assertIsInstance(
            self.scraping.get_news_content(self.url, is_pagination=False), dict)

    def test_get_news_desired_time(self):
        self.assertIsNotNone(
            self.scraping.get_news_content(self.url, is_pagination=False, date_of_news="12/12/2021"))
        self.assertIsInstance(
            self.scraping.get_news_content(self.url, is_pagination=False, date_of_news="12/12/2021"), dict)

    def test_get_news_today_pagination(self):
        self.assertIsNotNone(
            self.scraping.get_news_content(self.url, is_pagination=True))
        self.assertIsInstance(
            self.scraping.get_news_content(self.url, is_pagination=True), dict)

    def test_get_news_desired_time_pagination(self):
        self.assertIsNotNone(
            self.scraping.get_news_content(self.url, is_pagination=True, date_of_news="12/12/2021"))
        self.assertIsInstance(
            self.scraping.get_news_content(self.url, is_pagination=True, date_of_news="12/12/2021"), dict)

    def test_json_write(self):
        mock_json = {
            "title": "test"
        }
        self.scraping.save_to_json(mock_json, "test")
        try:
            test_file = open(f"{os.getcwd()}/results/test.json", "r")
            w = json.load(test_file)
            self.assertDictEqual(mock_json, w)
            test_file.close()
        finally:
            os.remove(f"{os.getcwd()}/results/test.json")


if __name__ == '__main__':
    unittest.main()
