from typing import List, Dict
from influxdb_client import WriteApi, QueryApi
from fastapi import Depends
from influxdb_client.client.flux_table import FluxStructureEncoder
import json


class CRUDinflux():
    def create(
        self,
        write_api: WriteApi,
        bucket: str,
        org: str,
        points: List[Dict]
    ):
        try:
            write_api.write(bucket=bucket, org=org, record=points)
            return {"result": True}
        except Exception as ex:
            print(ex)
            return {"result": False}

    def read(
        self,
        query_api: QueryApi,
        org: str,
        query: str
    ):
        try:
            results = query_api.query(org=org, query=query)
            output = json.dumps(results, cls=FluxStructureEncoder)
            return {"result": output}
        except Exception as ex:
            print(ex)
            return {"result": False}


influx = CRUDinflux()
