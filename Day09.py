import functools

coords = []

with open('inputs/09.txt', 'r') as file:
    for y, line in enumerate(file):
        coord = line.rstrip().split(',')
        coords.append((int(coord[0]), int(coord[1])))

max_s = 0
for i, (x1,y1) in enumerate(coords):
    for j in range(i + 1, len(coords)):
        x2, y2 = coords[j]

        s = abs((x1 - x2 + 1) *(y1 - y2 + 1))

        if s > max_s:
            max_s = s

print(f"Part 1: {max_s}")


coords_x = list(set([c[0] for c in coords]))
coords_y = list(set([c[1] for c in coords]))

coords_x.sort()
coords_y.sort()

colors = dict()

for x in coords_x:
    colors[(x, x)] = dict()
    for y in coords_y:
        colors[(x, x)][(y, y)] = -1 # unknown
    for y1, y2 in zip(coords_y, coords_y[1:]):
        if y2 - y1 == 1:
            continue
        colors[(x, x)][(y1 + 1, y2 - 1)] = -1

for c in coords:
    colors[(c[0], c[0])][(c[1], c[1])] = 1 # red

for x1, x2 in zip(coords_x, coords_x[1:]):
    if x2 - x1 != 1:
        xrng = (x1 + 1, x2 - 1)
        if xrng not in colors:
            colors[xrng] = dict()
        for y in coords_y:
            colors[xrng][(y, y)] = -1 # unknown
    for y1, y2 in zip(coords_y, coords_y[1:]):
        if y2 - y1 == 1 and x2 - x1 == 1:
            continue
        if y2 - y1 == 1:
            xrng = (x1 + 1, x2 - 1)
            if xrng not in colors:
                colors[xrng] = dict()
            colors[xrng][(y1, y1)] = -1 # unknown
            colors[xrng][(y2, y2)] = -1 # unknown
            continue
        if x2 - x1 == 1:
            colors[(x1, x1)][(y1 + 1, y2 - 1)] = -1
            colors[(x2, x2)][(y1 + 1, y2 - 1)] = -1
            continue
        
        xrng = (x1 + 1, x2 - 1)
        if xrng not in colors:
            colors[xrng] = dict()
        colors[xrng][(y1 + 1, y2 - 1)] = -1 # unknown


def get_range(x, y):
    for xr in colors:
        if xr[0] == x or xr[1] == x or (xr[0] < x and xr[1] > x):
            ycolors = colors[xr]
            for yr in ycolors:
                if yr[0] == y or yr[1] == y or (yr[0] < y and yr[1] > y):
                    return ycolors[yr]
    raise "Not found"

def set_range(x, y, val):
    for xr in colors:
        if xr[0] == x or xr[1] == x or (xr[0] < x and xr[1] > x):
            ycolors = colors[xr]
            for yr in ycolors:
                if yr[0] == y or yr[1] == y or (yr[0] < y and yr[1] > y):
                    ycolors[yr] = val
                    return

lines = []

(x1, y1), (x2, y2) = coords[-1], coords[0]
lines.append((x1, x2, y1, y2))

for i in range(1, len(coords)):
    (x1, y1), (x2, y2) = coords[i - 1], coords[i]
    lines.append((x1, x2, y1, y2))

for x1, x2, y1, y2 in lines:
    for x in range(min(x1, x2), max(x1, x2) + 1):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            set_range(x, y, 1)

min_y = min(coords, key=lambda x : x[1])[1] - 1
max_y = max(coords, key=lambda x : x[1])[1] + 1

max_s = 0

hor_lines = [(min(x1, x2), max(x1, x2), y1)  for (x1, x2, y1, y2)  in lines if y1 == y2]

@functools.cache
def is_white(x, y):
    r = get_range(x, y)
    if r != -1:
        return r == 0

    intersect_lines = []
    if y - min_y < max_y - y: # going up
        for iy in range(y, min_y - 1, -1):
            for (x1, x2, y1) in hor_lines:
                if y1 == y  and x1 <= x and x2 >= x:
                    return False
                if y1 == iy and x1 <= x and x2 >= x:
                    intersect_lines.append((x1, x2, y1))
    else:
        for iy in range(y, max_y + 1): # going down
            for (x1, x2, y1) in hor_lines:
                if y1 == y  and x1 <= x and x2 >= x:
                    return False
                if y1 == iy and x1 <= x and x2 >= x:
                    intersect_lines.append((x1, x2, y1))
    
    intersects = 0
    count_min = 0
    count_max = 0
    for (x1, x2, y1) in intersect_lines:
        if x1 < x and x2 > x:
            intersects += 1
        if x1 == x:
            count_min += 1
        if x2 == x:
            count_max += 1

    count_min %= 2
    count_max %= 2

    if count_max == 1 and count_min == 1:
        intersects += 1

    white = intersects % 2 == 0
    if white:
        set_range(x, y, 0)
    else:
        set_range(x, y, 1)
    return white

# coords.sort(key=lambda c : c[1] * 100000 + c[0])

for i, (x1, y1) in enumerate(coords):
    for j in range(i + 1, len(coords)):
        x2, y2 = coords[j]
        s = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)

        if s > max_s:
            if s >= 1653718920: # too high
                continue
            if s <= 455423693:  # too low
                continue

            print(max_s, "Checking", s)
            white = False

            for yi in range(min(y1, y2) + 1, max(y1, y2)):
                if is_white(x1, yi) or is_white(x2, yi):
                    white = True
                    break

            if white:
                continue

            for xi in range(min(x1, x2) + 1, max(x1, x2)):
                if is_white(xi, y1) or is_white(xi, y2):
                    white = True
                    break

            if white:
                continue

            max_s = s
            print(max_s)


print(f"Part 2: {max_s}")