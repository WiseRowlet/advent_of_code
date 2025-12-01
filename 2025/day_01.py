# aocd import
from aocd import get_puzzle
DAY = 1
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

def parse_input(input_data):
    return [line for line in input_data.splitlines()]

# puzzle imports
from math import floor

# puzzle solutions
def part_a(input_data):
    lines = parse_input(input_data)
    sum = 0
    position = 50
    for line in lines:
        position,_ = turn_dial(line, position)
        sum += 1 if position == 0 else 0
    return sum

def part_b(input_data):
    lines = parse_input(input_data)
    sum = 0
    position = 50
    for line in lines:
        position, num_0 = turn_dial(line, position)
        sum += num_0
    return sum

# puzzle helper functions
def turn_dial(instruction, position):
    direction, steps = instruction[0], instruction[1:]
    steps = int(steps)
    num_0 = 0
    new_position = position
    if direction == "R":
        num_0 = floor((position + steps) / 100)
        new_position = (position + steps) % 100  
    elif direction == "L":
        num_0 = abs(floor((position - steps) / 100))
        new_position = (position - steps) % 100
        if new_position == 0:
            num_0 += 1
        if position == 0:
            num_0 -= 1
    return new_position, num_0

# puzzle outputs
# print(example_input_a)
print("Example Output A: ", part_a(example_input_a), " Solution: ", part_a_example_solution)
print("Example Output B: ", part_b(example_input_b), " Solution: ", part_b_example_solution)
print("Part A: ", part_a(puzzle_data))
print("Part B: ", part_b(puzzle_data))
