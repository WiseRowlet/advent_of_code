import re

from aocd import get_puzzle

DAY = 1
YEAR = 2023

puzzle = get_puzzle(day=DAY, year=YEAR)
puzzle_data = puzzle.input_data
examples = puzzle.examples
example_input = examples[0].input_data
example_input_b = examples[1].input_data
part_a_example_solution = examples[0].answer_a
part_b_example_solution = examples[1].answer_b


def parse_input(input_data):
    return [line for line in input_data.splitlines()]


def part_a(input_data):
    lines = parse_input(input_data)
    sum = 0
    for line in lines:
        first = re.search(r"\d", line)
        last = re.search(r"\d", line[::-1])
        sum += int(str(first.group()) + str(last.group()))
    return sum


def get_nums(line):
    nums = []
    num_dict = {
        "zero": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }
    for num in num_dict:
        matches = [m.start() for m in re.finditer(num, line)]
        if len(matches) > 0:
            for match in matches:
                nums.append((match, num_dict[num]))
    for c in line:
        if c.isdigit():
            nums.append((line.index(c), int(c)))

    nums = sorted(nums)
    return int(str(nums[0][1]) + str(nums[-1][1]))


def part_b(input_data):
    lines = parse_input(input_data)
    sum = 0
    for line in lines:
        line_num = get_nums(line)
        sum += line_num
    return sum


# print(example_input)
print("Example Output A: ", part_a(example_input), " Solution: ", part_a_example_solution)
print("Example Output B: ", part_b(example_input_b), " Solution: ", part_b_example_solution)
print("Part A: ", part_a(puzzle_data))
print("Part B: ", part_b(puzzle_data))
