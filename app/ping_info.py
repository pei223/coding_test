from datetime import datetime


class TimeoutCountInfo:
    def __init__(self, timestamp: datetime):
        self._timestamp = timestamp
        self._count = 1

    def increment(self):
        self._count += 1

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    @property
    def count(self) -> int:
        return self._count


class PingResInfo:
    def __init__(self, remember_len: int, res_time: int):
        self._remember_len = remember_len
        self._res_list = [res_time, ]
        self._avg_ms = res_time

    def add(self, res_time):
        self._res_list.append(res_time)
        if len(self._res_list) > self._remember_len:
            self._res_list.pop(0)
        self._avg_ms = sum(self._res_list) / len(self._res_list)

    def is_accumulated(self):
        """
        応答ログが保持上限までたまった場合はtrue、そうでなければfalseを返す
        :return:
        """
        return len(self._res_list) >= self._remember_len

    def average_res_time(self):
        return self._avg_ms

    def clear(self):
        self._res_list.clear()
