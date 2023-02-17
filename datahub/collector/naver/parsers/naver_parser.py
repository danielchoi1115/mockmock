import ast
from pydantic import BaseModel
from typing import List, Dict
from .naver_date_module import naver_date
import logging
from _global.configs import config
from _global.dto import Point

log = logging.getLogger(__name__)


class NaverParser(BaseModel):
    symbol: str
    parsed_data: List[Dict] | None = None
    header_map: Dict = {
        '시가': 'open',
        '고가': 'high',
        '저가': 'low',
        '종가': 'close',
        '거래량': 'volume',
        '외국인소진율': 'foreigner_rate'
    }
    headers: List[str] | None = None
    
    def set_headers(self, headers: List[str]):
        self.headers = [
            self.header_map[h] 
            for h in headers
            if h in self.header_map
        ]
    
    def parse(self, data: str):
        if not data:
            log.warning(f'Item not found. Symbol: {self.symbol}')
            return
        try:
            data = ast.literal_eval(data.strip())
            self.set_headers(data[0])
            self.parsed_data = [
                self.make_point(row)
                for row in data[1:]
            ]

        except KeyError as ex:
            log.warning(f'Failed to parse. Missing Key {ex}. Symbol: {self.symbol}')

        except Exception as ex:
            log.warning(f'Error while creating Point: {ex}. Symbol: {self.symbol}')

    def make_point(self, row):
        p = Point.setMeasurement(config.influxdb.measurement.STOCK) \
                    .setTime(naver_date.to_datetime(row[0]))           \
                    .setTag("symbol", self.symbol)
        for i, header in enumerate(self.headers):
            if i >= len(row)-1: break
            p = p.setField(header, row[i+1])
        return p.dict()

    def clear_data(self):
        self.parsed_data.clear()
        self.parsed_data = None
