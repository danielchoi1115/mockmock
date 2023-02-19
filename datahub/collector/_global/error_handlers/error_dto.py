from pydantic import BaseModel
from datetime import datetime
from typing import Any


class ErrorDto(BaseModel):
    time: datetime = datetime.now()


class ParseErrorDto(ErrorDto):
    exception: str
    traceback: str


class RequestErrorDto(ErrorDto):
    type: str = "Request Error"
    url: str
    exception: Any
    msg: Any


class ScrapErrorDto(ErrorDto):
    type: str = "Scrap Error"
    url: str
    status_code: int
    error_code: str
    msg: str
