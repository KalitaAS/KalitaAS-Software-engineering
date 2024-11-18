def read_file():
    with open("./HW1 V8/third_task.txt", encoding="utf-8") as file:
        lines = file.readlines()
        table = []
        for line in lines:
            words = line.strip().split(" ")
            table.append(words)
    return table


def fill_na(table):
    for i in range(len(table)):
        for j in range(len(table[i])):
            if table[i][j] == 'N/A':
                table[i][j] = (int(table[i][j-1]) + int(table[i][j+1])) / 2
            else:
                table[i][j] = int(table[i][j])
    return table


def filter_multiples_7(table):
    filtered_table = []
    for row in table:
        filtered_row = [num for num in row if num % 7 == 0]
        filtered_table.append(filtered_row)
    return filtered_table


def write_to_file(table, filename="third_task_result.txt"):
    with open(filename, "w", encoding="utf-8") as file:
        for row in table:
            file.write(" ".join(map(str, row)) + "\n")


raw_table = read_file()
filled_table = fill_na(raw_table)  
filtered_table = filter_multiples_7(filled_table)
write_to_file(filtered_table)
