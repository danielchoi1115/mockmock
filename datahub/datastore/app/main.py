from influxdb_client import Point
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, APIRouter, Request, Depends
from app.api.settings import get_settings, Settings
from app.api.api_v1 import api
from app.api.deps import close_influx_db


def get_application(settings: Settings = get_settings()) -> FastAPI:
    app = FastAPI(
        title="MockMock", openapi_url="/openapi.json"
    )
    root_router = APIRouter()

    app.include_router(api.api_router, prefix=settings.API_V1_STR)
    app.include_router(root_router)

    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            # allow_origin_regex=settings.BACKEND_CORS_ORIGIN_REGEX,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    return app


app = get_application()

if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    try:
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug", reload=True)
    except Exception as ex:
        print(ex)
    finally:
        close_influx_db()

# lchezZQGLQ8H_8LAfaWjXsGPuVWcXitr_4jGAw1lP6gM7Tvs3I-LHfdVeYRcOUNkkXEFFjEJnBelhzYLegCoeA==
# bucket = "test"


# {
#     "measurement": "h2o_feet",
#     "tags": {"location": "coyote_creek"},
#     "fields": {"water_level": 1.0},
#     "time": 1
# }

# points = []


# for data in dataset1["StatisticSearch"]["row"]:
#     p = Point(measurement_name="econ") \
#         .tag("stat_name", data["STAT_CODE"]) \
#         .tag("item_name", data["ITEM_CODE1"]) \
#         .field("value", float(data["DATA_VALUE"])) \
#         .time(datetime.strptime(data["TIME"], "%Y%m%d"))

#     points.append(p)

# gunicorn  -w 4 -k uvicorn.workers.UvicornWorker main:app