# aocd import
from aocd import get_puzzle
DAY = 4
YEAR = 2025

puzzle = get_puzzle(day=DAY, year=YEAR)
puzzle_data = puzzle.input_data
examples = puzzle.examples
example_input_a = examples[0].input_data
part_a_example_solution = examples[0].answer_a

part_b_index = 0
if len(examples) > 1:
    part_b_index = 1 
example_input_b = examples[part_b_index].input_data
part_b_example_solution = examples[part_b_index].answer_b

# puzzle input parser
def parse_input(input_data):
    lines = input_data.splitlines()
    size = (len(lines), len(lines[0]))
    ats = set()
    
    for i, line in enumerate(lines):
        length = len(line)
        j = 0
        while j < length:
            if line[j] == "@":
                ats.add((i, j))
            j += 1
    return ats, size

# puzzle imports

# puzzle solutions
def part_a(input_data):
    ats, size = parse_input(input_data)
    total = 0
    for at in ats:
        x, y = at
        neighbors = get_neighbors(x, y, size)
        num_neighbors = 0
        for nx, ny in neighbors:
            if (nx, ny) in ats:
                num_neighbors += 1
        if num_neighbors < 4:
            total += 1
    return total

def part_b(input_data):
    ats, size = parse_input(input_data)
    total = 0
    while True:
        new_ats = set()
        subtotal = 0
        for at in ats:
            x, y = at
            neighbors = get_neighbors(x, y, size)
            num_neighbors = 0
            for nx, ny in neighbors:
                if (nx, ny) in ats:
                    num_neighbors += 1
            if num_neighbors < 4:
                total += 1
                subtotal += 1
            else:
                new_ats.add(at)
        if subtotal == 0:
            break
        ats = new_ats
    return total

# puzzle helper functions
def get_neighbors(x, y, size):
    size_x, size_y = size
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    neighbors = [(x + dx, y + dy) for dx, dy in directions if 0 <= x + dx < size_x and 0 <= y + dy < size_y]

    return [n for n in neighbors]

# puzzle outputs
# print(example_input_a)
print("Example Output A: ", part_a(example_input_a), " Solution: ", part_a_example_solution)
print("Example Output B: ", part_b(example_input_b), " Solution: ", part_b_example_solution)
print("Part A: ", part_a(puzzle_data))
print("Part B: ", part_b(puzzle_data))
