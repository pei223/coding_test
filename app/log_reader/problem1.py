from datetime import datetime
from typing import Dict

from .base import BaseLogReader
from ..watch_log import parse_log_row


class LogReaderProblem1(BaseLogReader):
    def __init__(self):
        # IPアドレスをキーとしてタイムアウト時間を保持
        self._timeout_timestamps: Dict[str, datetime] = {}

    def read_line(self, line: str):
        log = parse_log_row(line)
        if log.is_timeout():
            if not self._timeout_timestamps.get(log.ip_address):
                self._timeout_timestamps[log.ip_address] = log.timestamp
            return
        if self._timeout_timestamps.get(log.ip_address):
            print(self.to_break_down_term_text(log.ip_address, self._timeout_timestamps[log.ip_address],
                                               log.timestamp))
            del self._timeout_timestamps[log.ip_address]

    def output_currently_break_down_info(self):
        for key, value in self._timeout_timestamps.items():
            print(self.to_break_down_term_text(key, value, None))
