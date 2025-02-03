import math
from collections import deque
from itertools import count

from aocd import get_puzzle

DAY = 20
YEAR = 2023

puzzle = get_puzzle(day=DAY, year=YEAR)
puzzle_data = puzzle.input_data
examples = puzzle.examples
example_input_0 = examples[0].input_data
example_input_1 = examples[1].input_data
part_a_example_solution_0 = examples[0].answer_a
part_a_example_solution_1 = examples[1].answer_a
part_b_example_solution_0 = examples[0].answer_b
part_b_example_solution_1 = examples[0].answer_b


def parse_input(input_data):
    modules = {}
    conjunctions = []
    for line in input_data.splitlines():
        k = line.split(" -> ")[0]
        v = line.split(" -> ")[1]
        module = {}

        if k == "broadcaster":
            module["type"] = "broadcaster"
            module["outputs"] = v.split(", ")
        elif k[0] == "%":
            module["type"] = k[0]
            module["outputs"] = v.split(", ")
            module["switch"] = False
            k = k[1:]
        elif k[0] == "&":
            module["type"] = k[0]
            module["outputs"] = v.split(", ")
            module["inputs"] = {}
            k = k[1:]
            conjunctions.append(k)
        modules[k] = module
    for c in conjunctions:
        for k, v in modules.items():
            if c in v["outputs"]:
                modules[c]["inputs"][k] = False
    return modules


def press_button(modules):
    low_pulses = 0
    high_pulses = 0
    queue = [("broadcaster", False)]
    while True:
        new_m = []
        new_flips = set()
        new_memory = set()
        for m, pulse in queue:
            if pulse:
                high_pulses += 1
            else:
                low_pulses += 1
            if m in modules:
                mod_type = modules[m]["type"]
                if mod_type == "broadcaster":
                    for output in modules[m]["outputs"]:
                        new_m.append((output, pulse))
                        if modules[output]["type"] == "&":
                            new_memory.add((m, output, pulse))
                elif mod_type == "%":
                    if not pulse:
                        switch = modules[m]["switch"]
                        new_flips.add(m)
                        for output in modules[m]["outputs"]:
                            if switch:
                                new_m.append((output, False))
                                if output in modules and modules[output]["type"] == "&":
                                    new_memory.add((m, output, False))
                            else:
                                new_m.append((output, True))
                                if output in modules and modules[output]["type"] == "&":
                                    new_memory.add((m, output, True))
                elif mod_type == "&":
                    p = all([v for v in modules[m]["inputs"].values()])
                    for output in modules[m]["outputs"]:
                        new_m.append((output, not p))
                        if output in modules and modules[output]["type"] == "&":
                            new_memory.add((m, output, not p))

        if len(new_memory) > 0:
            for m, output, pulse in new_memory:
                modules[output]["inputs"][m] = pulse

        if len(new_flips) > 0:
            for flip in new_flips:
                modules[flip]["switch"] = not modules[flip]["switch"]

        if len(new_m) > 0:
            queue = new_m
        else:
            break

    return modules, low_pulses, high_pulses


def part_a(input_data):
    modules = parse_input(input_data)
    total_low_pulses = 0
    total_high_pulses = 0
    for _ in range(1000):
        modules, low_pulses, high_pulses = press_button(modules)
        total_low_pulses += low_pulses
        total_high_pulses += high_pulses
    return total_low_pulses * total_high_pulses


def part_b(input_data):
    graph = {}
    flip_flop = {}
    memory = {}
    for line in input_data.split("\n"):
        source, destinations = line.split(" -> ")
        destinations = destinations.split(", ")
        graph[source.lstrip("%&")] = destinations
        if source.startswith("%"):
            flip_flop[source[1:]] = 0  # each flip flip is off (0) by default
        elif source.startswith("&"):
            memory[source[1:]] = {}

    for conjunction in memory.keys():  # get source modules for conjunctions
        for source, destinatons in graph.items():
            if conjunction in destinatons:
                memory[conjunction][source] = 0  # initialize memory at low (0)

    final_layer = [m1 for m1 in graph if "rx" in graph[m1]]
    assert len(final_layer) == 1, "Assumption #1: There is only 1 module pointing to rx"
    assert final_layer[0] in memory, "Assumption #2: The final module before rx is a conjunction"

    semi_final_layer = set(module for module in graph if final_layer[0] in graph[module])
    cycle_lengths = []  # Assumption #3: The modules on semi_final_layer signal high in regular intervals / cycles

    for button_push in count(1):
        queue = deque([("broadcaster", in_module, 0) for in_module in graph["broadcaster"]])
        while queue:
            out_module, in_module, signal = queue.popleft()

            if in_module in flip_flop and signal == 0:
                flip_flop[in_module] = 1 - flip_flop[in_module]
                out_signal = flip_flop[in_module]

            elif in_module in memory:
                memory[in_module][out_module] = signal
                out_signal = 1 if 0 in memory[in_module].values() else 0
                if in_module in semi_final_layer and out_signal == 1:
                    cycle_lengths.append(button_push)
                    semi_final_layer.remove(in_module)

            else:  # no output
                continue

            queue.extend([(in_module, nxt, out_signal) for nxt in graph[in_module]])

        if not semi_final_layer:
            break

    return math.lcm(*cycle_lengths)


# print(example_input_1)
# print(parse_input(example_input_1))
print("Example Output A-0: ", part_a(example_input_0), " Solution: ", part_a_example_solution_0)
print("Example Output A-1: ", part_a(example_input_1), " Solution: ", part_a_example_solution_1)
# print("Example Output B-0: ", part_b(example_input_0), " Solution: ", part_b_example_solution_0)
# print("Example Output B-1: ", part_b(example_input_1), " Solution: ", part_b_example_solution_1)
print("Part A: ", part_a(puzzle_data))
print("Part B: ", part_b(puzzle_data))
