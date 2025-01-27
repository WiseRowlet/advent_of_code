import numpy as np
from aocd import get_puzzle

DAY = 13
YEAR = 2023

puzzle = get_puzzle(day=DAY, year=YEAR)
puzzle_data = puzzle.input_data
examples = puzzle.examples
example_input = examples[0].input_data
part_a_example_solution = examples[0].answer_a
part_b_example_solution = examples[0].answer_b


def parse_input(input_data):
    graphs = []
    for block in input_data.split("\n\n"):
        graph = np.array([list(row) for row in block.split("\n")])
        graphs.append(graph)
    return graphs


def get_mirror_column(graph, smudges=0):
    n_cols = graph.shape[1]
    for c in range(1, n_cols):
        span = min(c, n_cols - c)
        right = graph[:, c : c + span]
        left = graph[:, c - span : c][:, ::-1]
        if (right != left).sum() == smudges:
            return c
    return None


def get_mirror_row(graph, smudges=0):
    n_rows = graph.shape[0]
    for r in range(1, n_rows):
        span = min(r, n_rows - r)
        bottom = graph[r : r + span, :]
        top = graph[r - span : r, :][::-1]
        if (top != bottom).sum() == smudges:
            return r
    return None


def part_a(input_data, smudges=0):
    graphs = parse_input(input_data)
    sum = 0

    for graph in graphs:
        if (row := get_mirror_row(graph, smudges)) is not None:
            sum += row * 100
        else:
            sum += get_mirror_column(graph, smudges)

    return sum


def part_b(input_data):
    return part_a(input_data, smudges=1)


# print(example_input)
# print(parse_input(example_input))
print("Example Output A: ", part_a(example_input))
print("Example Output B: ", part_b(example_input))
print("Part A: ", part_a(puzzle_data))
print("Part B: ", part_b(puzzle_data))
