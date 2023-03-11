from typing import List, Dict
from seleniumwire import webdriver
from seleniumwire.utils import decode
from seleniumwire.request import Response
import json
from json import JSONDecodeError
from _global import utils
from _global.configs import config
from edgar.configs import Company
from pydantic import BaseModel
from datetime import datetime
import time


class AccessionScraper(BaseModel):
    driver: webdriver.Chrome = None
    results: List | None = []
    url: str | None = None

    def setDriver(self):
        if self.driver is None:
            self.driver = utils.get_webdriver()

    def setUrl(self, company: Company):
        self.url = config.edgar.SEARCH_URL_TEMPLATE.substitute(ciks=company.ciks, entity=company.entity)

    def scrap(self, page=1):
        """
        Scrap data recursively over the pagenations.
        We have data at response['hits']['hits']
            Example Response:
            response = {
                "took": 164,
                "timed_out": False,
                "_shards": {...},
                "hits": {
                    "total": {...},
                    "max_score": None,
                    "hits": [data1, data2, ...]
                }
            }
        Args:
            url (_type_): _description_
            page (int, optional): _description_. Defaults to 1.
        """
        paged_url = f"{self.url}&page={page}" if page > 1 else self.url

        self.driver.get(url=paged_url)
        time.sleep(2)

        decoded = None
        for request in self.driver.requests:
            if request.response and request.url == config.edgar.ACCESSION_XHR_KEYWORD:
                decoded = self.decode_respose(request.response)
                break
        # raise error if no result
        if not decoded:
            return

        # if time out, log url and time and retry after sime time
        if decoded.get("timed_out") == True:
            print(f"timeout error at url {paged_url} at {datetime.now()}")

        # if record exists, append it to the hits
        self.results.append(decoded)

        total_count = decoded.get("hits")["total"]["value"]
        if total_count > page*100:
            self.driver.backend.storage.clear_requests()
            self.scrap(page=page+1)

    def decode_respose(self, response: Response) -> Dict | None:
        encoding = response.headers.get('Content-Encoding', 'identity')
        try:
            result = response.body
            if encoding in config.edgar.encoding_types:
                result = decode(result, encoding).decode("utf-8")
            return json.loads(result)
        except JSONDecodeError as e:
            print(result)
            raise JSONDecodeError("body cannot be deserialized") from e

        except ValueError as e:
            raise ValueError(f"ValueError if the data could not be decoded from encoding {encoding}") from e

    class Config:
        arbitrary_types_allowed = True


accessionScraper = AccessionScraper()
