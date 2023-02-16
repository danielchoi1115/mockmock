from typing import Literal
from pydantic import BaseModel
import requests
from requests import HTTPError
from naver.parsers import naver_date
from _global.configs import config
import logging
# requestType이 2일 경우 count 값도 인수로 보내야 함.
# 데이터를 한 번 받은 뒤에 추가로 데이터를 요청할 때 쓰는 값인 듯 하다.

log = logging.getLogger(__name__)

class NaverScraper(BaseModel):
    symbol: str
    requestType: int = 1
    startTime: str | None = None
    endTime: str | None = None
    timeframe: Literal["day", "week", "month"] = "day"
    scraped_data: str | None = None

    def get(self, url, headers=None, params=None) -> dict:
        try:
            res = requests.get(url, headers=headers, params=params)
            return res.text
        except (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError,
            requests.exceptions.RequestException
        ) as ex:
            log.warning(ex)

    def set_startTime(self, date=None):
        if date is None:
            # If no parameter, set start date as default
            date = naver_date.get_date_default()
        self.startTime = date

    def set_endTime(self, date=None):
        if date is None:
            date = naver_date.get_date_now()
        self.endTime = date

    def set_time_range(self, start=None, end=None):
        self.set_startTime(start)
        self.set_endTime(end)

    def scrap(self):
        params = {k: v for k, v in self.dict().items() if v is not None}
        headers = config.naver.NAVER_HEADERS
        self.scraped_data = self.get(config.naver.NAVER_URL, headers=headers, params=params)

    def clear_data(self):
        self.scraped_data = None
