def get_input(file_path):
    with open(file_path, "r") as file:
        input_map = [line.strip() for line in file]
    return input_map


def find_trail_heads(trail_map):
    trail_heads = []
    for y, string in enumerate(trail_map):
        for x, char in enumerate(string):
            if char == "0":
                trail_heads.append((x, y))
    return trail_heads


def find_trails(trail_map, position):
    x, y = position
    current_elevation = int(trail_map[y][x])
    next_elevation = current_elevation + 1
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    valid_trails = []
    trail_ends = set()
    trail_count = 0
    for direction in directions:
        dx, dy = direction
        next_x = x + dx
        next_y = y + dy

        if (
            0 <= next_x < len(trail_map[0])
            and 0 <= next_y < len(trail_map)
            and trail_map[next_y][next_x] == str(next_elevation)
        ):
            if next_elevation == 9:
                trail_ends.add((next_x, next_y))
                trail_count += 1
            else:
                valid_trails.append((next_x, next_y))

    for valid_position in valid_trails:
        next_ends, next_count = find_trails(trail_map, valid_position)
        trail_ends.update(next_ends)
        trail_count += next_count

    return trail_ends, trail_count


def trail_sum(trail_map):
    trail_heads = find_trail_heads(trail_map)
    trail_sum = 0
    trail_count_total = 0
    for trail_head in trail_heads:
        trail_ends, trail_count = find_trails(trail_map, trail_head)
        trail_sum += len(trail_ends)
        trail_count_total += trail_count
    return trail_sum, trail_count_total


trail_map = [
    "89010123",
    "78121874",
    "87430965",
    "96549874",
    "45678903",
    "32019012",
    "01329801",
    "10456732",
]

trail_map = get_input("2024/Data/10_input.txt")
trail_sum, trail_count = trail_sum(trail_map)
print(trail_sum, trail_count)
