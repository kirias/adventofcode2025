from tarfile import OutsideDestinationError

connections = dict()

with open('inputs/11.txt', 'r') as file:
    for y, line in enumerate(file):
        line = line.rstrip().split(': ')
        input = line[0]
        outputs = line[1].split()
        connections[input] = outputs


path_count = dict()
path_count['out'] = 1

to_check = [['you']]

def get_paths_count(node, path = []):
    if node in path_count:
        return path_count[node]
    
    if node in path:
        return 0
    
    sum = 0
    new_path = path.copy()
    new_path.append(node)
    for output in connections[node]:
        sum += get_paths_count(output, new_path)
    
    path_count[node] = sum
    return sum

print(f"Part 1: {get_paths_count('you')}")

path_count2 = dict()
path_count2[('out', False, False)] = 1 # to node, fft visited, dac visited

def get_paths_count2(node, fft, dac, path = []):
    if (node, fft, dac) in path_count2:
        return path_count2[(node, fft, dac)]
    
    if node in path:
        return 0
    
    if node not in connections:
        return 0
    
    sum = 0
    new_path = path.copy()
    new_path.append(node)
    for output in connections[node]:
        if output == 'fft':
            sum += get_paths_count2(output, False, dac, new_path)
        elif output == 'dac':
            sum += get_paths_count2(output, fft, False, new_path)
        else:
            sum += get_paths_count2(output, fft, dac, new_path)
    
    path_count2[(node, fft, dac)] = sum
    return sum


print(f"Part 2: {get_paths_count2('svr', True, True)}")