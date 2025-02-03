from itertools import combinations

from aocd import get_puzzle

DAY = 11
YEAR = 2023

puzzle = get_puzzle(day=DAY, year=YEAR)
puzzle_data = puzzle.input_data
examples = puzzle.examples
example_input = examples[0].input_data
part_a_example_solution = examples[0].answer_a
part_b_example_solution = examples[0].answer_b


def parse_input(input_data):
    filled_columns = set()
    empty_lines = set()
    galaxies = set()
    for i, line in enumerate(input_data.splitlines()):
        empty_line = True
        for j, char in enumerate(line):
            if char != ".":
                empty_line = False
                filled_columns.add(j)
                galaxies.add((j, i))
        if empty_line:
            empty_lines.add(i)
    return filled_columns, empty_lines, galaxies


def part_a(input_data, gap=2):
    filled_columns, empty_lines, galaxies = parse_input(input_data)
    pairs = [c for c in combinations(galaxies, 2)]
    sum = 0
    for pair in pairs:
        x1, y1 = pair[0]
        x2, y2 = pair[1]

        x1, x2 = (x1, x2) if x1 < x2 else (x2, x1)
        y1, y2 = (y1, y2) if y1 < y2 else (y2, y1)

        dy = 0
        dx = 0
        for x in range(x1 + 1, x2 + 1):
            if x not in filled_columns:
                dx += gap
            else:
                dx += 1
        for y in range(y1 + 1, y2 + 1):
            if y in empty_lines:
                dy += gap
            else:
                dy += 1
        sum += dx + dy
    return sum


def part_b(input_data, gap=100):
    return part_a(input_data, gap)


# print(example_input)
# print(parse_input(example_input))
print("Example Output A: ", part_a(example_input), " Solution: ", part_a_example_solution)
print("Example Output B: ", part_b(example_input), " Solution: ", part_b_example_solution)
print("Part A: ", part_a(puzzle_data))
print("Part B: ", part_b(puzzle_data, 1000000))
