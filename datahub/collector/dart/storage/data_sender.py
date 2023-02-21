
import requests
from pydantic import BaseModel
from _global.configs import config


class DataSender(BaseModel):
    url: str = config.INFLUXDB_API_URL
    dbconfig: str = {
        "bucket": config.INFLUXDB_BUCKET,
        "org": config.INFLUXDB_ORG
    }

    def send(self, data):
        response = requests.post(
            self.url,
            params=self.dbconfig,
            json=data
        )
        if response.status_code in (200, 201):
            return "Successful post request with status code:", response.status_code
        else:
            return "Failed post request with status code:", response.status_code


sender = DataSender()
