import re

from aocd import get_puzzle

DAY = 22
YEAR = 2023

puzzle = get_puzzle(day=DAY, year=YEAR)
puzzle_data = puzzle.input_data
examples = puzzle.examples
example_input = examples[0].input_data
part_a_example_solution = examples[0].answer_a
part_b_example_solution = examples[0].answer_b


def parse_input(input_data):
    regex = r"(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)"
    blocks = []
    for block in re.findall(regex, input_data):
        x1, y1, z1, x2, y2, z2 = map(int, block)
        x1, x2 = sorted((x1, x2))
        y1, y2 = sorted((y1, y2))
        z1, z2 = sorted((z1, z2))
        blocks.append((x1, y1, z1, x2, y2, z2))
    return blocks


def blocks_fall(blocks):
    blocks.sort(key=lambda x: x[2])
    X = max(b[3] for b in blocks) + 1
    Y = max(b[4] for b in blocks) + 1
    Z = max(b[5] for b in blocks) + 1

    stack = [[["empty" for _ in range(X)] for _ in range(Y)] for _ in range(Z)]
    supported_by = {}

    for block_id, (x1, y1, z1, x2, y2, z2) in enumerate(blocks):
        for z in range(Z):
            support = set(stack[z][y][x] for x in range(x1, x2 + 1) for y in range(y1, y2 + 1)) - {"empty"}
            if support:
                supported_by[block_id] = support
                break
        height = z2 - z1 + 1
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z_ in range(z - height, z):
                    stack[z_][y][x] = block_id

    return supported_by


def part_a(input_data):
    blocks = parse_input(input_data)
    supported_by = blocks_fall(blocks)

    indispensable = set.union(*[x for x in supported_by.values() if len(x) == 1])
    return len(blocks) - len(indispensable)


def part_b(input_data):
    blocks = parse_input(input_data)
    supported_by = blocks_fall(blocks)
    N = len(blocks)

    indispensible = set.union(*[x for x in supported_by.values() if len(x) == 1])
    total = 0
    for i in indispensible:
        disintegrated = set([i])
        for j in range(i + 1, N):
            if j in supported_by and supported_by[j].issubset(disintegrated):
                disintegrated.add(j)
        total += len(disintegrated) - 1
    return total


# print(example_input)
# print(parse_input(example_input))
print("Example Output A: ", part_a(example_input), " Solution: ", part_a_example_solution)
print("Example Output B: ", part_b(example_input), " Solution: ", part_b_example_solution)
print("Part A: ", part_a(puzzle_data))
print("Part B: ", part_b(puzzle_data))
