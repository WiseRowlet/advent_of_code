from aocd import get_puzzle

DAY = 1
YEAR = 2024

puzzle = get_puzzle(day=DAY, year=YEAR)
puzzle_data = puzzle.input_data
examples = puzzle.examples
example_input = examples[0].input_data
part_a_example_solution = examples[0].answer_a
part_b_example_solution = examples[0].answer_b


def parse_input(input_data):
    left = []
    right = []
    for line in input_data.splitlines():
        left.append(int(line.split("   ")[0]))
        right.append(int(line.split("   ")[1]))
    return sorted(left), sorted(right)


def part_a(input_data):
    left, right = parse_input(input_data)
    sum = 0
    for i in range(len(left)):
        sum += abs(left[i] - right[i])
    return sum


def part_b(input_data):
    left, right = parse_input(input_data)
    similarity = 0
    for num in left:
        similarity += num * right.count(num)
    return similarity


print(example_input)
print(parse_input(example_input))
print("Example Output A: ", part_a(example_input))
print("Example Output B: ", part_b(example_input))
print("Part A: ", part_a(puzzle_data))
print("Part B: ", part_b(puzzle_data))
