def get_towel_input(file_path):
    with open(file_path, "r") as file:
        towels = set(item.strip() for item in file.readline().strip().split(","))
        designs = []
        for i, line in enumerate(file):
            if i > 0:
                designs.append(line.strip())
    return towels, designs


def check_possible_design(design, towels, count_designs=False):
    design_length = len(design)
    dp = [False] * (design_length + 1)
    dp[0] = True
    for i in range(1, design_length + 1):
        for j in range(i):
            if not count_designs and dp[j] and design[j:i] in towels:
                dp[i] = True
                break
            if design[j:i] in towels:
                dp[i] += dp[j]

    return dp[design_length]


def count_possible_designs(file_path, count_designs=False):
    towels, designs = get_towel_input(file_path)
    count = 0
    for design in designs:
        if count_designs:
            count += check_possible_design(design, towels, True)
        else:
            if check_possible_design(design, towels):
                count += 1
    return count


# print(count_possible_designs("2024/Data/19_input.txt"))
print(count_possible_designs("2024/Data/19_input.txt", True))
