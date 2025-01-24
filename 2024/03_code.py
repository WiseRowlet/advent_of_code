import re

with open("2024/Data/03_input.txt", mode="r") as file:
    memory_string = file.read()


def find_memory(input_string: str) -> int:
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    matches = re.findall(pattern, input_string)

    return sum([int(a) * int(b) for a, b in matches])


memory_leak = find_memory(memory_string)
print(memory_leak)


def find_memory_complex(input_string: str) -> int:
    pattern = r"(?:^|do\(\))(.*?)(?=don't\(\)|$)"
    matches = re.findall(pattern, input_string, flags=re.DOTALL)
    return sum([find_memory(match) for match in matches])


memory_leak = find_memory_complex(memory_string)
print(memory_leak)
