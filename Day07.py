lines = []

with open('inputs/07.txt', 'r') as file:
    for y, line in enumerate(file):
        line = line.rstrip()
        lines.append(line)

beams = []
start = 0
len_line = len(lines[0])
for i in range(len_line):
    if lines[0][i] == 'S':
        beams.append(i)
        start = i
        break

splits = 0

for i in range(1, len(lines)):
    next_beams = set()
    for beam in beams:
        if lines[i][beam] == '^':
            if beam > 0:
                next_beams.add(beam - 1)
            if beam < len_line - 1:
                next_beams.add(beam + 1)
            splits += 1
        else:
            next_beams.add(beam)
    beams = next_beams

print(f"Part 1: {splits}")

beams = dict()
beams[start] = 1

for i in range(1, len(lines)):
    next_beams = dict()
    for beam in beams:
        if lines[i][beam] == '^':
            if beam > 0:
                next_beams[beam - 1] = next_beams.get(beam - 1, 0) + beams[beam]
            if beam < len_line - 1:
                next_beams[beam + 1] = next_beams.get(beam + 1, 0) + beams[beam]
        else:
            next_beams[beam] = next_beams.get(beam, 0) + beams[beam]
    beams = next_beams

print(f"Part 2: {sum(beams.values())}")

