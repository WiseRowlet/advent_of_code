from collections import Counter

stones = [0, 7, 6618216, 26481, 885, 42, 202642, 8791]
stones_test = [125, 17]


def blink_counter(stone_counter):
    next_stones = Counter()

    for stone, count in stone_counter.items():
        if stone == 0:
            next_stones[1] += count
        else:
            str_stone = str(stone)
            if len(str_stone) % 2 == 0:
                half = len(str_stone) // 2
                left, right = int(str_stone[:half]), int(str_stone[half:])
                next_stones[left] += count
                next_stones[right] += count
            else:
                next_stones[stone * 2024] += count

    return next_stones


def count_stones_counter(stones, num_blinks):
    stone_counter = Counter(stones)
    for _ in range(num_blinks):
        stone_counter = blink_counter(stone_counter)
    return sum(stone_counter.values())


num_stones = count_stones_counter(stones, 75)

print(num_stones)
