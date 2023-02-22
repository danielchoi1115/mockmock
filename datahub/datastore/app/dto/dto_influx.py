from pydantic import BaseModel, Field
from typing import Dict, Optional, Any
from datetime import datetime


class PointDto(BaseModel):
    measurement: str
    tags: Optional[Dict[str, str]]
    fields: Dict[str, float]
    time: Any
    write_precision: str

    #     self._tags = {}
    # self._fields = {}
    # self._name = measurement_name
    # self._time = None
    # self._write_precision = DEFAULT_WRITE_PRECISION
    # self._field_types = {}


class QueryDto(BaseModel):
    query: str
