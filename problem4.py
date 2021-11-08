from app.log_reader.problem4 import LogReaderProblem4


def test_with_params(n: int, m: int, t: int):
    print(f"n={n}, m={m}, t={t}で実行")
    reader = LogReaderProblem4(n, m, t, ip_address_list=[
        "10.20.30.1/24",
        "10.20.30.2/24",
        "10.20.31.1/24",
        "10.20.31.2/24",
        "10.20.31.3/24",
        "192.168.0.1/16",
        "192.168.2.1/16",
        "192.170.0.1/16",
        "192.170.0.2/16",
    ])
    with open("samples/problem4.txt", "r", encoding="utf-8") as file:
        for line in file:
            reader.read_line(line.replace("\n", ""))
        reader.output_currently_break_down_info()
        reader.output_currently_overload_info()
        reader.output_currently_subnet_break_down_info()
    print("\n\n\n\n")


if __name__ == '__main__':
    print("設問3. ")
    ip_address_list = [
        "10.20.30.1/16",
        "10.20.30.2/16",
        "10.20.30.3/16",
        "10.20.30.4/16",
        "10.20.30.5/16",
        "192.168.1.1/24",
        "192.168.1.2/24",
        "192.168.1.3/24",
        "192.168.1.4/24",
        "192.168.2.1/24",
        "192.168.2.2/24",
        "192.168.2.3/24",
        "192.168.2.4/24",
    ]
    print("設問1と同じデータをN=1で実行")
    reader = LogReaderProblem4(n=1, m=3, t=60, ip_address_list=ip_address_list)
    with open("samples/problem1.txt", "r", encoding="utf-8") as file:
        for line in file:
            reader.read_line(line.replace("\n", ""))
        reader.output_currently_break_down_info()
    print("\n\n\n\n")

    print("設問2と同じデータをN=2で実行")
    reader = LogReaderProblem4(n=2, m=3, t=60, ip_address_list=ip_address_list)
    with open("samples/problem2.txt", "r", encoding="utf-8") as file:
        for line in file:
            reader.read_line(line.replace("\n", ""))
        reader.output_currently_break_down_info()
        reader.output_currently_overload_info()
    print("\n\n\n\n")

    print("設問3と同じデータをN=2, m=2, t=20で実行")
    reader = LogReaderProblem4(n=2, m=2, t=20, ip_address_list=ip_address_list)
    with open("samples/problem3.txt", "r", encoding="utf-8") as file:
        for line in file:
            reader.read_line(line.replace("\n", ""))
        reader.output_currently_break_down_info()
        reader.output_currently_overload_info()
    print("\n\n\n\n")

    test_with_params(n=2, m=2, t=20)
    test_with_params(n=3, m=2, t=30)
