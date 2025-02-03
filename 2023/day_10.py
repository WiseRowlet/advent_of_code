from collections import deque

from aocd import get_puzzle

DAY = 10
YEAR = 2023

puzzle = get_puzzle(day=DAY, year=YEAR)
puzzle_data = puzzle.input_data
examples = puzzle.examples
example_input = examples[0].input_data
example_input_2 = examples[1].input_data
example_input_3 = examples[2].input_data
example_input_4 = examples[3].input_data
example_input_5 = examples[4].input_data
example_input_6 = examples[5].input_data
part_a_example_solution = examples[1].answer_a
part_b_example_solution = examples[4].answer_b


def parse_input(input_data):
    pipes = set()
    pipe_map = []
    for i, line in enumerate(input_data.splitlines()):
        pipe_map.append(line)
        for j, char in enumerate(line):
            if char != ".":
                if char == "S":
                    start = (j, i)
                else:
                    pipes.add((j, i))
    return start, pipe_map


def get_neighbors(x, y, pipe_map, visited):
    char = pipe_map[y][x]
    if char == "S":
        directions = {"up": (x, y - 1), "down": (x, y + 1), "left": (x - 1, y), "right": (x + 1, y)}
    elif char == "|":
        directions = {
            "up": (x, y - 1),
            "down": (x, y + 1),
        }
    elif char == "-":
        directions = {"left": (x - 1, y), "right": (x + 1, y)}
    elif char == "L":
        directions = {"up": (x, y - 1), "right": (x + 1, y)}
    elif char == "J":
        directions = {"up": (x, y - 1), "left": (x - 1, y)}
    elif char == "7":
        directions = {"down": (x, y + 1), "left": (x - 1, y)}
    elif char == "F":
        directions = {"down": (x, y + 1), "right": (x + 1, y)}

    neighbors = []
    for direction, coord in directions.items():
        if coord not in visited:
            if direction == "up" and pipe_map[coord[1]][coord[0]] in "|7F":
                neighbors.append(coord)
            elif direction == "down" and pipe_map[coord[1]][coord[0]] in "|LJ":
                neighbors.append(coord)
            elif direction == "left" and pipe_map[coord[1]][coord[0]] in "-FL":
                neighbors.append(coord)
            elif direction == "right" and pipe_map[coord[1]][coord[0]] in "-7J":
                neighbors.append(coord)

    return neighbors


def part_a(input_data):
    start, pipe_map = parse_input(input_data)
    x, y = start
    visited = set()
    visited.add((x, y))
    queue = deque([(x, y, 0)])
    while queue:
        x, y, steps = queue.popleft()
        neighbors = get_neighbors(x, y, pipe_map, visited)
        for neighbor in neighbors:
            queue.append((*neighbor, steps + 1))
            visited.add(neighbor)
    return steps


def part_b(input_data):
    grid = input_data.split()
    graph = {}
    for x, line in enumerate(grid):
        for y, tile in enumerate(line):
            adjacent = []
            if tile in "-J7S":
                adjacent.append((x, y - 1))
            if tile in "-FLS":
                adjacent.append((x, y + 1))
            if tile in "|F7S":
                adjacent.append((x + 1, y))
            if tile in "|LJS":
                adjacent.append((x - 1, y))
            if tile == "S":
                tile_q = set([(x, y)])
            graph[(x, y)] = adjacent
    pipes = set()
    while tile_q:
        nxt = set()
        for x1, y1 in tile_q:
            for x2, y2 in graph[(x1, y1)]:
                if (x1, y1) not in graph.get((x2, y2), []):
                    continue
                pipe = (*sorted((x1, x2)), *sorted((y1, y2)))
                if pipe not in pipes:
                    pipes.add(pipe)
                    nxt.add((x2, y2))
        tile_q = nxt
    m, n = len(grid), len(grid[0])
    visited = set()
    corner_q = [(0, 0)]

    while corner_q:
        x, y = corner_q.pop()
        requirements = (x > 0, y < n, x < m, y > 0)
        adjacent = ((x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1))
        tile_pairs = (
            (x - 1, x - 1, y - 1, y),  # up
            (x - 1, x, y, y),  # right
            (x, x, y - 1, y),  # down
            (x - 1, x, y - 1, y - 1),
        )  # left
        for req, corner, tile_pair in zip(requirements, adjacent, tile_pairs):
            if req and corner not in visited and tile_pair not in pipes:
                visited.add(corner)
                corner_q.append(corner)

    total = m * n - len(pipes)
    for i in range(m):
        for j in range(n):
            corners = ((i, j), (i + 1, j), (i, j + 1), (i + 1, j + 1))
            if all(c in visited for c in corners):
                total -= 1

    return total


# print(example_input_5)
# print(parse_input(example_input))
print("Example Output A: ", part_a(example_input_2), " Solution: ", part_a_example_solution)
print("Example Output B: ", part_b(example_input_5), " Solution: ", part_b_example_solution)
print("Part A: ", part_a(puzzle_data))
print("Part B: ", part_b(puzzle_data))
