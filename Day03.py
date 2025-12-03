sum_volt2 = 0
sum_volt12 = 0

def max_voltage2(line):
    first_dig_i = 0
    second_dig_i = len(line) - 1
    num = lambda f,s : int(line[f] + line[s])

    curr_num = num(first_dig_i, second_dig_i)
    for i in range(1, second_dig_i):
        if num(i, second_dig_i) > curr_num:
            first_dig_i = i
            curr_num = num(i, second_dig_i)
    
    for i in range(second_dig_i - 1, first_dig_i, -1):
        if num(first_dig_i, i) > curr_num:
            second_dig_i = i
            curr_num = num(first_dig_i, i)

    return curr_num

def max_voltage12(line):
    line_end = len(line)
    digits = [ line_end - i for i in range(12, 0, -1)]

    limit = -1
    for i, digit in enumerate(digits):
        new_index = digit
        max_value = line[digit]
        for j in range(digit - 1, limit, -1):
            if line[j] >= max_value:
                max_value = line[j]
                new_index = j
        digits[i] = new_index
        limit = new_index

    result = 0
    for i, digit in enumerate(digits):
        result += int(line[digit]) * 10 ** (11 - i)

    return result

with open('inputs/03.txt', 'r') as file:
    for y, line in enumerate(file):
        line = line.rstrip()
        sum_volt2 += max_voltage2(line)
        sum_volt12 += max_voltage12(line)

print(f"Part 1: {sum_volt2}")
print(f"Part 2: {sum_volt12}")
