from fastapi import APIRouter, Depends, status
from app import dto
from app import crud
from influxdb_client import WriteApi
from typing import List
from app.api.settings import settings
from app.api import deps
router = APIRouter()


@router.post("/point", status_code=status.HTTP_201_CREATED)
async def create_points(
    bucket: str,
    points: List[dto.PointDto],
    org: str = settings.INFLUX_ORG,
    write_api: WriteApi = Depends(deps.get_influx_writeapi)
) -> dict:
    points_obj = [p.dict() for p in points]
    return crud.influx.create(
        write_api=write_api,
        bucket=bucket,
        org=org,
        points=points_obj
    )


@router.post("/query", status_code=status.HTTP_200_OK)
async def read_points(
    query_obj: dto.QueryDto,
    org: str = settings.INFLUX_ORG,
    query_api: WriteApi = Depends(deps.get_influx_queryapi)
) -> dict:

    return crud.influx.read(
        query_api=query_api,
        org=org,
        query=query_obj.query
    )
