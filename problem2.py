from app.log_reader.problem2 import LogReaderProblem2


def test_with_param(n: int):
    print(f"N={n}で実行")
    reader = LogReaderProblem2(n)
    with open("samples/problem2.txt", "r", encoding="utf-8") as file:
        for line in file:
            reader.read_line(line.replace("\n", ""))
        reader.output_currently_break_down_info()
    print("\n\n\n\n")


if __name__ == '__main__':
    print("設問2. ")
    print("設問1と同じデータをN=1で実行")
    reader = LogReaderProblem2(1)
    with open("samples/problem1.txt", "r", encoding="utf-8") as file:
        for line in file:
            reader.read_line(line.replace("\n", ""))
        reader.output_currently_break_down_info()
    print("\n\n\n\n")

    test_with_param(2)
    test_with_param(3)
    test_with_param(5)
    test_with_param(6)
