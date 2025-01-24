import re


def get_input(file_path):
    with open(file_path, "r") as file:
        robots = parse_input(file.read())
    return robots


def parse_input(robots):
    results = []
    lines = robots.strip().split("\n")

    for line in lines:
        match_pos = re.search(r"p=(-?\d+),(-?\d+)", line)
        match_vel = re.search(r"v=(-?\d+),(-?\d+)", line)
        if match_pos and match_vel:
            position = (int(match_pos.group(1)), int(match_pos.group(2)))
            velocity = (int(match_vel.group(1)), int(match_vel.group(2)))

            results.append({"position": position, "velocity": velocity})
    return results


def move_robot(robot, min_pos, max_pos):
    min_x, min_y = min_pos
    max_x, max_y = max_pos
    position = robot["position"]
    velocity = robot["velocity"]
    new_position = (position[0] + velocity[0], position[1] + velocity[1])
    diff_x, diff_y = 0, 0
    if new_position[0] < min_x:
        diff_x = abs(min_x - new_position[0])
        new_position_x = max_x - diff_x + 1
    elif new_position[0] > max_x:
        diff_x = abs(new_position[0] - max_x)
        new_position_x = min_x + diff_x - 1

    if new_position[1] < min_y:
        diff_y = abs(min_y - new_position[1])
        new_position_y = max_y - diff_y + 1
    elif new_position[1] > max_y:
        diff_y = abs(new_position[1] - max_y)
        new_position_y = min_y + diff_y - 1

    if diff_x > 0:
        new_position = (new_position_x, new_position[1])
    if diff_y > 0:
        new_position = (new_position[0], new_position_y)
    robot["position"] = new_position
    return robot


def elapse_time(robots, time, min_pos, max_pos):
    for _ in range(time):
        for robot in robots:
            move_robot(robot, min_pos, max_pos)
    return robots


def get_robot_quadrants(robots, time, min_pos, max_pos):
    robots = elapse_time(robots, time, min_pos, max_pos)
    mid_x = float(max_pos[0]) / 2
    mid_y = float(max_pos[1]) / 2
    quadrants = {"1": 0, "2": 0, "3": 0, "4": 0}
    for robot in robots:
        if robot["position"][0] < mid_x and robot["position"][1] < mid_y:
            quadrants["1"] += 1
        elif robot["position"][0] > mid_x and robot["position"][1] < mid_y:
            quadrants["2"] += 1
        elif robot["position"][0] < mid_x and robot["position"][1] > mid_y:
            quadrants["3"] += 1
        elif robot["position"][0] > mid_x and robot["position"][1] > mid_y:
            quadrants["4"] += 1
    return quadrants


def get_safety_factor(robots, time, min_pos, max_pos):
    safety_factor = 1
    quadrants = get_robot_quadrants(robots, time, min_pos, max_pos)
    for quadrant in quadrants:
        if quadrants[quadrant] == 0:
            safety_factor = 0
            break
        else:
            safety_factor *= quadrants[quadrant]
    return safety_factor


# def get_robot_regions(robots):
#     visited = set()
#     region_number = 0
#     regions = []
#     for robot in robots:
#         if robot["position"] in visited:
#             continue
#         region = {str(region_number): 0}
#         visited.add(robot["position"])
#         for nx, ny in [
#             (robot["position"][0] - 1, robot["position"][1]),
#             (robot["position"][0] + 1, robot["position"][1]),
#             (robot["position"][0], robot["position"][1] - 1),
#             (robot["position"][0], robot["position"][1] + 1),
#         ]:
#             if (nx, ny) not in visited:
#                 visited.add((nx, ny))
#                 region[str(region_number)] += 1
#         regions.append(region)
#         region_number += 1


#     return regions
def check_robots(robots):
    robot_positions = set(robot["position"] for robot in robots)
    for robot in robot_positions:
        robot_filled = False
        for nx, ny in [
            (robot[0] - 1, robot[1]),
            (robot[0] + 1, robot[1]),
            (robot[0], robot[1] - 1),
            (robot[0], robot[1] + 1),
            (robot[0] - 1, robot[1] - 1),
            (robot[0] + 1, robot[1] + 1),
            (robot[0] - 1, robot[1] + 1),
            (robot[0] + 1, robot[1] - 1),
        ]:
            if (nx, ny) not in robot_positions:
                robot_filled = False
                break
            else:
                robot_filled = True
        if robot_filled:
            return True
    return False


def get_tree(robots, min_pos, max_pos):
    i = 0
    while True:
        is_tree = check_robots(robots)
        if not is_tree:
            elapse_time(robots, 1, min_pos, max_pos)
            if i == 100000:
                i = -1
                break
            i += 1
        else:
            break
    return i


test_input = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""

test_robots = parse_input(test_input)
robots = get_input("2024/Data/14_input.txt")
time = 100
min_pos = (0, 0)
max_pos_test = (10, 6)
max_pos = (100, 102)


# robots = elapse_time(robots, 7051, min_pos, max_pos)
# for x in range(min_pos[1], max_pos[1] + 1):
#     for y in range(min_pos[0], max_pos[0] + 1):
#         if (x, y) in set(robot["position"] for robot in robots):
#             print("#", end="")
#         else:
#             print(".", end="")
#     print()

safety_factor = get_safety_factor(robots, time, min_pos, max_pos)
robots = get_input("2024/Data/14_input.txt")
num_seconds = get_tree(robots, min_pos, max_pos)
print(safety_factor, num_seconds)
