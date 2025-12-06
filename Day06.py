n_rows = []
ops = []

with open('inputs/06.txt', 'r') as file:
    for y, line in enumerate(file):
        line = line.rstrip()

        elements = line.split()

        if y == 4:
            ops = elements
        else:
            n_row = [int(e) for e in elements]
            n_rows.append(n_row)

    result = 0
    for i, op in enumerate(ops):
        if op == '+':
            for j in range(len(n_rows)):
                result += n_rows[j][i]
        if op == '*':
            k = 1
            for j in range(len(n_rows)):
                k *= n_rows[j][i]
            result += k

print(f"Part 1: {result}")

lines = []
with open('inputs/06.txt', 'r') as file:
    for y, line in enumerate(file):
        lines.append(line[:-1])

result = 0
ops_row = 4
cur_ops = ''
col_result = 0
for i in range(len(lines[0])):
    number = 0
    for j in range(ops_row):
        if lines[j][i] != ' ':
            number *= 10
            number += int(lines[j][i])
    if number == 0:
        result += col_result
        col_result = 0
        continue 

    if lines[ops_row][i] == '+':
        cur_ops = '+'
    if lines[ops_row][i] == '*':
        cur_ops = '*'
        col_result = 1
    
    if cur_ops == '+':
        result += number
    if cur_ops == '*':
        col_result *= number
    
result += col_result


print(f"Part 2: {result}")