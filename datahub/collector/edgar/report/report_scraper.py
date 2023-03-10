import requests
from pydantic import BaseModel
from typing import List
from _global.configs import config
from edgar.accession import AccessionDto
import time
import logging

log = logging.getLogger(__name__)

class ReportScraper(BaseModel):
    scraped_data: List = []
    url: str = None

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

    def set_url(self, adsh: str):
        reportId = adsh.replace("-", "")
        filename = adsh
        self.url = config.edgar.ARCHIVE_URL_TEMPLATE.substitute(reportId=reportId, filename=filename)

    def scrap(self, accessionDto: AccessionDto):
        for accession in accessionDto.accessions:
            headers = config.edgar.REQUEST_HEADERS
            self.set_url(accession.adsh)
            data = self.get(self.url, headers=headers)
            self.scraped_data.append(data)
            time.sleep(0.2)

    def clear_data(self):
        self.scraped_data = None


reportScraper = ReportScraper()
