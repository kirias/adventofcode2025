from pyrsistent import inc


ranges = []

ranges_input = True

fresh_count = 0

with open('inputs/05.txt', 'r') as file:
    for y, line in enumerate(file):
        line = line.rstrip()
        if not line:
            ranges_input = False
            continue

        if ranges_input:
            range = line.split('-')
            ranges.append((int(range[0]), int(range[1])))
        else:
            id = int(line)
            for (frm, to) in ranges:
                if id >= frm and id <= to:
                    fresh = True
                    fresh_count += 1
                    break

    total_ids = 0
    points = set()
    for f, t in ranges:
        points.add(f)
        points.add(t)

    points = list(points)
    points.sort()

    def end_ranges(p):
        ends_count = 0
        for _, endr in ranges:
            if endr == p:
                ends_count += 1
        return ends_count
    
    def start_ranges(p):
        starts_count = 0
        for strtrange,_ in ranges:
            if strtrange == p:
                starts_count += 1
        return starts_count

    included = start_ranges(points[0])
    prev_point = points[0]
    for p in points[1:]:

        if included > 0:
            total_ids += p - prev_point

        included -= end_ranges(p)
        included += start_ranges(p)

        if included == 0:
            total_ids += 1
        
        prev_point = p


print(f"Part 1: {fresh_count}")
print(f"Part 2: {total_ids}")