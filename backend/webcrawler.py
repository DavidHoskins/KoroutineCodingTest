import requests
import re
from bs4 import BeautifulSoup, ResultSet
import json
import asyncio
from time import sleep

class Webcrawler():
    def __init__(self, retry_limit: int, sleep_time: int, url: str, websocket: any):
        # Retry params for connection to urls
        self.retry_limit = retry_limit
        self.sleep_time = sleep_time

        self.unexplored_links = [url]
        self.confirmed_links = []
        self.websocket = websocket

    async def get_all_links_from_url(self) -> list[str]:
        while len(self.unexplored_links) > 0:
            url_to_check = self.unexplored_links[0]

            page_text_data = self.request_page_text_data(url=url_to_check)
            self.confirmed_links.append(url_to_check)

            current_page_links = self.parse_page_text_data_for_links(text_data=page_text_data, url=url_to_check)
            current_page_links = self.remove_if_already_exists(primary=self.confirmed_links, secondary=current_page_links)
            current_page_links = self.remove_duplicates(links=current_page_links)

            self.unexplored_links = self.append_if_unique(secondary=current_page_links, primary=self.unexplored_links)

            self.unexplored_links.pop(0)

            links_message = {"explored_urls": self.confirmed_links, "unexplored_urls": self.unexplored_links}
            await self.websocket.send(json.dumps(links_message))
            await asyncio.sleep(0.0) # Yields current process, to allow for multiple requests

        return self.confirmed_links
    
    def request_page_text_data(self, url: str) -> str:
        for i in range(self.retry_limit):
            try:
                request_data = requests.get(url=url)
                if request_data.status_code == 200:
                    return request_data.text
                else:
                    sleep(self.sleep_time)
            except requests.exceptions.ConnectionError:
                print("Error connecting to url check the url is valid and retry later")
        return ""

    def parse_page_text_data_for_links(self, text_data: str, url: str) -> ResultSet:
        soup = BeautifulSoup(text_data, 'html.parser')

        # Regex only allows where url matches protocol, subdomain & domain name, but allows any page paths & parameters
        parsed_links = soup.find_all(href=re.compile(f"^{url}*"))
        return [x.get("href") for x in parsed_links]

    # Returns the secondary list with all elements not found in the primary list
    def remove_if_already_exists(self, primary: list[str], secondary: list[str]) -> list[str]:
        return [x for x in secondary if x not in primary]
    
    # Returns the original array with all duplicates removed
    def remove_duplicates(self, links: list[str]) ->list[str]:
        # Converts list to dict, and back to list (dict's can only have unique keys so this removes dupes)
        return list(dict.fromkeys(links))

    # Returns the primary with all secondary elements not found in primary list.
    def append_if_unique(self, primary: list[str], secondary: list[str]) -> list[str]:
        elements_to_appent = self.remove_if_already_exists(primary=primary, secondary=secondary)
        return primary + elements_to_appent
