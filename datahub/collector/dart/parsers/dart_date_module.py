from datetime import datetime
import pytz


class DartDateModule():
    def __init__(self) -> None:
        self.date_format = "%Y%m%d"
        self.default_date = 2015

    def get_date_default(self) -> str:
        return self.default_date

    def get_date_now(self) -> str:
        return datetime.now().year

    # DART API 의 rcept_no를 파싱해서 datetime object로 돌려주는 함수
    def to_datetime(self, datestr: str):
        return datetime.strptime(datestr[:8], self.date_format).astimezone(pytz.UTC)


dart_date = DartDateModule()
