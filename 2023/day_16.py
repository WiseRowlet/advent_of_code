from aocd import get_puzzle
from collections import deque

DAY = 16
YEAR = 2023

puzzle = get_puzzle(day=DAY, year=YEAR)
puzzle_data = puzzle.input_data
examples = puzzle.examples
example_input = examples[0].input_data
part_a_example_solution = examples[0].answer_a
part_b_example_solution = examples[0].answer_b

DIRECTIONS = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
}

MIRROR_MAP = {
    "\\": {
        "up": ["left"],
        "down": ["right"],
        "left": ["up"],
        "right": ["down"],
    },
    "/": {
        "up": ["right"],
        "down": ["left"],
        "left": ["down"],
        "right": ["up"],
    },
    "-": {
        "up": ["left", "right"],
        "down": ["left", "right"],
        "left": ["left"],
        "right": ["right"],
    },
    "|": {
        "up": ["up"],
        "down": ["down"],
        "left": ["up", "down"],
        "right": ["up", "down"],
    },
    ".": {
        "up": ["up"],
        "down": ["down"],
        "left": ["left"],
        "right": ["right"],
    },
}

def parse_input(input_data):
    return input_data.splitlines()


def part_a(input_data, start=(0,0,"right")):
    grid = parse_input(input_data)
    sx, sy, _ = start
    height = len(grid)
    width = len(grid[0])
    queue = deque([start])
    visited = set()
    loop_check = set()
    visited.add((sx,sy))
    loop_check.add(start)

    while queue:
        x, y, direction = queue.popleft()
        c = grid[y][x]
        if c in MIRROR_MAP:
            for d in MIRROR_MAP[c][direction]:
                dx, dy = DIRECTIONS[d]
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    if (nx,ny,d) not in loop_check:
                        visited.add((nx, ny))
                        loop_check.add((nx,ny,d))
                        queue.append((nx,ny,d))
    return len(visited)


def part_b(input_data):
    grid = parse_input(input_data)
    height = len(grid)
    width = len(grid[0])
    charged = 0

    for i in range(width):
        charge = part_a(input_data, (i, 0, "down"))
        if charge > charged:
            charged = charge
        charge = part_a(input_data, (i, height-1, "up"))
        if charge > charged:
            charged = charge
    for i in range(height):
        charge = part_a(input_data, (0, i, "right"))
        if charge > charged:
            charged = charge
        charge = part_a(input_data, (width-1, i, "left"))
        if charge > charged:
            charged = charge
    
    return charged

print(example_input)
# print(parse_input(example_input))
print("Example Output A: ", part_a(example_input), " Solution: ", part_a_example_solution)
print("Example Output B: ", part_b(example_input), " Solution: ", part_b_example_solution)
print("Part A: ", part_a(puzzle_data))
print("Part B: ", part_b(puzzle_data))
