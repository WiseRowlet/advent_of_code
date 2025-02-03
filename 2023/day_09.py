import re

from aocd import get_puzzle

DAY = 9
YEAR = 2023

puzzle = get_puzzle(day=DAY, year=YEAR)
puzzle_data = puzzle.input_data
examples = puzzle.examples
example_input = examples[0].input_data
part_a_example_solution = examples[0].answer_a
part_b_example_solution = examples[0].answer_b


def parse_input(input_data):
    hists = []
    for line in input_data.splitlines():
        hists.append([int(m) for m in re.findall(r"-?\d+", line)])
    return hists


def part_a(input_data):
    hists = parse_input(input_data)
    s = 0
    for hist in hists:
        final_nums = []
        while set(hist) != set([0]):
            final_nums.append(hist[-1])
            hist = [hist[i] - hist[i - 1] for i in range(1, len(hist))]
        s += sum(final_nums)
    return s


def part_b(input_data):
    hists = parse_input(input_data)
    s = 0
    for hist in hists:
        first_nums = []
        while set(hist) != set([0]):
            first_nums.append(hist[0])
            hist = [hist[i] - hist[i - 1] for i in range(1, len(hist))]
        i = len(first_nums) - 1
        d = 0
        while i >= 0:
            d = first_nums[i] - d
            i -= 1
        s += d
    return s


# print(example_input)
# print(parse_input(example_input))
print("Example Output A: ", part_a(example_input), " Solution: ", part_a_example_solution)
print("Example Output B: ", part_b(example_input), " Solution: ", part_b_example_solution)
print("Part A: ", part_a(puzzle_data))
print("Part B: ", part_b(puzzle_data))
