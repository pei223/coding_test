from typing import Dict

from .base import BaseLogReader
from ..ping_info import TimeoutCountInfo
from ..watch_log import parse_log_row, WatchLog


class LogReaderProblem2(BaseLogReader):
    def __init__(self, n: int):
        self._n = n
        # IPアドレスをキーとしてタイムアウト時間・回数を保持
        self._timeout_info_dict: Dict[str, TimeoutCountInfo] = {}

    def read_line(self, line: str):
        log = parse_log_row(line)
        if log.is_timeout():
            self._save_timeout_info(log)
            return

        if not self._timeout_info_dict.get(log.ip_address):
            return
        if self._timeout_info_dict[log.ip_address].count >= self._n:
            print(self.to_break_down_term_text(log.ip_address,
                                               self._timeout_info_dict[log.ip_address].timestamp,
                                               log.timestamp))
        del self._timeout_info_dict[log.ip_address]

    def output_currently_break_down_info(self):
        for key, value in self._timeout_info_dict.items():
            print(self.to_break_down_term_text(key, value.timestamp, None))

    def _save_timeout_info(self, log: WatchLog):
        if not self._timeout_info_dict.get(log.ip_address):
            self._timeout_info_dict[log.ip_address] = TimeoutCountInfo(log.timestamp)
            return
        self._timeout_info_dict[log.ip_address].increment()
