from aocd import get_puzzle

DAY = 15
YEAR = 2023

puzzle = get_puzzle(day=DAY, year=YEAR)
puzzle_data = puzzle.input_data
examples = puzzle.examples
example_input = examples[0].input_data
part_a_example_solution = examples[0].answer_a
part_b_example_solution = examples[0].answer_b


def parse_input(input_data):
    return [code for code in input_data.split(",")]


def find_hash(code):
    value = 0
    for c in code:
        value = (value + ord(c)) * 17 % 256
    return value


def part_a(input_data):
    codes = parse_input(input_data)
    total = 0
    for code in codes:
        total += find_hash(code)
    return total


def part_b(input_data):
    codes = parse_input(input_data)
    boxes = {}

    for code in codes:
        if "-" in code:
            label = code.split("-", 1)[0]
            box = find_hash(label)
            if box in boxes:
                boxes[box].pop(label, None)
        else:
            label, lens = code.split("=", 1)
            box = find_hash(label)
            if box not in boxes:
                boxes[box] = {}
            boxes[box][label] = int(lens)

    total = 0
    for box, lenses in boxes.items():
        for i, focal in enumerate(lenses.values(), start=1):
            total += (box + 1) * i * focal

    return total


# print(example_input)
# print(parse_input(example_input))
print("Example Output A: ", part_a(example_input), " Solution: ", part_a_example_solution)
print("Example Output B: ", part_b(example_input), " Solution: ", part_b_example_solution)
print("Part A: ", part_a(puzzle_data))
print("Part B: ", part_b(puzzle_data))
