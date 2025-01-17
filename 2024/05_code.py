import csv

with open("Data/05_input_rules.txt", "r") as file:
    rules = [tuple(map(int, line.split("|"))) for line in file]

updates = []
with open("Data/05_input.csv", mode="r") as file:
    reader = csv.reader(file)
    for row in reader:
        updates.append([int(value) for value in row])


def check_rule(rule, update):
    try:
        index_0 = update.index(rule[0])
    except ValueError:
        index_0 = -1
    try:
        index_1 = update.index(rule[1])
    except ValueError:
        index_1 = -1

    if index_0 == -1 or index_1 == -1:
        return True
    elif index_0 < index_1:
        return True
    else:
        return False


def find_middle_elements(arr):
    if not arr:
        return None
    middle_index = len(arr) // 2
    if len(arr) % 2 == 0:
        return arr[middle_index - 1 : middle_index + 1]
    else:
        return [arr[middle_index]]


def check_update(rules, update):
    for rule in rules:
        if not check_rule(rule, update):
            return False
    return True


def classify_updates(rules, updates):
    correct_updates = []
    incorrect_updates = []
    for update in updates:
        if not check_update(rules, update):
            incorrect_updates.append(update)
        else:
            correct_updates.append(update)
    return correct_updates, incorrect_updates


def fix_update(rules, update):
    correct = False
    while not correct:
        for i in range(len(update[:-1])):
            for rule in rules:
                if rule[1] == update[i] and rule[0] == update[i + 1]:
                    update[i], update[i + 1] = update[i + 1], update[i]
        correct = check_update(rules, update)
    return update


def fix_updates(rules, updates):
    fixed_updates = []
    for update in updates:
        fixed_updates.append(fix_update(rules, update))
    return fixed_updates


def total_updates(updates):
    total_updates = 0
    for update in updates:
        total_updates += sum(find_middle_elements(update))
    return total_updates


correct_updates, incorrect_updates = classify_updates(rules, updates)

print(total_updates(correct_updates))
print(total_updates(fix_updates(rules, incorrect_updates)))
