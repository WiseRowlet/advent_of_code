import re
from collections import defaultdict


def get_input(file_path):
    wires = defaultdict(int)
    gates = set()

    with open(file_path) as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        wire_match = re.match(r"(\w+): (\d+)", line)
        gate_match = re.match(r"(\w+) (\w+) (\w+) -> (\w+)", line)
        if wire_match:
            wire, value = wire_match.groups()
            wires[wire] = int(value)
        elif gate_match:
            a, op, b, result = gate_match.groups()
            if a not in wires:
                wires[a] = None
            if b not in wires:
                wires[b] = None
            if result not in wires:
                wires[result] = None
            gates.update([(a, b, op, result)])

    return wires, gates


def count_null_wires(wires):
    return sum(1 for wire in wires if wires[wire] is None)


def connect_gates(wires, gates):
    while count_null_wires(wires) > 0:
        for a, b, op, result in gates:
            if wires[a] is not None and wires[b] is not None and wires[result] is None:
                if op == "AND":
                    wires[result] = wires[a] & wires[b]
                elif op == "OR":
                    wires[result] = wires[a] | wires[b]
                elif op == "XOR":
                    wires[result] = wires[a] ^ wires[b]
    return wires


def get_result(wires):
    return "".join(str(wires[key]) for key in sorted([key for key in wires if key.startswith("z")], reverse=True))


def part_one(file_path):
    wires, gates = get_input(file_path)
    wires = connect_gates(wires, gates)
    return int(get_result(wires), 2)


def get_target_result(wires):
    binary_x = "".join(str(wires[key]) for key in sorted([key for key in wires if key.startswith("x")], reverse=True))
    binary_y = "".join(str(wires[key]) for key in sorted([key for key in wires if key.startswith("y")], reverse=True))
    numeric_z = int(binary_x, 2) + int(binary_y, 2)
    return format(numeric_z, "b")


def part_two(file_path):
    wires, gates = get_input(file_path)
    highest_z_int = max(int(wire[1:]) for wire in wires if wire.startswith("z"))
    highest_z = f"z{highest_z_int:02}"
    wrong = set()
    for a, b, op, result in gates:
        if result[0] == "z" and op != "XOR" and result != highest_z:
            wrong.add(result)
        if (
            op == "XOR"
            and result[0] not in ["x", "y", "z"]
            and a[0] not in ["x", "y", "z"]
            and b[0] not in ["x", "y", "z"]
        ):
            wrong.add(result)
        if op == "AND" and "x00" not in [a, b]:
            for suba, subb, subop, _ in gates:
                if (result == suba or result == subb) and subop != "OR":
                    wrong.add(result)
        if op == "XOR":
            for suba, subb, subop, _ in gates:
                if (result == suba or result == subb) and subop == "OR":
                    wrong.add(result)

    return ",".join(sorted(wrong))


test_path = "Data/24_input_test.txt"
test_path_2 = "Data/24_input_test_2.txt"
path = "Data/24_input.txt"

print(part_one(path))
print(part_two(path))
