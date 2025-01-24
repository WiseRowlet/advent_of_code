from collections import defaultdict
from itertools import product

from aocd import get_puzzle

DAY = 7
YEAR = 2024

puzzle = get_puzzle(day=DAY, year=YEAR)
puzzle_data = puzzle.input_data
examples = puzzle.examples
example_input = examples[0].input_data
part_a_example_solution = examples[0].answer_a
part_b_example_solution = examples[0].answer_b


def parse_input(input_data):
    equations = defaultdict(list)
    for line in input_data.splitlines():
        equations[int(line.split(": ")[0])] = [x for x in map(int, line.split(": ")[1].split(" "))]
    return equations


def part_a(input_data, operators={"+": lambda x, y: x + y, "*": lambda x, y: x * y}):
    equations = parse_input(input_data)
    sum = 0
    for sol, nums in equations.items():
        operations = product(operators.keys(), repeat=len(nums) - 1)
        for operation in operations:
            result = nums[0]
            for i, num in enumerate(nums[1:]):
                result = operators[operation[i]](result, num)
                if result > sol:
                    break
            if result == sol:
                sum += sol
                break
    return sum


def part_b(input_data):
    # This is too slow, there's a better way to do this, but it wasn't slow enough to make me look for it
    operators = {"+": lambda x, y: x + y, "*": lambda x, y: x * y, "||": lambda x, y: int(f"{x}{y}")}
    return part_a(input_data, operators)


# print(example_input)
# print(parse_input(example_input))
print("Example Output A: ", part_a(example_input))
print("Example Output B: ", part_b(example_input))
print("Part A: ", part_a(puzzle_data))
print("Part B: ", part_b(puzzle_data))
