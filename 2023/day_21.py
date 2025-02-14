from aocd import get_puzzle
from collections import deque
import numpy as np

DAY = 21
YEAR = 2023

puzzle = get_puzzle(day=DAY, year=YEAR)
puzzle_data = puzzle.input_data
examples = puzzle.examples
example_input = examples[0].input_data
part_a_example_solution = examples[0].answer_a
part_b_example_solution = examples[0].answer_b


def parse_input(input_data):
    grid = input_data.splitlines()
    start = None
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c == "S":
                start = (x,y)
    return grid, start

def get_neighbors(x, y, grid):
    directions = [(1,0),(-1,0),(0,1),(0,-1)]
    height = len(grid)
    width = len(grid[0])
    neighbors = []
    for direction in directions:
        dx, dy = direction
        nx, ny = x + dx, y + dy
        if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] != "#":
            neighbors.append((nx, ny))
    return neighbors
        
def part_a(input_data, steps=6):
    grid, start = parse_input(input_data)
    places = set()
    places.add(start)
    steps_taken = 0
    while steps_taken < steps:
        next_places = set()
        for place in places:
            x,y = place
            neighbors = get_neighbors(x,y,grid)
            for n in neighbors:
                next_places.add(n)
        places = next_places
        steps_taken += 1
    
    return len(places)


def part_b(input_data):
    grid = [list(row) for row in input_data.split('\n')]
    m, n = len(grid), len(grid[0])
    assert m == n and grid[n//2][n//2] == 'S', "The grid needs to be square with S exactly in the middle"

    # After having crossed the border of the first grid, every further border crossing is seperated by n steps (length/width of grid)
    # Therefore, the total number of grids to traverse in any direction is 26_501_365 // n = x_final
    # Assumption: at step 26_501_365 another border crossing is taking place
    # If so, then it follows that the first crossing takes place at 26_501_365 % n = remainder
    x_final, remainder = divmod(26_501_365, n)
    border_crossings = [remainder, remainder + n, remainder + 2*n]

    visited = set()
    queue = deque([(n//2, n//2)])
    total = [0, 0]  # [even, odd]
    Y = []
    for step in range(1, border_crossings[-1]+1):
        for _ in range(len(queue)):
            x, y = queue.popleft()
            for i, j in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                if (i, j) in visited or grid[i%m][j%n] == '#':
                    continue

                visited.add((i, j))
                queue.append((i, j))
                total[step % 2] += 1

        if step in border_crossings:
            Y.append(total[step % 2])

    X = [0, 1, 2]
    coefficients = np.polyfit(X, Y, deg=2)      # get coefficients for quadratic equation y = a*x^2 + bx + c
    y_final = np.polyval(coefficients, x_final) # using coefficients, get y value at x_final
    return y_final.round().astype(int)


print(example_input)
print(parse_input(example_input))
print("Example Output A: ", part_a(example_input), " Solution: ", part_a_example_solution)
print("Example Output B: ", part_b(example_input), " Solution: ", part_b_example_solution)
print("Part A: ", part_a(puzzle_data, 64))
print("Part B: ", part_b(puzzle_data))

