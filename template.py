from aocd import get_puzzle

DAY = 1
YEAR = 2023

puzzle = get_puzzle(day=DAY, year=YEAR)
puzzle_data = puzzle.input_data
examples = puzzle.examples
example_input = examples[0].input_data
part_a_example_solution = examples[0].answer_a
part_b_example_solution = examples[0].answer_b


def parse_input(input_data):
    pass


def part_a(input_data):
    pass


def part_b(input_data):
    pass


print(example_input)
print(parse_input(example_input))
# print("Example Output A: ", part_a(example_input), " Solution: ", part_a_example_solution)
# print("Example Output B: ", part_b(example_input), " Solution: ", part_b_example_solution)
# print("Part A: ", part_a(puzzle_data))
# print("Part B: ", part_b(puzzle_data))
