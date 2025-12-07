# aocd import
from aocd import get_puzzle
DAY = 6
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
    # Split into non-empty rows, splitting on any whitespace
    rows = [line.split() for line in input_data.splitlines() if line.strip()]
    if not rows:
        return []

    # All rows except the last are numeric
    num_rows = rows[:-1]
    ops = rows[-1]

    columns = [list(map(int, col)) for col in zip(*num_rows)]

    return columns, ops

# puzzle imports

# puzzle solutions
def part_a(input_data):
    columns, ops = parse_input(input_data)
    if len(columns) != len(ops):
        print("Error: number of columns and operations do not match")
        print(len(columns), len(ops))
        return 0

    return weird_math(columns, ops)

def part_b(input_data):
    rows, ranges = parse_grid(input_data)
    num_rows = rows[:-1]
    ops_row = rows[-1]

    total = 0
    problems = []  # for debugging / sanity check

    for start, end in ranges:
        # operator: any non-space in that horizontal slice of the last row
        op = next(ch for ch in ops_row[start:end] if ch != " ")

        numbers = []
        # columns right-to-left within this problem
        for c in reversed(range(start, end)):
            digits = "".join(
                row[c] for row in num_rows
                if row[c] != " "
            )
            if digits:
                numbers.append(int(digits))

        problems.append((op, numbers))

        if op == "+":
            val = sum(numbers)
        elif op == "*":
            val = 1
            for n in numbers:
                val *= n
        else:
            raise ValueError(f"Unknown op {op!r}")

        total += val

    return total

# puzzle helper functions
def parse_grid(text: str):
    rows = text.splitlines()
    width = len(rows[0])
    # separator columns: all rows have a space here
    seps = [c for c in range(width) if all(r[c] == " " for r in rows)]
    bounds = [-1] + seps + [width]

    # ranges for problems: [start, end)
    problem_ranges = [
        (a + 1, b)
        for a, b in zip(bounds, bounds[1:])
        if b - a > 1
    ]
    return rows, problem_ranges

def weird_math(values, ops):
    total = 0
    for i in range(len(ops)):
        if ops[i] == "+":
            total += sum(values[i])
        elif ops[i] == "*":
            prod = 1
            for v in values[i]:
                prod *= v
            total += prod
    return total

# puzzle outputs
# print(example_input_a)
print("Example Output A: ", part_a(example_input_a), " Solution: ", part_a_example_solution)
print("Example Output B: ", part_b(example_input_b), " Solution: ", part_b_example_solution)
print("Part A: ", part_a(puzzle_data))
print("Part B: ", part_b(puzzle_data))
