from aocd import get_puzzle

DAY = 3
YEAR = 2023

puzzle = get_puzzle(day=DAY, year=YEAR)
puzzle_data = puzzle.input_data
examples = puzzle.examples
example_input = examples[0].input_data
part_a_example_solution = examples[0].answer_a
part_b_example_solution = examples[0].answer_b


def parse_input(input_data):
    numbers = []
    symbols = set()
    gears = set()
    lines = input_data.splitlines()
    for i, line in enumerate(lines):
        length = len(line)
        j = 0
        while j < length:
            if line[j].isdigit():
                num = ""
                num_set = set()
                while j < length and line[j].isdigit():
                    num += line[j]
                    num_set.add((i, j))
                    j += 1
                numbers.append((int(num), num_set))

            if j < length and line[j] != ".":
                symbols.add((i, j))
                if line[j] == "*":
                    gears.add((i, j))

            j += 1
    return numbers, symbols, gears


def get_neighbors(x, y, size):
    size_x, size_y = size
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    neighbors = [(x + dx, y + dy) for dx, dy in directions if 0 <= x + dx < size_x and 0 <= y + dy < size_y]

    return [n for n in neighbors]


def part_a(input_data):
    size = (len(input_data.splitlines()), len(input_data.splitlines()[0]))
    numbers, symbols, _ = parse_input(input_data)
    part_sum = 0
    for number in numbers:
        num, num_set = number
        found = False
        for digit in num_set:
            neighbors = get_neighbors(*digit, size)
            for nx, ny in neighbors:
                if (nx, ny) in symbols:
                    part_sum += num
                    found = True
                    break
            if found:
                break
    return part_sum


def part_b(input_data):
    size = (len(input_data.splitlines()), len(input_data.splitlines()[0]))
    numbers, _, gears = parse_input(input_data)
    gear_ratio = 0
    for gear in gears:
        neighbors = get_neighbors(*gear, size)
        num_neighbors = []
        for number in numbers:
            num, num_set = number
            for nx, ny in neighbors:
                if (nx, ny) in num_set:
                    num_neighbors.append(num)
                    break
            if len(num_neighbors) == 2:
                gear_ratio += num_neighbors[0] * num_neighbors[1]
                break
    return gear_ratio


# print(example_input)
print("Example Output A: ", part_a(example_input), " Solution: ", part_a_example_solution)
print("Example Output B: ", part_b(example_input), " Solution: ", part_b_example_solution)
print("Part A: ", part_a(puzzle_data))
print("Part B: ", part_b(puzzle_data))
