# aocd import
from aocd import get_puzzle
DAY = 2
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
    return input_data.split(",")

# puzzle imports

# puzzle solutions
def part_a(input_data):
    ids = parse_input(input_data)
    sum = 0
    for id in ids:
        start = int(id.split("-")[0])
        end = int(id.split("-")[1])
        sum += check_invalid_half(start, end)
    return sum

def part_b(input_data):
    ids = parse_input(input_data)
    sum = 0
    for id in ids:
        start = int(id.split("-")[0])
        end = int(id.split("-")[1])
        sum += check_invalid(start, end)
    return sum

# puzzle helper functions
def check_invalid_half(start, end):
    invalid_sum = 0
    for num in range(start, end + 1):
        str_num = str(num)
        if len(str_num) % 2 != 0:
            continue
        mid = len(str_num) // 2
        if str_num[:mid] == str_num[mid:]:
            invalid_sum += num
    return invalid_sum

def check_invalid(start, end):
    invalid_sum = 0
    for num in range(start, end + 1):
        str_num = str(num)
        _, size = get_repeating_pattern(str_num)
        if size > 0:
            invalid_sum += num
    return invalid_sum

def get_repeating_pattern(s: str):
    n = len(s)
    for size in range(1, n // 2 + 1):
        if n % size != 0:
            continue
        pattern = s[:size]
        if pattern * (n // size) == s:
            return pattern, n // size
    return 0, 0

# puzzle outputs
# print(example_input_a)
print("Example Output A: ", part_a(example_input_a), " Solution: ", part_a_example_solution)
print("Example Output B: ", part_b(example_input_b), " Solution: ", part_b_example_solution)
print("Part A: ", part_a(puzzle_data))
print("Part B: ", part_b(puzzle_data))
