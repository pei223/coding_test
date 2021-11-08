from datetime import datetime
from typing import Dict, List, Optional

from .base import BaseLogReader
from ..ping_info import TimeoutCountInfo, PingResInfo
from ..subnet import SubNet, parse_ip_address
from ..watch_log import parse_log_row, WatchLog


class LogReaderProblem4(BaseLogReader):
    def __init__(self, n: int, m: int, t: int, ip_address_list: List[str]):
        self._n = n
        self._m = m
        self._t = t
        # IPアドレスをキーとしてタイムアウト時間・回数を保持
        self._timeout_info_dict: Dict[str, TimeoutCountInfo] = {}
        # IPアドレスをキーとして過負荷によるタイムアウト開始時間を保持
        self._overload_timestamp_dict: Dict[str, datetime] = {}
        # IPアドレスをキーとしてPing応答時間を記憶
        self._ping_info_dict: Dict[str, PingResInfo] = {}
        # サブネットのIPアドレスをキーとしてサブネット内の故障状態を記憶
        self._subnet_breakdown_dict: Dict[str, SubNet] = {}
        for ip_address in ip_address_list:
            network, host = parse_ip_address(ip_address)
            if self._subnet_breakdown_dict.get(network):
                self._subnet_breakdown_dict[network].add_host(host)
                continue
            self._subnet_breakdown_dict[network] = SubNet(network)

    def read_line(self, line: str):
        log = parse_log_row(line)
        if log.is_timeout():
            self._save_timeout_info(log)
            network, host = parse_ip_address(log.ip_address)
            self._subnet_breakdown_dict[network].break_down_host(host, log.timestamp)
            # 過負荷中にタイムアウトが起きたら現時点までの過負荷期間を出力する
            if self._overload_timestamp_dict.get(log.ip_address):
                print(self.to_overload_term_text(log.ip_address, self._overload_timestamp_dict[log.ip_address],
                                                 log.timestamp))
                del self._overload_timestamp_dict[log.ip_address]
                self._ping_info_dict[log.ip_address].clear() if self._ping_info_dict.get(log.ip_address) else None
            return

        network, host = parse_ip_address(log.ip_address)
        if self._timeout_info_dict.get(log.ip_address):
            if self._timeout_info_dict[log.ip_address].count >= self._n:
                print(self.to_break_down_term_text(log.ip_address,
                                                   self._timeout_info_dict[log.ip_address].timestamp,
                                                   log.timestamp))
                if self._subnet_breakdown_dict[network].is_all_break_down():
                    print(self.to_subnet_break_down_term_text(network, self._subnet_breakdown_dict[
                        network].all_break_down_start_time, log.timestamp))
            del self._timeout_info_dict[log.ip_address]

        self._subnet_breakdown_dict[network].recover_host(host)
        self._save_ping_info(log)
        # m回応答を受けていない場合は一律過負荷と見なさない
        if not self._ping_info_dict[log.ip_address].is_accumulated():
            return
        if self._overload_timestamp_dict.get(log.ip_address):
            if self._ping_info_dict[log.ip_address].average_res_time() < self._t:
                print(self.to_overload_term_text(log.ip_address,
                                                 self._overload_timestamp_dict[log.ip_address],
                                                 log.timestamp))
                del self._overload_timestamp_dict[log.ip_address]
            return
        if self._ping_info_dict[log.ip_address].average_res_time() >= self._t:
            self._overload_timestamp_dict[log.ip_address] = log.timestamp

    def output_currently_break_down_info(self):
        for key, value in self._timeout_info_dict.items():
            print(self.to_break_down_term_text(key, value.timestamp, None))

    def output_currently_overload_info(self):
        for key, value in self._overload_timestamp_dict.items():
            print(self.to_overload_term_text(key, value, None))

    def output_currently_subnet_break_down_info(self):
        for key, value in self._subnet_breakdown_dict.items():
            if value.is_all_break_down():
                print(self.to_subnet_break_down_term_text(key, value.all_break_down_start_time, None))

    def to_subnet_break_down_term_text(self, ip_address: str, start: datetime, end: Optional[datetime]):
        return f"[subnet故障]\t{ip_address}\t: {start.strftime('%Y%m%d%H%M%S')} ~ {end.strftime('%Y%m%d%H%M%S') if end else ''}"

    def _save_timeout_info(self, log: WatchLog):
        if not self._timeout_info_dict.get(log.ip_address):
            self._timeout_info_dict[log.ip_address] = TimeoutCountInfo(log.timestamp)
            return
        self._timeout_info_dict[log.ip_address].increment()

    def _save_ping_info(self, log: WatchLog):
        if not self._ping_info_dict.get(log.ip_address):
            self._ping_info_dict[log.ip_address] = PingResInfo(self._m, log.res_ms)
        else:
            self._ping_info_dict[log.ip_address].add(log.res_ms)
