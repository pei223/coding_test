from typing import Tuple
from datetime import datetime


def parse_ip_address(ip_address_str: str) -> Tuple[str, str]:
    """
    IPアドレス文字列をネットワーク部とホスト部にパースする
    :param ip_address_str:
    :return:
    """
    ip_address_and_prefix = ip_address_str.split("/")
    hex_str_ls = ip_address_and_prefix[0].split(".")
    network_prefix = int(ip_address_and_prefix[1])

    ip_address = 0
    for i, hex_str in enumerate(hex_str_ls):
        ip_address |= int(hex_str) << ((3 - i) * 8)

    host_int = ip_address & int("1" * (32 - network_prefix), 2)
    network_int = ip_address & (int("1" * network_prefix, 2) << (32 - network_prefix))

    network_str_ls, host_str_ls = [], []
    mask = 0b11111111
    for i in range(4):
        network_value = (network_int >> (3 - i) * 8) & mask
        host_value = (host_int >> (3 - i) * 8) & mask
        network_str_ls.append(str(network_value))
        host_str_ls.append(str(host_value))
    return ".".join(network_str_ls), ".".join(host_str_ls)


class SubNet:
    def __init__(self, network_part: str):
        self._network_part = network_part
        self._break_down_dict = {}
        self._all_break_down_start_time = None

    def add_host(self, host_part: str):
        self._break_down_dict[host_part] = False

    def break_down_host(self, host_part: str, timestamp: datetime):
        self._break_down_dict[host_part] = True
        if not self._all_break_down_start_time and self.is_all_break_down():
            self._all_break_down_start_time = timestamp

    def recover_host(self, host_part: str):
        self._break_down_dict[host_part] = False
        self._all_break_down_start_time = None

    def is_all_break_down(self) -> bool:
        return all(self._break_down_dict.values())

    @property
    def all_break_down_start_time(self) -> datetime:
        return self._all_break_down_start_time
