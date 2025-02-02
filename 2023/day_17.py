from aocd import get_puzzle
import heapq

DAY = 17
YEAR = 2023

puzzle = get_puzzle(day=DAY, year=YEAR)
puzzle_data = puzzle.input_data
examples = puzzle.examples
example_input = examples[0].input_data
part_a_example_solution = examples[0].answer_a
part_b_example_solution = examples[0].answer_b

def parse_input(input_data):
    return input_data.splitlines()

def part_a(input_data, min_con = 1, max_con = 3):
    grid = parse_input(input_data)
    height = len(grid)
    width = len(grid[0])
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    start = (0,0,0)
    end = (width - 1, height - 1)
    pq = []
    heapq.heappush(pq, (0, start[0], start[1], start[2], 0))
    visited = set()


    while pq:
        score, x, y, direction, con = heapq.heappop(pq)
        if (x, y) == end:
            return score

        if (x, y, direction, con) in visited:
            continue
        visited.add((x, y, direction, con))

        # Move forward
        if con < max_con:
            dx, dy = directions[direction]
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                heapq.heappush(pq, (score + int(grid[ny][nx]), nx, ny, direction, con + 1))

        if con >= min_con:
            # Rotate clockwise
            new_direction = (direction + 1) % 4
            if (x, y, new_direction, 0) not in visited:
                heapq.heappush(pq, (score, x, y, new_direction, 0))

            # Rotate counter-clockwise
            new_direction = (direction - 1) % 4
            if (x, y, new_direction, 0) not in visited:
                heapq.heappush(pq, (score, x, y, new_direction, 0))

    return -1  # If no solution exists (shouldn't happen with a valid grid)


def part_b(input_data):
    return part_a(input_data, 4, 10)


# print(example_input)
# print(parse_input(example_input))
print("Example Output A: ", part_a(example_input), " Solution: ", part_a_example_solution)
print("Example Output B: ", part_b(example_input), " Solution: ", part_b_example_solution)
print("Part A: ", part_a(puzzle_data))
print("Part B: ", part_b(puzzle_data))
