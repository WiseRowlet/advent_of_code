import csv


def is_sorted(lst):
    if all(lst[i] < lst[i + 1] for i in range(len(lst) - 1)):
        return "Ascending"
    elif all(lst[i] > lst[i + 1] for i in range(len(lst) - 1)):
        return "Descending"
    else:
        return "Unsorted"


# Initialize a list to store rows
reports = []

# Open the CSV file and read its contents
with open("Data/02_input.csv", mode="r") as file:
    reader = csv.reader(file)
    for row in reader:
        reports.append([int(value) for value in row])

total_safe = 0

for report in reports:
    is_safe = True
    sort_type = is_sorted(report)
    if sort_type == "Unsorted":
        is_safe = False
    else:
        level_index = 0
        while is_safe and level_index < len(report):
            level = report[level_index]
            if level_index != 0:
                previous_level = report[level_index - 1]
                if not (1 <= abs(level - previous_level) <= 3):
                    is_safe = False

            level_index += 1

    if is_safe:
        total_safe += 1


print(total_safe)
# Print the resulting list of lists
# print(list_of_lists)


def is_safe_report(report):
    def is_valid(lst):
        """Check if a list is fully valid."""
        return all(1 <= abs(lst[i] - lst[i + 1]) <= 3 for i in range(len(lst) - 1)) and (
            all(lst[i] < lst[i + 1] for i in range(len(lst) - 1))
            or all(lst[i] > lst[i + 1] for i in range(len(lst) - 1))
        )

    if is_valid(report):  # If the report is already valid
        return True

    # Try removing each level and check if the rest is valid
    for i in range(len(report)):
        modified_report = report[:i] + report[i + 1 :]  # Remove the i-th level
        if is_valid(modified_report):
            return True

    return False  # If no single removal makes it valid


# Process the reports
total_safe = 0
for report in reports:
    if is_safe_report(report):
        total_safe += 1

print(total_safe)
