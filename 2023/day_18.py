from aocd import get_puzzle

DAY = 18
YEAR = 2023

puzzle = get_puzzle(day=DAY, year=YEAR)
puzzle_data = puzzle.input_data
examples = puzzle.examples
example_input = examples[0].input_data
part_a_example_solution = examples[0].answer_a
part_b_example_solution = examples[0].answer_b


def parse_input(input_data):
    return [tuple(line.split(" ")) for line in input_data.splitlines()]


def polygon_area(vertices):
    """Calculate the area of a polygon using the shoelace formula.

    vertices: List of (x, y) tuples, ordered around the perimeter.
    """
    n = len(vertices)
    area = 0
    perimeter = 0
    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]
        area += x1 * y2 - x2 * y1
        perimeter += abs(x2 - x1) + abs(y2 - y1)
    return int((abs(area) + perimeter) / 2 + 1)


def part_a(input_data):
    instructions = parse_input(input_data)
    directions = {
        "R": (1, 0),
        "D": (0, 1),
        "L": (-1, 0),
        "U": (0, -1),
    }

    start = (0, 0)
    v = []

    x, y = start
    v.append((x, y))

    for d, q, _ in instructions:
        dx, dy = directions[d]
        q = int(q)
        x, y = x + (dx * q), y + (dy * q)
        if (x, y) != start:
            v.append((x, y))

    return polygon_area(v)


def part_b(input_data):
    instructions = parse_input(input_data)
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    start = (0, 0)
    v = []

    x, y = start
    v.append((x, y))

    for _, _, h in instructions:
        q = int(h[2:-2], 16)
        d = int(h[-2:-1])
        dx, dy = directions[d]
        x, y = x + (dx * q), y + (dy * q)
        if (x, y) != start:
            v.append((x, y))

    return polygon_area(v)


# print(example_input)
# print(parse_input(example_input))
print("Example Output A: ", part_a(example_input), " Solution: ", part_a_example_solution)
print("Example Output B: ", part_b(example_input), " Solution: ", part_b_example_solution)
print("Part A: ", part_a(puzzle_data))
print("Part B: ", part_b(puzzle_data))
