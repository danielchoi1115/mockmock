from typing import Literal
from pydantic import BaseModel
import requests
from requests import HTTPError
from json.decoder import JSONDecodeError
import logging

from _global.configs import config

from ecos.parsers import ecos_date

log = logging.getLogger(__name__)


class EcosScraper(BaseModel):
    service_name: str = config.ecos.default_service_name
    auth_key: str
    req_type: str = config.ecos.default_req_type
    lang: str = config.ecos.default_lang
    req_start: str | int = 0
    req_end: str | int = 0
    stat_code: str = None
    period: Literal["A", "S", "Q", "M", "SM", "D"] = None
    date_start: str = None
    date_end: str = None
    item_code1: str = "?"
    item_code2: str = "?"
    item_code3: str = "?"
    item_code4: str = "?"
    total_count: int = 0

    def get_url(self):
        return f"https://ecos.bok.or.kr/api/{self.service_name}/{self.auth_key}/{self.req_type}/{self.lang}/{self.req_start}/{self.req_end}/{self.stat_code}/{self.period}/{self.date_start}/{self.date_end}/{self.item_code1}/{self.item_code2}/{self.item_code3}/{self.item_code4}"

    def get(self, url) -> dict:
        res = requests.get(url)
        try:
            data = res.json()
            if "RESULT" in data:
                raise HTTPError
            return data
        except HTTPError as ex:
            log.warning(f'''Failed to call ECOS API. URL: {url}, response: {data["RESULT"]}''')
        except (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.RequestException
        ) as ex:
            log.warning(ex)
        except JSONDecodeError:
            # handle error
            log.warning(f"Response is not a proper JSON. URL: {url}, response: {res.text[200]}")

    def set_date_start(self, date=None):
        if date is None:
            # If no parameter, set start date as default
            date = ecos_date.get_date_default(self.period)
        self.date_start = date

    def set_date_end(self, date=None):
        if date is None:
            date = ecos_date.get_date_now(self.period)
        self.date_end = date

    def set_time_range(self, start=None, end=None):
        self.set_date_start(start)
        self.set_date_end(end)

    def set_total_count(self):
        try:
            url = self.get_url()
            if data := self.get(url):
                total_count = data[self.service_name]["list_total_count"]
                self.total_count = int(total_count)
        except ValueError as ex:
            log.warning(f"total_count -> {total_count} <- is not an Integer. URL: {url}")

    def scrap(self):
        self.req_start = 1
        self.req_end = config.ecos.chunk_size

        while self.req_start < self.total_count:
            yield self.get(self.get_url())

            self.req_start = self.req_end + 1
            self.req_end += config.ecos.chunk_size
