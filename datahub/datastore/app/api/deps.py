
from influxdb_client.client.write_api import SYNCHRONOUS
import influxdb_client
from app.api.settings import settings

client = influxdb_client.InfluxDBClient(
    url=settings.INFLUX_URL,
    token=settings.INFLUX_TOKEN,
    org=settings.INFLUX_ORG
)


def get_influx_writeapi():
    return client.write_api(write_options=SYNCHRONOUS)


def get_influx_queryapi():
    return client.query_api()


def close_influx_db():
    client.close()
