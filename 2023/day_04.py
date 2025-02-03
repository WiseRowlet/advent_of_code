from aocd import get_puzzle

DAY = 4
YEAR = 2023

puzzle = get_puzzle(day=DAY, year=YEAR)
puzzle_data = puzzle.input_data
examples = puzzle.examples
example_input = examples[0].input_data
part_a_example_solution = examples[0].answer_a
part_b_example_solution = examples[0].answer_b


def parse_input(input_data):
    cards = []
    for line in input_data.splitlines():
        card = []
        numbers = line.split(": ")[1].split(" | ")
        winners = [int(n) for n in numbers[0].split(" ") if n != ""]
        picks = [int(n) for n in numbers[1].split(" ") if n != ""]
        card.append(winners)
        card.append(picks)
        card.append(1)
        cards.append(card)
    return cards


def part_a(input_data):
    cards = parse_input(input_data)
    score = 0
    for card in cards:
        winners, picks, _ = card
        exp = -1
        for winner in winners:
            if winner in picks:
                exp += 1
        if exp >= 0:
            score += 2**exp
    return score


def part_b(input_data):
    cards = parse_input(input_data)
    num_cards = len(cards)
    total_cards = 0
    for i, card in enumerate(cards):
        winners, picks, card_count = card
        total_cards += card_count
        matches = 0
        for winner in winners:
            if winner in picks:
                matches += 1
        if matches > 0:
            for match in range(matches):
                if i + match + 1 < num_cards:
                    cards[i + match + 1][2] += card_count
                else:
                    break
    return total_cards


# print(example_input)
print("Example Output A: ", part_a(example_input), " Solution: ", part_a_example_solution)
print("Example Output B: ", part_b(example_input), " Solution: ", part_b_example_solution)
print("Part A: ", part_a(puzzle_data))
print("Part B: ", part_b(puzzle_data))
