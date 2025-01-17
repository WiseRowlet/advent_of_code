from collections import defaultdict


def parse_input(file_path):
    locks = []
    keys = []

    blocks = open(file_path).read().strip().split("\n\n")

    for i, block in enumerate(blocks):
        lines = block.splitlines()
        num_columns = len(lines[0])
        is_key = False
        if lines[0][0] == ".":
            is_key = True

        heights = defaultdict(int)

        for col in range(num_columns):
            heights[col] = -1
            for line in lines:
                if line[col] == "#":
                    heights[col] += 1

        if is_key:
            keys.append(heights)
        else:
            locks.append(heights)

    return locks, keys


def part_one(file_path):
    locks, keys = parse_input(file_path)
    fits = 0
    for key in keys:
        for lock in locks:
            if all(key[col] + lock[col] <= 5 for col in key):
                fits += 1
    return fits


print(part_one("Data/25_input.txt"))
