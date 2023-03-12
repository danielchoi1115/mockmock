from typing import List, Dict
from seleniumwire import webdriver
from seleniumwire.utils import decode
from seleniumwire.request import Response
import json
from json import JSONDecodeError
from _global import utils
from _global.configs import config

from pydantic import BaseModel
from datetime import datetime
import time


class CompanyNameScraper(BaseModel):
    driver: webdriver.Chrome = None
    results: Dict | None = {}
    url: str | None = None

    def setDriver(self):
        if self.driver is None:
            self.driver = utils.get_webdriver()

    def setUrl(self, tickers: str):
        self.url = config.yahoo.COMPANY_NAME_BY_TICKER_URL.substitute(tickers)

    def scrap(self):
        ...
        self.driver.get(url=self.url)
        time.sleep(1)

        for request in self.driver.requests:
            ...
            
    class Config:
        arbitrary_types_allowed = True


companyNameScraper = CompanyNameScraper()
