from datetime import datetime
from typing import Literal
import pytz


def validate_period(func):
    def wrapper(x, period):
        if period not in x.periods:
            pstring = ", ".join(x.periods)
            raise KeyError(f"period must be either one of {pstring}")
        return func(x, period)
    return wrapper


class ECOSDateModule():
    def __init__(self) -> None:
        self.periods = ["A", "S", "Q", "M", "SM", "D"]
        self.date_formats: dict[str, str] = {
            "A": "%Y",
            "S": "%YS1",
            "Q": "%YQ1",
            "M": "%Y%m",
            "SM": "%Y%mS1",
            "D": "%Y%m%d"
        }
        self.default_datestr: dict[str, str] = {
            "A": "1970",
            "S": "1970S1",
            "Q": "1970Q1",
            "M": "197001",
            "SM": "197001S1",
            "D": "19700101"
        }
        self.period_to_month_map = {
            "Q": {
                "1": "01",
                "2": "04",
                "3": "07",
                "4": "10"
            },
            "S": {
                "1": "01",
                "2": "07",
            },
            "SM": {
                "1": "01",
                "2": "16"
            }
        }

    @validate_period
    def get_date_default(self, period: Literal["A", "S", "Q", "M", "SM", "D"]) -> str:
        """_summary_
            1970년 01월 01일을 주기에 맞는 형식으로 리턴
        Args:
            주기(년:A, 반년:S, 분기:Q, 월:M, 반월:SM, 일: D)

        Returns:
            str: 1970, 1970S1, 1970Q1, 197001, 197001S1, or 19700101
        """

        return self.default_datestr[period]

    @validate_period
    def get_date_now(self, period: Literal["A", "S", "Q", "M", "SM", "D"]) -> str:
        """
            오늘 날짜를 주기에 맞는 형식으로 리턴

        Args:
            주기(년:A, 반년:S, 분기:Q, 월:M, 반월:SM, 일: D)

        Returns:
            str: (예시) 2015, 2015S1, 2015Q1, 201501, 201501S1, or 20150101
        """
        return datetime.now().strftime(self.date_formats[period])

    def to_datetime(self, datestr: str, period: Literal["A", "S", "Q", "M", "SM", "D"]):
        # if period is not in A, M, D, period needs to be converted to months
        if period not in ("A", "M", "D"):
            # get map
            converter = self.period_to_month_map.get(period)
            # Split the datestr "2017S1" -> ["2017", "1"]
            temp = datestr.split(period[0])
            # convert the period to month
            temp[1] = converter.get(temp[1])
            datestr = "".join(temp)
            # convert period type as well
            period = "D" if period == "SM" else "M"

        return datetime.strptime(datestr, self.date_formats[period]).astimezone(pytz.UTC).strftime("%Y-%m-%dT%H:%M:%S.000Z")


ecos_date = ECOSDateModule()
