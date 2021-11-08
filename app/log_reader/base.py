from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import Optional


class BaseLogReader(metaclass=ABCMeta):
    @abstractmethod
    def read_line(self, line: str):
        pass

    def to_break_down_term_text(self, ip_address: str, start: datetime, end: Optional[datetime]):
        return f"[故障]\t\t\t{ip_address}\t: {start.strftime('%Y%m%d%H%M%S')} ~ {end.strftime('%Y%m%d%H%M%S') if end else ''}"

    def to_overload_term_text(self, ip_address: str, start: datetime, end: Optional[datetime]):
        return f"[過負荷]\t\t{ip_address}\t: {start.strftime('%Y%m%d%H%M%S')} ~ {end.strftime('%Y%m%d%H%M%S') if end else ''}"

    def output_currently_break_down_info(self):
        pass

    def output_currently_overload_info(self):
        pass
