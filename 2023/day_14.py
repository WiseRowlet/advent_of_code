import numpy as np
from aocd import get_puzzle

DAY = 14
YEAR = 2023

puzzle = get_puzzle(day=DAY, year=YEAR)
puzzle_data = puzzle.input_data
examples = puzzle.examples
example_input = examples[0].input_data
part_a_example_solution = examples[0].answer_a
part_b_example_solution = examples[0].answer_b


def parse_input(input_data):
    grid = np.array([list(row) for row in input_data.split("\n")])
    return grid


def tilt_array(array, direction):
    fixed_indices = np.where(array == "#")[0]
    sections = np.split(array, fixed_indices)

    sorted_sections = [
        sorted(
            section,
            key=lambda x: (x == ".", x == "O", x == "#") if direction == "left" else (x == "O", x == ".", x == "#"),
        )
        for section in sections
    ]
    return np.concatenate(sorted_sections)


def tilt_grid(grid, tilt):
    if tilt == "North":
        return np.array([tilt_array(column, "left") for column in grid.T]).T
    elif tilt == "South":
        return np.array([tilt_array(column, "right") for column in grid.T]).T
    elif tilt == "West":
        return np.array([tilt_array(row, "left") for row in grid])
    elif tilt == "East":
        return np.array([tilt_array(row, "right") for row in grid])


def cycle(grid, n):
    for _ in range(n):
        grid = tilt_grid(grid, "North")
        grid = tilt_grid(grid, "West")
        grid = tilt_grid(grid, "South")
        grid = tilt_grid(grid, "East")
    return grid


def calculate_load(grid):
    load = 0
    height = grid.shape[0]
    for i, row in enumerate(grid):
        load += np.where(row == "O")[0].size * (height - i)

    return load


def part_a(input_data, tilt="North"):
    grid = parse_input(input_data)
    grid = tilt_grid(grid, tilt)
    return calculate_load(grid)


def part_b(input_data):
    grid = parse_input(input_data)
    loads = []
    history = {}
    for i in range(300):
        grid = cycle(grid, 1)
        load = calculate_load(grid)
        loads.append(load)

        if i > 20:
            state_hash = str(loads[-20:])
            if state_hash in history:
                rep_cycle_start = history[state_hash]
                rep_cycle_length = i - rep_cycle_start
                break
            history[state_hash] = i
    target = 1000000000
    offset = (target - rep_cycle_start) % rep_cycle_length - 1
    return loads[rep_cycle_start + offset]


print(example_input)
# print(parse_input(example_input))
print("Example Output A: ", part_a(example_input))
print("Example Output B: ", part_b(example_input))
print("Part A: ", part_a(puzzle_data))
print("Part B: ", part_b(puzzle_data))
