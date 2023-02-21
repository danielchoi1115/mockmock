import ast
from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime
from .dart_date_module import dart_date
from error_handlers import err_handler, ParseErrorDto
from configs import config


class DartParser(BaseModel):
    symbol: str
    parsed_data: List[Dict] | None = None
    headers = ['open', 'high', 'low', 'close', 'volume', 'foreigner_rate']

    def parse(self, data: str):
        if data == []:
            return
        try:
            data = ast.literal_eval(data.strip())
            self.parsed_data = [
                {
                    "measurement": config.INFLUXDB_MEASUREMENT,
                    "tags": {"symbol": self.symbol},
                    "fields": {  # foreigner_rate 가 없는 데이터도 있음
                        h: row[i+1]
                        for i, h in enumerate(self.headers) if i+1 < len(row)
                    },
                    "time": dart_date.to_datetime(row[0])
                } for row in data[1:]
            ]

        except KeyError as e:
            raise ValueError(f"Missing key in raw data: {e}") from e

        except Exception as ex:
            err_handler.send_error(ParseErrorDto(
                exception=str(ex),
                data=str(data)[:100]
            ))

    def clear_data(self):
        self.parsed_data.clear()
        self.parsed_data = None
