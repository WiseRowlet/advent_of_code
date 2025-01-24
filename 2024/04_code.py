def is_word_in_direction(grid, word, x, y, dx, dy):
    """Check if the word exists starting at (x, y) in direction (dx, dy)."""
    for i in range(len(word)):
        nx, ny = x + i * dx, y + i * dy
        if not (0 <= nx < len(grid) and 0 <= ny < len(grid[0])):
            return False  # Out of bounds
        if grid[nx][ny] != word[i]:
            return False  # Mismatch
    return True


def is_word_in_direction_with_middle(grid, word, x, y, dx, dy):
    """Check if the word exists starting at (x, y) in direction (dx, dy)
    with the middle letter at the starting position (x, y)."""
    middle_index = len(word) // 2  # Calculate the index of the middle letter

    for i in range(len(word)):
        nx, ny = x + (i - middle_index) * dx, y + (i - middle_index) * dy
        if not (0 <= nx < len(grid) and 0 <= ny < len(grid[0])):
            return False  # Out of bounds
        if grid[nx][ny] != word[i]:
            return False  # Mismatch

    return True


def get_middle_letter(word):
    length = len(word)
    if length % 2 == 1:  # Odd length
        return word[length // 2]
    else:  # Even length
        raise "Word must have odd length"


def count_word_in_grid(grid, word):
    directions = [  # All 8 possible directions
        (0, 1),  # Right
        (0, -1),  # Left
        (1, 0),  # Down
        (-1, 0),  # Up
        (1, 1),  # Down-right
        (-1, -1),  # Up-left
        (1, -1),  # Down-left
        (-1, 1),  # Up-right
    ]

    count = 0
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            for dx, dy in directions:
                if is_word_in_direction(grid, word, x, y, dx, dy):
                    count += 1
    return count


def count_x_word_in_grid(grid, xword):
    xdirections_1 = [
        (1, 1),  # Down-right
        (-1, -1),  # Up-left
    ]

    xdirections_2 = [
        (1, -1),  # Down-left
        (-1, 1),  # Up-right
    ]
    count = 0
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == get_middle_letter(xword):
                for dx, dy in xdirections_1:
                    if is_word_in_direction_with_middle(grid, xword, x, y, dx, dy):
                        print("Found")
                        for dx, dy in xdirections_2:
                            if is_word_in_direction_with_middle(grid, xword, x, y, dx, dy):
                                count += 1
    return count


# Read the grid from the text file
with open("2024/Data/04_input.txt", "r") as file:
    grid = [list(line.strip()) for line in file]

# Define the word to search for
word = "XMAS"
xword = "MAS"

# Count instances of the word
result = count_word_in_grid(grid, word)
xresult = count_x_word_in_grid(grid, xword)

print(f"The word '{word}' appears {result} times in the grid.")
print(f"The x-word '{xword}' appears {xresult} times in the grid.")
