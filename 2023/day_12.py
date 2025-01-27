from collections import deque
from functools import cache

from aocd import get_puzzle

DAY = 12
YEAR = 2023

puzzle = get_puzzle(day=DAY, year=YEAR)
puzzle_data = puzzle.input_data
examples = puzzle.examples
example_input = examples[0].input_data
part_a_example_solution = examples[0].answer_a
part_b_example_solution = examples[0].answer_b


@cache
def dfs(sequence, groups):
    if not groups:
        return "#" not in sequence
    seq_len = len(sequence)
    group_len = groups[0]
    if seq_len - sum(groups) - len(groups) + 1 < 0:
        return 0
    has_holes = any(sequence[x] == "." for x in range(group_len))
    if seq_len == group_len:
        return 0 if has_holes else 1
    can_use = not has_holes and (sequence[group_len] != "#")
    if sequence[0] == "#":
        return dfs(sequence[group_len + 1 :].lstrip("."), tuple(groups[1:])) if can_use else 0
    skip = dfs(sequence[1:].lstrip("."), groups)
    if not can_use:
        return skip
    return skip + dfs(sequence[group_len + 1 :].lstrip("."), tuple(groups[1:]))


# Did it with Deque at first but it was too slow for the larger input
# @cache
# def bfs(sequence, groups):
#     valid = 0
#     queue = deque([(sequence.lstrip("."), 0, "")])
#     while queue:
#         # print(queue)
#         current, group, full = queue.popleft()
#         if (len(current) == 0 or current.count("#") == 0) and group == len(groups):
#             # print("Valid", full)
#             valid += 1
#             continue
#         if group >= len(groups):
#             continue
#         group_len = groups[group]

#         # Skip invalid states early
#         if len(current) < group_len:
#             continue
#         if len(current) < len(groups[group:]) - 1 + sum(groups[group:]):
#             continue
#         has_holes = any(current[x] == "." for x in range(group_len))
#         skip = (len(current) > group_len and current[group_len] == "#") or has_holes

#         # Process valid transitions
#         if current[0] == "#":
#             if skip:
#                 continue
#             queue.append((current[group_len + 1 :].lstrip("."), group + 1, full + "#" * group_len + "."))
#         else:
#             # current[0] == "?"
#             queue.append((current[1:].lstrip("."), group, full + "."))
#             if not skip:
#                 queue.append((current[group_len + 1 :].lstrip("."), group + 1, full + "#" * group_len + "."))

#     # print(sequence, groups, valid)
#     return valid


def parse_input(input_data):
    springs = []
    arrangements = []
    for line in input_data.splitlines():
        springs.append(line.split(" ")[0])
        arrangements.append([int(n) for n in line.split(" ")[1].split(",")])
    return springs, arrangements


def part_a(input_data, fold=0):
    springs, arrangements = parse_input(input_data)
    if fold > 0:
        for i, spring in enumerate(springs):
            springs[i] = "?".join([spring] * fold)
            arrangements[i] = arrangements[i] * fold
    sum_valid = 0
    for i, spring in enumerate(springs):
        sum_valid += dfs(spring, tuple(arrangements[i]))

    return sum_valid


def part_b(input_data):
    return part_a(input_data, 5)


# print(example_input)
# print(parse_input(example_input))
print("Example Output A: ", part_a(example_input, 0))
print("Example Output B: ", part_b(example_input))
print("Part A: ", part_a(puzzle_data))
print("Part B: ", part_b(puzzle_data))
