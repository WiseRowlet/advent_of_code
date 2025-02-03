import math
import re

from aocd import get_puzzle

DAY = 8
YEAR = 2023

puzzle = get_puzzle(day=DAY, year=YEAR)
puzzle_data = puzzle.input_data
examples = puzzle.examples
example_input = examples[0].input_data
example_input_2 = examples[1].input_data
example_input_3 = examples[2].input_data
part_a_example_solution = examples[1].answer_a
part_b_example_solution = examples[2].answer_b


def parse_input(input_data):
    lines = input_data.splitlines()
    instructions = [0 if d == "L" else 1 for d in lines[0]]
    elements = {}
    for line in lines[2:]:
        m = re.match(r"([1-9A-Z]{3}) = \(([1-9A-Z]{3}), ([1-9A-Z]{3})\)", line)
        elements[m.group(1)] = [m.group(2), m.group(3)]
    return instructions, elements


def part_a(input_data):
    instructions, elements = parse_input(input_data)
    loc = "AAA"
    steps = 0
    i = 0
    max_instructions = len(instructions)
    while loc != "ZZZ":
        instruction = instructions[i]
        loc = elements[loc][instruction]
        steps += 1
        i = (i + 1) % max_instructions
    return steps


def part_b(input_data):
    instructions, elements = parse_input(input_data)
    locs = [key for key in elements.keys() if key[2] == "A"]
    cycles = []
    for loc in locs:
        i = 0
        steps = 0
        max_instructions = len(instructions)
        while True:
            instruction = instructions[i]
            loc = elements[loc][instruction]
            steps += 1
            if loc[2] == "Z":
                cycles.append(steps)
                break
            i = (i + 1) % max_instructions
    return math.lcm(*cycles)


# print(example_input_3)
# print(parse_input(example_input))
print("Example Output A: ", part_a(example_input_2), " Solution: ", part_a_example_solution)
print("Example Output B: ", part_b(example_input_3), " Solution: ", part_b_example_solution)
print("Part A: ", part_a(puzzle_data))
print("Part B: ", part_b(puzzle_data))
