from datetime import datetime
from typing import Optional


def parse_log_row(text: str):
    """
    ログ1行をパースする
    :param text:
    :return:
    """
    fields = text.split(",")

    date = datetime.strptime(fields[0], "%Y%m%d%H%M%S")
    ip_addr = fields[1]
    res_ms = int(fields[2]) if fields[2] != "-" else None

    return WatchLog(date, ip_addr, res_ms)


class WatchLog:
    def __init__(self, timestamp: datetime, ip_address: str, res_ms: Optional[int]):
        self._timestamp = timestamp
        self._ip_address = ip_address
        self._res_ms = res_ms

    def __repr__(self):
        return f"{self._timestamp.strftime('%Y/%m/%d %H:%M:%S')}, {self._ip_address}, {self._res_ms}"

    def is_timeout(self) -> bool:
        return self._res_ms is None

    @property
    def ip_address(self) -> str:
        return self._ip_address

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    @property
    def res_ms(self) -> int:
        return self._res_ms
