from datetime import datetime, timedelta, timezone, tzinfo

utc = timezone.utc


class JST(tzinfo):
    def __repr__(self):
        return self.tzname(self)

    def utcoffset(self, dt):
        # ローカル時刻とUTCの差分に等しいtimedeltaを返す
        return timedelta(hours=9)

    def tzname(self, dt):
        # タイムゾーン名を返す
        return "Asia/Tokyo"

    def dst(self, dt):
        # 夏時間を返す。有効でない場合はtimedelta(0)を返す
        return timedelta(0)


def get_now() -> datetime:
    return datetime.now(JST())


def get_now_str(datetime: datetime = datetime.now(JST())) -> str:
    if not datetime.tzinfo:
        datetime.replace(tzinfo=JST())
    return datetime.strftime("%Y/%m/%d %H:%M:%S")
