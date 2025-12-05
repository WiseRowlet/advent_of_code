# aocd import
from aocd import get_puzzle
DAY = 3
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
    return [line for line in input_data.splitlines()]

# puzzle imports
from math import floor

# puzzle solutions
def part_a(input_data, xm: int = 2):
    lines = parse_input(input_data)
    sum = 0

    for line in lines:
        sum += get_max_joltage(line, xm)
    return sum

def part_b(input_data):
    return part_a(input_data, xm=12)

# puzzle helper functions
def get_max_joltage(batteries: str, xm: int = 2) -> int:
    start = 0      # first index we are allowed to pick from
    total = 0      # resulting number we’re building

    for pick in range(xm):
        best_digit = -1
        best_index = start

        # Highest index we’re allowed to consider for this pick.
        # We must leave enough digits to fill the remaining picks.
        last_allowed = len(batteries) - (xm - pick)

        for i in range(start, last_allowed + 1):
            d = int(batteries[i])
            if d > best_digit:
                best_digit = d
                best_index = i

        # Append this digit to the result
        total = total * 10 + best_digit

        # Next pick must come after this index
        start = best_index + 1

    return total

# puzzle outputs
# print(example_input_a)
print("Example Output A: ", part_a(example_input_a), " Solution: ", part_a_example_solution)
print("Example Output B: ", part_b(example_input_b), " Solution: ", part_b_example_solution)
print("Part A: ", part_a(puzzle_data))
print("Part B: ", part_b(puzzle_data))
