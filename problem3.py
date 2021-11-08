from app.log_reader.problem3 import LogReaderProblem3


def test_with_params(n: int, m: int, t: int):
    print(f"n={n}, m={m}, t={t}で実行")
    reader = LogReaderProblem3(n, m, t)
    with open("samples/problem3.txt", "r", encoding="utf-8") as file:
        for line in file:
            reader.read_line(line.replace("\n", ""))
        reader.output_currently_break_down_info()
        reader.output_currently_overload_info()
    print("\n\n\n\n")


if __name__ == '__main__':
    print("設問3. ")
    print("設問1と同じデータをN=1で実行")
    reader = LogReaderProblem3(n=1, m=3, t=60)
    with open("samples/problem1.txt", "r", encoding="utf-8") as file:
        for line in file:
            reader.read_line(line.replace("\n", ""))
        reader.output_currently_break_down_info()
    print("\n\n\n\n")

    print("設問2と同じデータをN=2で実行")
    reader = LogReaderProblem3(n=2, m=3, t=60)
    with open("samples/problem2.txt", "r", encoding="utf-8") as file:
        for line in file:
            reader.read_line(line.replace("\n", ""))
        reader.output_currently_break_down_info()
        reader.output_currently_overload_info()
    print("\n\n\n\n")

    test_with_params(n=2, m=2, t=20)
    test_with_params(n=3, m=2, t=20)
    test_with_params(n=2, m=2, t=30)
    test_with_params(n=2, m=3, t=20)
    test_with_params(n=2, m=3, t=30)
