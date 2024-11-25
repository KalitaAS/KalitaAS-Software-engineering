def read_file():
    with open("./HW1 V8/second_task.txt", encoding="utf-8") as file:
        lines = file.readlines()
        table = []
        for line in lines:
            words = line.strip().split(" ")
            table.append(list(map(int, words)))
        return table


def first_operation(table):
    result = []
    for row in table:
        negate_count = 0    
        negate_sum = 0
        for num in row:
            if num < 0:
                negate_count += 1
                negate_sum += num
        result.append(negate_sum / negate_count)
    return result


def find_min_and_max(arr):
    min_val = arr[0]
    max_val = arr[0]

    for el in arr:
        if el < min_val:
            min_val = el
        if el > max_val:
            max_val = el
    return min_val, max_val


def write_to_file(column, min_val, max_val):
    with open("second_task_result.txt", "w", encoding="utf-8") as file:
        for num in column:
            file.write(f"{num}\n")
        file.write(f"\n{min_val}\n{max_val}\n")


table = read_file()
column = first_operation(table)
min_val, max_val = find_min_and_max(column)
write_to_file(column, min_val, max_val)
