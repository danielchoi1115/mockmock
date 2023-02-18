
import requests
from pydantic import BaseModel
from typing import Any
from _global.configs import config


class DataSender(BaseModel):
    url: str = config.influxdb.API_URL
    org: str = config.influxdb.ORG

    def send(self, bucket: str, data: Any):
        dbconfig = {
            "bucket": bucket,
            "org": self.org
        }
        response = requests.post(
            self.url,
            params=dbconfig,
            json=data
        )
        if response.status_code in {200, 201}:
            return "Successful post request with status code:", response.status_code
        else:
            return "Failed post request with status code:", response.status_code

dataSender = DataSender()