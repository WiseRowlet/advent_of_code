from aocd import get_puzzle

DAY = 5
YEAR = 2023

puzzle = get_puzzle(day=DAY, year=YEAR)
puzzle_data = puzzle.input_data
examples = puzzle.examples
example_input = examples[0].input_data
part_a_example_solution = examples[0].answer_a
part_b_example_solution = examples[0].answer_b


def parse_input(input_data):
    plots = []
    seeds = []
    lines = input_data.splitlines()
    seeds = list(map(int, lines[0].split(": ")[1].split(" ")))
    plot = []
    for line in lines[1:]:
        if line == "":
            continue
        if line[0].isalpha():
            if len(plot) > 0:
                plots.append(plot)
                plot = []
        else:
            plot.append(list(map(int, line.split(" "))))
    plots.append(plot)

    return seeds, plots


def part_a(seeds, plots):
    locations = []
    for seed in seeds:
        location = seed
        for plot in plots:
            for tran in plot:
                dest, src, rng = tran[0], tran[1], tran[2]
                if src <= location < src + rng:
                    location = dest + location - src
                    break
        locations.append(location)
    return min(locations)


def part_b(seeds, plots):
    new_seeds = set()
    i = 0
    while i + 1 < len(seeds):
        for j in range(seeds[i], seeds[i] + seeds[i + 1]):
            new_seeds.add(j)
        i += 2
    # return part_a(new_seeds, plots)
    return len(new_seeds)


seeds, plots = parse_input(puzzle_data)
print(part_a(seeds, plots))
print(part_b(seeds, plots))
