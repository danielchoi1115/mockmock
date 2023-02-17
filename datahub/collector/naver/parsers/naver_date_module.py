from datetime import datetime
import pytz


class NaverDateModule():
    def __init__(self) -> None:
        self.date_format = "%Y%m%d"
        self.default_datestr = "19700101"

    def get_date_default(self) -> str:
        return self.default_datestr

    def get_date_now(self) -> str:
        return datetime.now().strftime(self.date_format)

    def to_datetime(self, datestr: str):
        date = datetime.strptime(datestr, self.date_format).astimezone(pytz.UTC)
        return date.strftime("%Y-%m-%dT%H:%M:%S.000Z")


naver_date = NaverDateModule()
