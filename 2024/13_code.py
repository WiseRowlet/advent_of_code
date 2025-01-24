import re


def parse_input(input_text):
    results = []
    # Split the input into blocks, one per Button/Prize group
    blocks = input_text.strip().split("\n\n")

    for block in blocks:
        # Extract Button A, Button B, and Prize coordinates using regex
        match_a = re.search(r"Button A: X\+(\d+), Y\+(\d+)", block)
        match_b = re.search(r"Button B: X\+(\d+), Y\+(\d+)", block)
        match_prize = re.search(r"Prize: X=(\d+), Y=(\d+)", block)

        if match_a and match_b and match_prize:
            button_a = (int(match_a.group(1)), int(match_a.group(2)))
            button_b = (int(match_b.group(1)), int(match_b.group(2)))
            prize = (int(match_prize.group(1)), int(match_prize.group(2)))

            # Append the dictionary for this block
            results.append({"A": button_a, "B": button_b, "Prize": prize})

    return results


def get_input(file_path):
    with open(file_path, "r") as file:
        arcade_machines = parse_input(file.read())
    return arcade_machines


test_input = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""

test_machines = parse_input(test_input)
arcade_machines = get_input("2024/Data/13_input.txt")


def press_button(position, arcade_machine, button):
    position_x, position_y = position
    button_x, button_y = arcade_machine[button]
    return (position_x + button_x, position_y + button_y)


def min_tokens_brute(arcade_machine):
    a_x, a_y = arcade_machine["A"]
    p_x, p_y = arcade_machine["Prize"]

    position = (0, 0)
    count_b_presses = 0
    i = 0
    possible_press = {}
    while i < 100:
        position = press_button(position, arcade_machine, "B")
        count_b_presses += 1
        position_x, position_y = position
        if position_x > p_x or position_y > p_y:
            break
        if (
            (p_x - position_x) % a_x == 0
            and (p_y - position_y) % a_y == 0
            and (p_x - position_x) / a_x == (p_y - position_y) / a_y
        ):
            possible_press = {
                "A": (p_x - position_x) // a_x,
                "B": count_b_presses,
            }
        i += 1
    if possible_press:
        min_tokens = possible_press["A"] * 3 + possible_press["B"] * 1
    else:
        min_tokens = 0
    return min_tokens


def min_tokens(arcade_machine, offset=0):
    a_x, a_y = arcade_machine["A"]
    b_x, b_y = arcade_machine["B"]
    p_x, p_y = arcade_machine["Prize"]
    p_x += offset
    p_y += offset

    det = a_x * b_y - a_y * b_x
    if det == 0:
        return 0

    a = (p_x * b_y - p_y * b_x) // det
    b = (a_x * p_y - a_y * p_x) // det

    if a_x * a + b_x * b == p_x and a_y * a + b_y * b == p_y:
        return a * 3 + b * 1
    return 0


def total_tokens_brute(arcade_machines):
    total = 0
    for machine in arcade_machines:
        total += min_tokens_brute(machine)
    return total


def total_tokens(arcade_machines, offset=0):
    total = 0
    for machine in arcade_machines:
        total += min_tokens(machine, offset)
    return total


offset = 0
offset = 10000000000000
print(total_tokens(test_machines, offset))
print(total_tokens(arcade_machines, offset))
