import heapq
from collections import defaultdict


def get_input(file_path):
    with open(file_path, "r") as file:
        maze_map = [line.strip() for line in file]
    return maze_map


def get_maze_elements(maze_map):
    walls = set()

    for y, row in enumerate(maze_map):
        for x, cell in enumerate(row):
            if cell == "#":
                walls.add((x, y))
            if cell == "S":
                start = (x, y)
                direction = 0
            if cell == "E":
                end = (x, y)
    return walls, end, start, direction


def a_star(maze_map):
    # Parse the map
    walls, end, start, direction = get_maze_elements(maze_map)

    # Directions: 0 = East, 1 = North, 2 = West, 3 = South
    directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]

    # Priority queue for A*
    pq = []
    heapq.heappush(pq, (0, start[0], start[1], direction))  # (score, x, y, direction)

    # Visited states: (x, y, direction)
    visited = set()

    while pq:
        score, x, y, direction = heapq.heappop(pq)

        # Goal reached
        if (x, y) == end:
            return score

        # Avoid revisiting states
        if (x, y, direction) in visited:
            continue
        visited.add((x, y, direction))

        # Move forward
        dx, dy = directions[direction]
        nx, ny = x + dx, y + dy
        if (nx, ny) not in walls and 0 <= nx < len(maze_map[0]) and 0 <= ny < len(maze_map):
            heapq.heappush(pq, (score + 1, nx, ny, direction))

        # Rotate clockwise
        new_direction = (direction + 1) % 4
        if (x, y, new_direction) not in visited:
            heapq.heappush(pq, (score + 1000, x, y, new_direction))

        # Rotate counter-clockwise
        new_direction = (direction - 1) % 4
        if (x, y, new_direction) not in visited:
            heapq.heappush(pq, (score + 1000, x, y, new_direction))

    return -1  # If no solution exists (shouldn't happen with a valid grid)


def a_star_with_predecessors(grid):
    walls, end, start, direction = get_maze_elements(grid)

    # Directions: 0 = East, 1 = North, 2 = West, 3 = South
    directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]

    # Priority queue for A*
    pq = []
    heapq.heappush(pq, (0, start[0], start[1], direction))  # (score, x, y, direction)

    # Store the minimum score and predecessors for each state
    scores = defaultdict(lambda: float("inf"))
    predecessors = defaultdict(list)  # (x, y, direction) -> list of predecessor states

    scores[(start[0], start[1], 0)] = 0

    while pq:
        score, x, y, direction = heapq.heappop(pq)

        # Stop processing once we've explored all paths to the goal
        if (x, y) == end:
            continue

        # Prune worse scores
        if score > scores[(x, y, direction)]:
            continue

        # Move forward
        dx, dy = directions[direction]
        nx, ny = x + dx, y + dy
        if (nx, ny) not in walls and 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
            new_state = (nx, ny, direction)
            new_score = score + 1
            if new_score < scores[new_state]:
                scores[new_state] = new_score
                predecessors[new_state] = [(x, y, direction)]
                heapq.heappush(pq, (new_score, nx, ny, direction))
            elif new_score == scores[new_state]:
                predecessors[new_state].append((x, y, direction))

        # Rotate clockwise
        new_direction = (direction + 1) % 4
        new_state = (x, y, new_direction)
        new_score = score + 1000
        if new_score < scores[new_state]:
            scores[new_state] = new_score
            predecessors[new_state] = [(x, y, direction)]
            heapq.heappush(pq, (new_score, x, y, new_direction))
        elif new_score == scores[new_state]:
            predecessors[new_state].append((x, y, direction))

        # Rotate counter-clockwise
        new_direction = (direction - 1) % 4
        new_state = (x, y, new_direction)
        new_score = score + 1000
        if new_score < scores[new_state]:
            scores[new_state] = new_score
            predecessors[new_state] = [(x, y, direction)]
            heapq.heappush(pq, (new_score, x, y, new_direction))
        elif new_score == scores[new_state]:
            predecessors[new_state].append((x, y, direction))

    return predecessors, end


def reconstruct_all_paths(predecessors, end):
    paths = []

    def backtrack(node, current_path):
        if not predecessors[node]:
            # Reached the start
            paths.append(current_path[::-1])
            return

        for pred in predecessors[node]:
            backtrack(pred, current_path + [pred])

    # Start backtracking from the goal state
    for direction in range(4):  # Check all possible directions at the goal
        goal_state = (end[0], end[1], direction)
        if goal_state in predecessors:
            backtrack(goal_state, [goal_state])

    return paths


def score_path(path):
    last_path = -1
    score = 0
    for i, (x, y, direction) in enumerate(path):
        if last_path == -1:
            last_path = 0
        else:
            last_path = i - 1
        if direction != path[last_path][2]:
            score += 1000
        if x != path[last_path][0] or y != path[last_path][1]:
            score += 1
    return score


test_maze = [
    "###############",
    "#.......#....E#",
    "#.#.###.#.###.#",
    "#.....#.#...#.#",
    "#.###.#####.#.#",
    "#.#.#.......#.#",
    "#.#.#####.###.#",
    "#...........#.#",
    "###.#.#####.#.#",
    "#...#.....#.#.#",
    "#.#.#.###.#.#.#",
    "#.....#...#.#.#",
    "#.###.#.#.#.#.#",
    "#S..#.....#...#",
    "###############",
]
maze = test_maze
maze = get_input("Data/16_input.txt")
predecessors, end = a_star_with_predecessors(maze)
maze_score = a_star(maze)
all_paths = reconstruct_all_paths(predecessors, end)
optimal_paths = [path for path in all_paths if score_path(path) == maze_score]

print(f"Number of Optimal Paths: {len(optimal_paths)}")
all_spots = set()
for i, path in enumerate(optimal_paths, 1):
    # print(f"Path {i}:")
    for spot in path:
        x, y, direction = spot
        all_spots.add((x, y))
print(maze_score)
print(len(all_spots))
