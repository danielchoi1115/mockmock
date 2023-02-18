from pydantic import BaseModel
from typing import Dict, Literal
from datetime import datetime
from enum import Enum
# Made from Influxdb-client.Point Module

DEFAULT_WRITE_PRECISION = "ns"


class Point(BaseModel):
    """
    Point defines the values that will be written to the influx database.

    Ref: https://docs.influxdata.com/influxdb/latest/reference/key-concepts/data-elements/#point
    """
    measurement: str
    tags: Dict = {}
    fields: Dict = {}
    time: datetime | None = None
    write_precision: Literal["ms", "s", "us", "ns"] = "ns"

    @staticmethod
    def setMeasurement(measurement):
        """Create a new Point with specified measurement name."""
        return Point(measurement=measurement)

    def setTime(self, time, write_precision=None):
        if write_precision is not None:
            self.write_precision = write_precision
        self.time = time
        return self

    def setTag(self, key, value):
        """Add tag with key and value."""
        self.tags[key] = value
        return self

    def setField(self, field, value):
        """Add field with key and value."""
        self.fields[field] = value
        return self
