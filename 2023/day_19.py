import re
from collections import defaultdict, deque

from aocd import get_puzzle

DAY = 19
YEAR = 2023

puzzle = get_puzzle(day=DAY, year=YEAR)
puzzle_data = puzzle.input_data
examples = puzzle.examples
example_input = examples[0].input_data
part_a_example_solution = examples[0].answer_a
part_b_example_solution = examples[0].answer_b


def parse_input(input_data):
    blocks = input_data.split("\n\n")
    parts = []
    properties = {
        "x": 0,
        "m": 1,
        "a": 2,
        "s": 3,
    }

    wf = defaultdict(list)
    for part in blocks[1].splitlines():
        match = re.search(r"{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}", part)
        parts.append([int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4))])

    for line in blocks[0].splitlines():
        key = line.split("{")[0]
        ins = line.split("{")[1][:-1]
        ins_sp = ins.split(",")
        p = []

        for i in ins_sp:
            steps = i.split(":")
            if len(steps) > 1:
                step = (properties[steps[0][0]], steps[0][1], int(steps[0][2:]), steps[1])
            else:
                step = (steps[0],)
            p.append(step)
        wf[key] = p

    return wf, parts


def part_a(input_data):
    wfs, parts = parse_input(input_data)
    accepted = []
    for p in parts:
        k = "in"
        while True:
            wf = wfs[k]
            for s in wf:
                if len(s) > 1:
                    if s[1] == ">":
                        if p[s[0]] > s[2]:
                            k = s[3]
                            break
                    else:
                        if p[s[0]] < s[2]:
                            k = s[3]
                            break
                else:
                    k = s[0]
            if k == "A":
                accepted.append(p)
                break
            if k == "R":
                break

    return sum([sum(p) for p in accepted])


def part_b(input_data):
    wfs, _ = parse_input(input_data)
    accepted = []
    queue = deque()
    queue.append(([(1, 4000), (1, 4000), (1, 4000), (1, 4000)], "in"))
    while queue:
        p, k = queue.popleft()
        wf = wfs[k]
        splits = []
        for s in wf:
            if len(s) > 1:
                left, right = p[s[0]]
                if s[1] == ">":
                    if right > s[2]:
                        p1 = p.copy()
                        p[s[0]] = (left, s[2])
                        if s[2] + 1 != right:
                            p1[s[0]] = (s[2] + 1, right)
                        else:
                            p1[s[0]] = (right, right)
                        splits.append((p1, s[3]))
                else:
                    if left < s[2]:
                        p1 = p.copy()
                        p[s[0]] = (s[2], right)
                        if s[2] - 1 != left:
                            p1[s[0]] = (left, s[2] - 1)
                        else:
                            p1[s[0]] = (left, left)
                        splits.append((p1, s[3]))
            else:
                splits.append((p, s[0]))
        for split in splits:
            p, k = split
            if k == "A":
                accepted.append(p)
            elif k == "R":
                continue
            else:
                queue.append((p, k))
    sum = 0
    for p in accepted:
        p_sum = 1
        for c in p:
            p_sum *= c[1] - c[0] + 1
        sum += p_sum
    return sum


# print(example_input)
# print(parse_input(example_input))
print("Example Output A: ", part_a(example_input), " Solution: ", part_a_example_solution)
print("Example Output B: ", part_b(example_input), " Solution: ", part_b_example_solution)
print("Part A: ", part_a(puzzle_data))
print("Part B: ", part_b(puzzle_data))
