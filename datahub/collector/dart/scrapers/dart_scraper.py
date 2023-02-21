from typing import Dict, List
from pydantic import BaseModel
import requests
from requests import HTTPError
from parsers import dart_date
from json.decoder import JSONDecodeError
from configs import status, config
import itertools
# requestType이 2일 경우 count 값도 인수로 보내야 함.
# 데이터를 한 번 받은 뒤에 추가로 데이터를 요청할 때 쓰는 값인 듯 하다.


class DartScraper(BaseModel):
    corp_code: str
    report_codes = ["11013", "11012", "11014", "11011"]
    years: List[str]
    fs_div: str = "OFS"  # CFS:연결재무제표, OFS:재무제표

    def get(self, url, params) -> dict:
        try:
            res = requests.get(url, params=params)
            data = res.json()

            if data["status"] != status.DART_000_OK:
                err_handler.send_error(ApiErrorDto(
                    url=url,
                    error_code=data["status"],
                    error_msg=data["message"]
                ))
                return []

            return data["list"]
        except (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError,
            requests.exceptions.RequestException
        ) as ex:
            err_handler.send_error(RequestErrorDto(
                url=url,
                status_code=res.status_code,
                exception=str(type(ex).__name__),
                error_msg=str(ex)
            ))

    def set_time_range(self, start=None):
        if start is None:
            start = dart_date.get_date_default()
        end = dart_date.get_date_now()
        self.years = list(map(str, range(start, end+1)))

    def scrap(self):
        for year, reprt_code in itertools.product(self.years, self.report_codes):
            params = {
                "crtfc_key": config.DART_API_KEY,
                "corp_code": self.corp_code,
                "bsns_year": year,
                "reprt_code": reprt_code,
                "fs_div": self.fs_div
            }
            return self.get(
                url=config.DART_URL,
                params=params
            )
