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
            for start, end in ranges:
                if id >= start and id <= end:
                    fresh_count += 1
                    break

    total_ids = 0
    points = set()
    for f, t in ranges:
        points.add(f)
        points.add(t)

    points = list(points)
    points.sort()
    
    def start_end_ranges(p):
        starts_count = 0
        for start, end in ranges:
            if start == p:
                starts_count += 1
            if end == p:
                starts_count -= 1
        return starts_count

    included = start_end_ranges(points[0])
    prev_point = points[0]
    for point in points[1:]:

        if included > 0:
            total_ids += point - prev_point
        
        included += start_end_ranges(point)

        if included == 0:
            total_ids += 1
        
        prev_point = point


print(f"Part 1: {fresh_count}")
print(f"Part 2: {total_ids}")