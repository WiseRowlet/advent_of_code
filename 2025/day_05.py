# aocd import
from aocd import get_puzzle
DAY = 5
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
    ran, ingr = input_data.split("\n\n")
    s_ingr = [int(x) for x in ingr.splitlines()]
    s_ran = set()
    l_ran = ran.splitlines()
    for i in range(len(l_ran)):
        left, right = l_ran[i].split("-")
        s_ran.add((int(left), int(right)))
    
    return s_ran, s_ingr

# puzzle imports

# puzzle solutions
def part_a(input_data):
    ranges, ingredients = parse_input(input_data)
    total = 0
    for ingr in ingredients:
        for r in ranges:
            if ingr >= r[0] and ingr <= r[1]:
                total += 1
                break
    return total

def part_b(input_data):
    ranges, _ = parse_input(input_data)
    
    return count_unique_ints(ranges)

# puzzle helper functions
def count_unique_ints(ranges):
    if not ranges:
        return 0

    # Sort by start
    ranges = sorted(ranges, key=lambda t: t[0])

    merged = []
    cur_start, cur_end = ranges[0]

    for start, end in ranges[1:]:
        if start <= cur_end + 1:
            # Overlapping or touching → merge
            cur_end = max(cur_end, end)
        else:
            # Push finished segment and start a new one
            merged.append((cur_start, cur_end))
            cur_start, cur_end = start, end

    merged.append((cur_start, cur_end))

    # Count integers in merged closed intervals
    return sum(e - s + 1 for s, e in merged)

# puzzle outputs
# print(example_input_a)
print("Example Output A: ", part_a(example_input_a), " Solution: ", part_a_example_solution)
print("Example Output B: ", part_b(example_input_b), " Solution: ", part_b_example_solution)
print("Part A: ", part_a(puzzle_data))
print("Part B: ", part_b(puzzle_data))
