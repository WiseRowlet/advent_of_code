from collections import Counter, defaultdict

from aocd import get_puzzle

DAY = 7
YEAR = 2023

puzzle = get_puzzle(day=DAY, year=YEAR)
puzzle_data = puzzle.input_data
examples = puzzle.examples
example_input = examples[0].input_data
part_a_example_solution = examples[0].answer_a
part_b_example_solution = examples[0].answer_b


def card_value(label, jokers=None):
    if label == jokers:
        return 1
    if label.isnumeric():
        return int(label)
    if label == "T":
        return 10
    if label == "J":
        return 11
    if label == "Q":
        return 12
    if label == "K":
        return 13
    if label == "A":
        return 14
    return 0


def parse_input(input_data):
    hands = defaultdict(int)
    for line in input_data.splitlines():
        hand, bid = line.split(" ")
        hands[hand] = int(bid)
    return hands


def calculate_score_camel(hand, jokers=None):
    score = 0
    c = Counter(hand)
    if jokers:
        joker = jokers
        num_jokers = c[joker]
    else:
        joker = None
        num_jokers = 0
    mc = sorted(c.items(), key=lambda item: (item[0] == joker, -item[1]))

    if (mc[0][1] + num_jokers == 5) or mc[0][0] == joker:
        score = 600000000000
    elif mc[0][1] + num_jokers == 4:
        score = 500000000000
    elif (mc[0][1] + num_jokers == 3 and mc[1][1] == 2) or (mc[0][1] == 3 and mc[1][1] + num_jokers == 2):
        score = 400000000000
    elif mc[0][1] + num_jokers == 3:
        score = 300000000000
    elif (mc[0][1] + num_jokers == 2 and mc[1][1] == 2) or (mc[0][1] == 2 and mc[1][1] + num_jokers == 2):
        score = 200000000000
    elif mc[0][1] == 2 or num_jokers == 1:
        score = 100000000000

    base = 1000000000
    for card in hand:
        score += card_value(card, jokers) * base
        base //= 100
    return score


def part_a(input_data, jokers=None):
    hands = parse_input(input_data)
    bids = [bid for _, bid in sorted(hands.items(), key=lambda item: calculate_score_camel(item[0], jokers))]
    i = 1
    winnings = 0
    for bid in bids:
        winnings += bid * i
        i += 1
    return winnings


def part_b(input_data):
    return part_a(input_data, jokers="J")


# print(example_input)
print("Example Output A: ", part_a(example_input), " Solution: ", part_a_example_solution)
print("Example Output B: ", part_b(example_input), " Solution: ", part_b_example_solution)
print("Part A: ", part_a(puzzle_data))
print("Part B: ", part_b(puzzle_data))
