
def construct_num(one_part, parts_count, part_len):
    result = one_part
    for i in range(parts_count - 1):
        result *= 10 ** part_len
        result += one_part
    return result


invalid_sum1 = 0
with open('inputs/02.txt', 'r') as file:
    line = file.readline().rstrip()
    groups = line.split(',')

    for group in groups:
        ranges = group.split('-')
        r_from = int(ranges[0])
        r_to = int(ranges[1])

        if len(ranges[0]) % 2 == 1:
            r_from = 10 ** len(ranges[0])
            if r_from > r_to:
                continue
        
        if len(ranges[1]) % 2 == 1:
            r_to = 10 ** (len(ranges[1]) - 1) - 1
            if r_to < r_from:
                continue

        digits_cnt = len(str(r_from)) // 2
        
        first_part = r_from // (10 ** digits_cnt)

        while construct_num(first_part, 2, digits_cnt) < r_from:
            first_part += 1
        
        while construct_num(first_part, 2, digits_cnt) <= r_to:
            invalid_sum1 += construct_num(first_part, 2, digits_cnt)
            first_part += 1
   
print(f"Part 1: {invalid_sum1}")

invalid_ids = set()
with open('inputs/02.txt', 'r') as file:
    line = file.readline().rstrip()
    groups = line.split(',')

    for group in groups:
        ranges = group.split('-')
        r_from = int(ranges[0])
        r_to = int(ranges[1])

        subranges = []
        if len(ranges[0]) != len(ranges[1]):
            range_split = 10 ** len(ranges[0])
            subranges.append((r_from, range_split - 1)) # will fail in case more than one digit increase, e.g. 5-155
            subranges.append((range_split, r_to))
        else:
            subranges.append((r_from, r_to))

        for s in subranges:
            digits_cnt = len(str(s[0]))

            for dc in range(1, digits_cnt):
                if digits_cnt % dc != 0:
                    continue

                part = s[0] // (10 ** (digits_cnt - dc))
                
                while construct_num(part, digits_cnt // dc, dc) < s[0]:
                    part += 1
        
                while construct_num(part, digits_cnt // dc, dc) <= s[1]:
                    invalid_id = construct_num(part, digits_cnt // dc, dc)
                    invalid_ids.add(invalid_id)
                    part += 1
    
print(f"Part 2: {sum(invalid_ids)}")