from pydantic import AnyHttpUrl, BaseSettings, validator
from typing import List, Union
from functools import lru_cache


class Settings(BaseSettings):  # 1
    API_V1_STR: str = "/api/v1"  # 2
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",
        "http://localhost:8001",  # type: ignore
        "https://fastapi-recipe-app.herokuapp.com"
    ]

    @validator("BACKEND_CORS_ORIGINS", pre=True)  # 3
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    ALGORITHM: str = "HS256"

    INFLUX_TOKEN = "lchezZQGLQ8H_8LAfaWjXsGPuVWcXitr_4jGAw1lP6gM7Tvs3I-LHfdVeYRcOUNkkXEFFjEJnBelhzYLegCoeA=="
    # Store the URL of your InfluxDB instance
    INFLUX_URL = "http://localhost:8086"
    INFLUX_ORG = "primary"
    class Config:
        case_sensitive = True  # 4


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
