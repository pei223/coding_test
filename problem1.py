from app.log_reader.problem1 import LogReaderProblem1

if __name__ == '__main__':
    reader = LogReaderProblem1()
    print("設問1. ")
    with open("samples/problem1.txt", "r", encoding="utf-8") as file:
        for line in file:
            reader.read_line(line.replace("\n", ""))
        reader.output_currently_break_down_info()
