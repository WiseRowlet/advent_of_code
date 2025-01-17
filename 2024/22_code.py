def get_input(file_path):
    with open(file_path, "r") as file:
        return [int(line.strip()) for line in file]


input = get_input("Data/22_input.txt")
test_input = [1, 10, 100, 2024]
test_input_2 = [1, 2, 3, 2024]


# def mix(a, b):
#     return a ^ b


# def prune(a):
#     return a % 16777216


# def calculate_secret_number(a):
#     b = a * 64
#     s1 = prune(mix(a, b))
#     c = s1 // 32
#     s2 = prune(mix(s1, c))
#     d = s2 * 2048
#     s3 = prune(mix(s2, d))
#     return s3


# def calculate_nth_secret_number(a, n):
#     for _ in range(n):
#         a = calculate_secret_number(a)
#     return a


# def sum_of_secret_numbers(input_numbers, n):
#     secret_sum = 0
#     for number in input_numbers:
#         secret_sum += calculate_nth_secret_number(number, n)
#     return secret_sum


# def calculate_price_changes(input_numbers, steps):
#     price_sequences = []
#     for number in input_numbers:
#         prices = []
#         for _ in range(steps):
#             number = calculate_secret_number(number)
#             prices.append(number % 10)
#         changes = [prices[i + 1] - prices[i] for i in range(len(prices) - 1)]
#         price_sequences.append(changes)
#     return price_sequences


# def find_best_sequence(price_sequences):
#     from collections import defaultdict

#     sequence_scores = defaultdict(int)
#     for changes in price_sequences:
#         for i in range(len(changes) - 3):
#             seq = tuple(changes[i : i + 4])
#             sequence_scores[seq] += 1

#     best_sequence = None
#     max_bananas = 0
#     for seq, count in sequence_scores.items():
#         bananas = sum(
#             price_sequences[idx][seq_idx + 3]
#             for idx, seq_changes in enumerate(price_sequences)
#             for seq_idx in range(len(seq_changes) - 3)
#             if tuple(seq_changes[seq_idx : seq_idx + 4]) == seq
#         )
#         if bananas > max_bananas:
#             max_bananas = bananas
#             best_sequence = seq
#     return best_sequence, max_bananas


# def part_two(input_numbers):
#     steps = 2000
#     price_sequences = calculate_price_changes(input_numbers, steps)
#     best_sequence, max_bananas = find_best_sequence(price_sequences)
#     return best_sequence, max_bananas


# best_sequence, max_bananas = part_two(test_input_2)
# print(f"Best sequence: {best_sequence}, Maximum Bananas: {max_bananas}")


def step(secret):
    secret ^= (secret << 0x6) & 0xFFFFFF
    secret ^= (secret >> 0x5) & 0xFFFFFF
    secret ^= (secret << 0xB) & 0xFFFFFF
    return secret


def steps(secret, k=2000):
    for _ in range(k):
        secret = step(secret)
    return secret


def generate(secret, k=2000, modulus=10):
    sequence = [secret % modulus]
    for _ in range(k):
        secret = step(secret)
        sequence.append(secret % modulus)
    return sequence


def solve_part1(numbers):
    return sum([steps(n) for n in numbers])


def solve_part2(numbers, seq_len=4):
    total_bananas = {}
    for nums in [generate(number) for number in numbers]:
        seen = set()
        for i in range(len(nums) - seq_len):
            subseq = tuple([nums[i + 1 + k] - nums[i + k] for k in range(seq_len)])
            if subseq not in seen:
                seen.add(subseq)
                total_bananas[subseq] = total_bananas.get(subseq, 0) + nums[i + seq_len]
    return sorted([(v, k) for k, v in total_bananas.items()])[-1][0]


print(solve_part1(input))
print(solve_part2(input))
