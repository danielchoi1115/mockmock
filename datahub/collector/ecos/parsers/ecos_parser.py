from typing import Dict, List
from ecos.parsers.ecos_date_module import ecos_date
from pydantic import BaseModel
from _global.configs import config
from _global.dto import Point
import logging

log = logging.getLogger(__name__)


class EcosParser(BaseModel):
    parsed_data: List[Dict] | None = None
    period: str

    def parse(self, data: List[Dict]):
        if not data:
            log.warning(f'Item not found. Data: {data}')
            return

        try:
            self.parsed_data = [
                self.make_point(item)
                for item in data["StatisticSearch"]["row"]
            ]
        except KeyError as e:
            log.warning(f"Missing key in raw data: {e}")

        except Exception as ex:
            log.warning(f'Error while creating Point: {ex}. Symbol: {str(data["StatisticSearch"]["row"])[:100]}')

    def make_point(self, item):
        return Point.setMeasurement(config.influxdb.measurement.ECON)          \
                    .setTime(ecos_date.to_datetime(item["TIME"], self.period)) \
                    .setTag("stat_code", item["STAT_CODE"])                    \
                    .setTag("item_code", item["ITEM_CODE1"])                   \
                    .setField("value", float(item["DATA_VALUE"]))              \
                    .dict()

    def clear_data(self):
        self.parsed_data.clear()
