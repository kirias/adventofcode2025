rows = []

with open('inputs/04.txt', 'r') as file:
    for y, line in enumerate(file):
        line = line.rstrip()

        row = ['.']
        row.extend(list(line))
        row.append('.')
        rows.append(row)

    first_row = [ '.' for i in range(len(rows[0]))]
    rows.insert(0, first_row)
    rows.append(first_row)

    accessible = 0

    for i in range(1, len(rows) - 1):
        for j in range(1, len(rows[i]) - 1):
            if rows[i][j] == '.':
                continue 
            cnt = 0
            for ox in (-1, 0, 1):
                for oy in (-1, 0, 1):
                    if ox == 0 and oy == 0:
                        continue
                    if rows[i + oy][j + ox] == '@':
                        cnt += 1
            if cnt < 4:
                accessible += 1

    can_be_removed = 0

    while True:
        removed_this_round = 0
        for i in range(1, len(rows) - 1):
            for j in range(1, len(rows[i]) - 1):
                if rows[i][j] == '.':
                    continue 
                cnt = 0
                for ox in (-1, 0, 1):
                    for oy in (-1, 0, 1):
                        if ox == 0 and oy == 0:
                            continue
                        if rows[i + oy][j + ox] == '@':
                            cnt += 1
                if cnt < 4:
                    rows[i][j] = '.'
                    removed_this_round += 1
        if removed_this_round == 0:
            break
        else:
            can_be_removed += removed_this_round
    
print(f"Part 1: {accessible}") # 1349
print(f"Part 2: {can_be_removed}") # 8277