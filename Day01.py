start = 50
count_z = 0
count_clicks = 0

with open('inputs/01.txt', 'r') as file:
    for y, line in enumerate(file):
        line = line.rstrip()

        rotation = int(line[1:])

        count_clicks += rotation // 100
        rotation %= 100

        if line[0] == 'R':
            if start + rotation > 100:
                count_clicks += 1
            start = (start + rotation) % 100
        else:
            if start > 0 and start - rotation < 0:
                count_clicks += 1
            start = (start + 100 - rotation) % 100
        if start == 0:
            count_z += 1
            count_clicks += 1
    
print(f"Part 1: {count_z}")
print(f"Part 2: {count_clicks}")