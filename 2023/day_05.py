import re

from aocd import get_puzzle

DAY = 5
YEAR = 2023

puzzle = get_puzzle(day=DAY, year=YEAR)
puzzle_input = puzzle.input_data
examples = puzzle.examples
example_input = examples[0].input_data
part_a_example_solution = examples[0].answer_a
part_b_example_solution = examples[0].answer_b


def part1(puzzle_input):
    segments = puzzle_input.split("\n\n")
    seeds = re.findall(r"\d+", segments[0])

    min_location = float("inf")
    for x in map(int, seeds):
        for seg in segments[1:]:
            for conversion in re.findall(r"(\d+) (\d+) (\d+)", seg):
                destination, start, delta = map(int, conversion)
                if x in range(start, start + delta):
                    x += destination - start
                    break

        min_location = min(x, min_location)

    return min_location


def part2(puzzle_input):
    segments = puzzle_input.split("\n\n")
    intervals = []

    for seed in re.findall(r"(\d+) (\d+)", segments[0]):
        x1, dx = map(int, seed)
        x2 = x1 + dx
        intervals.append((x1, x2, 1))

    min_location = float("inf")
    while intervals:
        x1, x2, level = intervals.pop()
        if level == 8:
            min_location = min(x1, min_location)
            continue

        for conversion in re.findall(r"(\d+) (\d+) (\d+)", segments[level]):
            z, y1, dy = map(int, conversion)
            y2 = y1 + dy
            diff = z - y1
            if x2 <= y1 or y2 <= x1:  # no overlap
                continue
            if x1 < y1:  # split original interval at y1
                intervals.append((x1, y1, level))
                x1 = y1
            if y2 < x2:  # split original interval at y2
                intervals.append((y2, x2, level))
                x2 = y2
            intervals.append(
                (x1 + diff, x2 + diff, level + 1)
            )  # perfect overlap -> make conversion and let pass to next nevel
            break

        else:
            intervals.append((x1, x2, level + 1))

    return min_location


# print(example_input)
print("Example Output A: ", part1(example_input), " Solution: ", part_a_example_solution)
print("Example Output B: ", part2(example_input), " Solution: ", part_b_example_solution)
print("Part A: ", part1(puzzle_input))
print("Part B: ", part2(puzzle_input))
