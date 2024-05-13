import unittest
from unittest import mock
import webcrawler

import requests

class TestWebcrawler(unittest.IsolatedAsyncioTestCase):
    RETRY_COUNT = 3
    BACKOFF_TIME = 1

    def mocked_requests_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.text = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        if kwargs['url'] == 'test':
            return MockResponse("test", 200)

        return MockResponse(None, 404)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    async def test_upper(self, mock_get):
        message = "test"
        websocket = mock.AsyncMock()
        expected_results = ["test"]
        test_webcrawler = webcrawler.Webcrawler(self.RETRY_COUNT, self.BACKOFF_TIME, message, websocket)
        actual_results = await test_webcrawler.get_all_links_from_url()

        self.assertEqual(expected_results, actual_results)

    def test_append_if_unique(self):
        old_links = ["test", "test1", "test2"]
        new_links = ["test", "test3", "test-1"]
        expected_result = ["test", "test1", "test2", "test3", "test-1"]

        message = "test"
        websocket = mock.AsyncMock()
        test_webcrawler = webcrawler.Webcrawler(self.RETRY_COUNT, self.BACKOFF_TIME, message, websocket)

        result = test_webcrawler.append_if_unique(secondary=new_links, primary=old_links)
        self.assertEqual(expected_result, result)

    def test_remove_duplicates(self):
        array = ["test","test", "test1", "test2", "test"]
        expected_result = ["test", "test1", "test2"]

        message = "test"
        websocket = mock.AsyncMock()
        test_webcrawler = webcrawler.Webcrawler(self.RETRY_COUNT, self.BACKOFF_TIME, message, websocket)
        
        result = test_webcrawler.remove_duplicates(links=array)
        self.assertEqual(expected_result, result)

    def test_remove_if_already_exists(self):
        old_links = ["test", "test1", "test2"]
        new_links = ["test", "test3", "test-1"]
        expected_result = ["test3", "test-1"]

        message = "test"
        websocket = mock.AsyncMock()
        test_webcrawler = webcrawler.Webcrawler(self.RETRY_COUNT, self.BACKOFF_TIME, message, websocket)

        result = test_webcrawler.remove_if_already_exists(primary=old_links, secondary=new_links)
        self.assertEqual(expected_result, result)

    def test_parse_page_text_data_for_links(self):
        test_url = "test"
        test_html_data = "<a href='test'/> <a href='test'/> <a href='test'/>"
        expected_results = ["test", "test", "test"]

        message = "test"
        websocket = mock.AsyncMock()
        test_webcrawler = webcrawler.Webcrawler(self.RETRY_COUNT, self.BACKOFF_TIME, message, websocket)

        actual_results = test_webcrawler.parse_page_text_data_for_links(text_data=test_html_data, url=test_url)
        self.assertEqual(expected_results, actual_results)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_request_page_text_data(self, mock_get):
        test_url = "test"
        expected_results = "test"

        message = "test"
        websocket = mock.AsyncMock()
        test_webcrawler = webcrawler.Webcrawler(self.RETRY_COUNT, self.BACKOFF_TIME, message, websocket)

        actual_results = test_webcrawler.request_page_text_data(url=test_url)
        self.assertEqual(expected_results, actual_results)