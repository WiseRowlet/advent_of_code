import heapq
from collections import defaultdict, deque


def get_bytes(file_path):
    bytes = []
    with open(file_path, "r") as file:
        for line in file:
            byte = [int(num) for num in line.strip().split(sep=",")]
            bytes.append(tuple((byte[0], byte[1])))
    return bytes


def find_min_distance_2(start, end, size, corrupted, num_bytes):
    # Directions: 0 = East, 1 = North, 2 = West, 3 = South
    directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    corrupted = corrupted[:num_bytes]
    # Priority queue for A*
    pq = []
    heapq.heappush(pq, (0, start[0], start[1]))  # (score, x, y)

    # Visited states: (x, y)
    visited = set()

    while pq:
        # print(pq)
        score, x, y = heapq.heappop(pq)

        # Goal reached
        if (x, y) == end:
            return score

        # Avoid revisiting states
        if (x, y) in visited:
            continue
        visited.add((x, y))

        # Move forward
        movements = {(x + direction[0], y + direction[1]) for direction in directions}
        for movement in movements:
            nx, ny = movement
            if (nx, ny) not in corrupted and 0 <= nx <= size and 0 <= ny <= size:
                heapq.heappush(pq, (score + 1, nx, ny))


def find_min_distance(start, end, size, corrupted, num_bytes):
    # Directions: 0 = East, 1 = North, 2 = West, 3 = South
    directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    corrupted = corrupted[:num_bytes]
    # Priority queue for A*
    pq = []
    heapq.heappush(pq, (0, start[0], start[1], 0))  # (score, x, y, direction)

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
        if (nx, ny) not in corrupted and 0 <= nx <= size and 0 <= ny <= size:
            heapq.heappush(pq, (score + 1, nx, ny, direction))

        # Rotate clockwise
        new_direction = (direction + 1) % 4
        if (x, y, new_direction) not in visited:
            heapq.heappush(pq, (score, x, y, new_direction))


def find_last_bit(start, end, max, corrupted, start_byte=1):
    i = start_byte
    max_bytes = len(corrupted)
    while True:
        min_distance = find_min_distance(start, end, max, corrupted, i)
        print(f"Adding byte {i} - {corrupted[i - 1]}, distance: {min_distance}")
        if min_distance is None:
            return corrupted[i - 1]
        if i >= max_bytes:
            return None
        i += 1


def find_blockade(corrupted, size, start_byte=1):
    i = start_byte
    max_bytes = len(corrupted)
    while True:
        print(f"Adding byte {i} - {corrupted[i - 1]}")
        is_blockade = check_blockade(corrupted[:i], size, size)
        if is_blockade:
            return corrupted[i - 1]
        if i >= max_bytes:
            return None
        i += 1


def get_neighbors(x, y, coordinate_set):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    neighbors = [(x + dx, y + dy) for dx, dy in directions]

    return [n for n in neighbors if n in coordinate_set]


def check_blockade(corrupted, width, height):
    # Convert coordinates to a set for fast lookup
    corrupted_set = set(corrupted)
    width = width + 1
    height = height + 1
    # Define edges
    top_edge = {(x, 0) for x in range(width)}
    bottom_edge = {(x, height - 1) for x in range(width)}
    left_edge = {(0, y) for y in range(height)}
    right_edge = {(width - 1, y) for y in range(height)}
    edge_pairs = [(top_edge, bottom_edge), (left_edge, right_edge), (top_edge, left_edge), (right_edge, bottom_edge)]

    graph = defaultdict(list)
    for x, y in corrupted_set:
        graph[(x, y)] = get_neighbors(x, y, corrupted_set)

    # Check connectivity between edges
    for edge1, edge2 in edge_pairs:
        # Find all coordinates on the current edges
        start_nodes = edge1 & corrupted_set
        end_nodes = edge2 & corrupted_set
        # BFS to find a path
        visited = set()
        queue = deque(start_nodes)
        while queue:
            node = queue.popleft()
            if node in visited:
                continue
            visited.add(node)

            # If we reach a node on the second edge, a line exists
            if node in end_nodes:
                return True

            # Add neighbors to the queue
            for neighbor in graph[node]:
                if neighbor not in visited:
                    queue.append(neighbor)
    return False


corrupted = get_bytes("2024/Data/18_input.txt")
corrupted_test = get_bytes("2024/Data/18_input_test.txt")

# print(find_min_distance((0, 0), (6, 6), 6, corrupted_test, 12))
# print(find_min_distance((0, 0), (70, 70), 70, corrupted, 1024))
print(find_min_distance_2((0, 0), (6, 6), 6, corrupted_test, 12))
print(find_min_distance_2((0, 0), (70, 70), 70, corrupted, 1024))
# # print(find_last_bit((0, 0), (6, 6), 6, corrupted_test))
# print(find_last_bit((0, 0), (70, 70), 70, corrupted, 1024))
# print(find_blockade(corrupted_test, 6, 12))
# print(find_blockade(corrupted, 70, 1024))
