import math


coords = []

dists = dict()

with open('inputs/08.txt', 'r') as file:
    for y, line in enumerate(file):
        line = line.rstrip()
        raw_coords = line.split(',')
        coords.append((int(raw_coords[0]), int(raw_coords[1]), int(raw_coords[2])))

for i in range(len(coords) - 1):
    b1 = coords[i]
    for j in range(i + 1, len(coords)):
        b2 = coords[j]
        dist = math.sqrt((b1[0] - b2[0])**2 + (b1[1] - b2[1])**2 + (b1[2] - b2[2])**2 )
        dists[(i, j)] = dist
        # dists[(j, i)] = dist

dists = dict(sorted(dists.items(), key=lambda item: item[1]))

circuts = []
connected = 0

def in_circuit(el):
    for c in circuts:
        if el in c:
            return c
    return None

def merge_circuits(circuit1, circuit2):
    circuts.remove(circuit2)
    circuit1.update(circuit2)

def add_to_circuit(circuit, el):
    circuit.add(el)

while connected < 1000:
    min1, min2 = min(dists, key=dists.get)

    del dists[(min1, min2)]

    c1 = in_circuit(min1)
    c2 = in_circuit(min2)

    if c1 != None and c2 != None:
        if c1 != c2:
            merge_circuits(c1, c2)
    elif c1 == None and c2 == None:
        c = set()
        c.add(min1)
        c.add(min2)
        circuts.append(c)
    else:
        if c1 != None:
            add_to_circuit(c1, min2)
        else:
            add_to_circuit(c2, min1)
            

    connected += 1
    print(connected)


circuts.sort(key = lambda c: -len(c))


print(f"Part 1: {len(circuts[0]) * len(circuts[1]) * len(circuts[2])}")

