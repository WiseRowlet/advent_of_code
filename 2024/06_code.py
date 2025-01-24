def get_original_map():
    with open("2024/Data/06_input.txt", "r") as file:
        lab_map = [list(line.strip()) for line in file]
    return lab_map


def find_guard(find_map):
    for y in range(len(find_map)):
        for x in range(len(find_map[y])):
            if find_map[y][x] == "^":
                direction = (0, -1)
                guard = (x, y)
                break
    return guard, direction


def rotate_guard_90_clockwise(direction):
    dx, dy = direction
    return (-dy, dx)


def move_guard(guard_map, guard, direction, lab_height, lab_width, obstacle=None):
    x, y = guard
    dx, dy = direction
    move_x = x + dx
    move_y = y + dy
    guard_finished = False
    if move_x < 0 or move_x >= lab_width or move_y < 0 or move_y >= lab_height:
        guard_finished = True
        direction = (0, 0)
    else:
        if guard_map[move_y][move_x] == "#" or (obstacle and (move_x, move_y) == obstacle):
            direction = rotate_guard_90_clockwise(direction)
            guard = (x, y)
        else:
            guard = (move_x, move_y)

    return guard, direction, guard_finished


def patrol(lab_map, obstacle=None):
    guard, direction = find_guard(lab_map)
    visited_states = set()
    visited_states.add((guard, direction))
    guard_finished = False
    loop_detected = False
    lab_height = len(lab_map)
    lab_width = len(lab_map[0])
    while not guard_finished:
        guard, direction, guard_finished = move_guard(lab_map, guard, direction, lab_height, lab_width, obstacle)
        state = (guard, direction)
        if state in visited_states:
            loop_detected = True
            guard_finished = True
        else:
            visited_states.add(state)

    return visited_states, loop_detected


def unique_positions(lab_map):
    visited_states = patrol(lab_map)[0]
    return {state[0] for state in visited_states}


def count_unique_positions():
    lab_map = get_original_map()

    return len(unique_positions(lab_map))


def obstacle_loop_count():
    loop_map = get_original_map()
    loop_count = 0
    original_visited_points = unique_positions(loop_map)

    for x, y in original_visited_points:
        if loop_map[y][x] != "^":
            obstacle = (x, y)
            loop_detected = patrol(loop_map, obstacle)[1]
            if loop_detected:
                loop_count += 1

    return loop_count


print(count_unique_positions())
print(obstacle_loop_count())
