import re

from aocd import get_puzzle

DAY = 6
YEAR = 2023

puzzle = get_puzzle(day=DAY, year=YEAR)
puzzle_data = puzzle.input_data
examples = puzzle.examples
example_input = examples[0].input_data
part_a_example_solution = examples[0].answer_a
part_b_example_solution = examples[0].answer_b

"""
constant time = t
record distance = d

Equations
x + y = t
y * x > d

x and y are positive integers

x = t - y
y * (t - y) > d
y * t - y^2 > d
y^2 - y * t + d < 0
y = (-b + sqrt(b^2 - 4ac)) / 2a
y = (t + sqrt(t^2 - 4d)) / 2
"""


def parse_input_a(input_data):
    lines = []
    races = []
    for line in input_data.splitlines():
        lines.append(line)
    times = re.findall(r"\d+", lines[0])
    distances = re.findall(r"\d+", lines[1])
    for i in range(len(times)):
        race = (int(times[i]), int(distances[i]))
        races.append(race)
    return races


def parse_input_b(input_data):
    lines = []
    races = []
    for line in input_data.splitlines():
        lines.append(line)
    times = re.findall(r"\d+", lines[0])
    distances = re.findall(r"\d+", lines[1])
    time = "".join(times)
    distance = "".join(distances)
    races.append((int(time), int(distance)))
    return races


def part_a(races):
    m = 1
    for t, d in races:
        y_temp = (t + (t**2 - 4 * d) ** 0.5) / 2
        if y_temp.is_integer():
            y = int(y_temp) - 1
        else:
            y = y_temp // 1
        x = (t - y_temp) // 1
        m *= int(y) - int(x)
    return m


def part_b(races):
    return part_a(races)


races_a = parse_input_a(puzzle_data)
races_b = parse_input_b(puzzle_data)

print(part_a(races_a))
print(part_b(races_b))
