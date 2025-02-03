from collections import defaultdict

from aocd import get_puzzle

DAY = 2
YEAR = 2023

puzzle = get_puzzle(day=DAY, year=YEAR)
puzzle_data = puzzle.input_data
examples = puzzle.examples
example_input = examples[0].input_data
part_a_example_solution = examples[0].answer_a
part_b_example_solution = examples[0].answer_b


def parse_input(input_data):
    games = []
    for line in input_data.splitlines():
        pulls = line.split(": ")[1].split("; ")
        game = []
        for pull in pulls:
            cubes = defaultdict(int)
            for cube in pull.split(", "):
                count, color = cube.split(" ")
                cubes[color] = int(count)
            game.append(cubes)
        games.append(game)
    return games


def part_a(input_data):
    games = parse_input(input_data)
    enumerator = [i + 1 for i in range(len(games))]
    possible = [0] * len(games)
    total = {
        "red": 12,
        "blue": 14,
        "green": 13,
    }
    for i in range(len(games)):
        max_red = max(games[i], key=lambda x: x["red"])["red"]
        max_blue = max(games[i], key=lambda x: x["blue"])["blue"]
        max_green = max(games[i], key=lambda x: x["green"])["green"]
        if max_red <= total["red"] and max_blue <= total["blue"] and max_green <= total["green"]:
            possible[i] = 1
    return sum([a * b for a, b in zip(enumerator, possible)])


def part_b(input_data):
    games = parse_input(input_data)
    power_sum = 0
    for game in games:
        max_red = max(game, key=lambda x: x["red"])["red"]
        max_blue = max(game, key=lambda x: x["blue"])["blue"]
        max_green = max(game, key=lambda x: x["green"])["green"]
        power_sum += max_red * max_blue * max_green

    return power_sum


# print(example_input)
print("Example Output A: ", part_a(example_input), " Solution: ", part_a_example_solution)
print("Example Output B: ", part_b(example_input), " Solution: ", part_b_example_solution)
print("Part A: ", part_a(puzzle_data))
print("Part B: ", part_b(puzzle_data))
