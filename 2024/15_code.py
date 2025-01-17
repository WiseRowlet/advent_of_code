def get_input(file_path):
    with open(file_path, "r") as file:
        warehouse_map = [line.strip() for line in file]
    return warehouse_map


def get_instructions(file_path):
    with open(file_path, "r") as file:
        instructions = file.read().strip()
    return instructions


def get_robot(warehouse_map):
    for y, row in enumerate(warehouse_map):
        for x, cell in enumerate(row):
            if cell == "@":
                return (x, y)


def get_obstacles(warehouse_map, double=False):
    boxes = {}
    b = 0
    walls = {}
    w = 0
    for y, row in enumerate(warehouse_map):
        for x, cell in enumerate(row):
            if not double and cell == "O":
                boxes[b] = (x, y)
                b += 1
            if double and cell == "[":
                boxes[b] = [(x, y), (x + 1, y)]
                b += 1
            if cell == "#":
                walls[w] = (x, y)
                w += 1
    return boxes, walls


def get_objects(warehouse_map, double=False):
    robot = get_robot(warehouse_map)
    boxes, walls = get_obstacles(warehouse_map, double)
    objects = {"robot": robot, "boxes": boxes, "walls": walls}
    return objects


def move_object(objects, direction, double=False):
    """
    Moves the robot or a box based on the given direction while handling obstacles iteratively.
    """

    def trace_push_path(start_box, direction, objects, double):
        """
        Trace the chain of boxes in the push direction.
        Returns the list of all positions in the push chain and whether the push is valid.
        """
        dx, dy = {"<": (-1, 0), ">": (1, 0), "^": (0, -1), "v": (0, 1)}[direction]
        push_chain = []
        current_pos = objects["boxes"][start_box]

        push_chain.append(start_box)
        next_chain = []
        next_chain.append(start_box)

        while True:
            next_chain_temp = []
            for chain_box_id in next_chain:
                current_pos = objects["boxes"][chain_box_id]  # Move to the next box in the chain
                if not double:
                    next_pos = (current_pos[0] + dx, current_pos[1] + dy)
                else:
                    next_pos = (current_pos[0][0] + dx, current_pos[0][1] + dy)
                    next_pos_2 = (current_pos[1][0] + dx, current_pos[1][1] + dy)

                # Check for walls
                if next_pos in objects["walls"].values():
                    return push_chain, False
                if double and next_pos_2 in objects["walls"].values():
                    return push_chain, False

                # Check for other boxes
                for box_id, box_pos in objects["boxes"].items():
                    if box_id not in push_chain:
                        if not double and box_pos == next_pos:
                            next_chain_temp.append(box_id)
                            push_chain.append(box_id)
                            break
                        elif double and (
                            box_pos[0] == next_pos
                            or box_pos[1] == next_pos
                            or box_pos[0] == next_pos_2
                            or box_pos[1] == next_pos_2
                        ):
                            push_chain.append(box_id)
                            next_chain_temp.append(box_id)

            if len(next_chain_temp) == 0:
                # No more boxes in the chain
                break

            next_chain = next_chain_temp
        return push_chain, True

    # Start the movement process
    current_pos = objects["robot"]

    # Compute the next position based on the direction
    dx, dy = {"<": (-1, 0), ">": (1, 0), "^": (0, -1), "v": (0, 1)}[direction]

    next_pos = (current_pos[0] + dx, current_pos[1] + dy)

    # Check for walls
    if next_pos in objects["walls"].values():
        return objects  # No movement

    # Check for boxes
    found_box = None
    for box_id, box_pos in objects["boxes"].items():
        if not double and box_pos == next_pos:
            found_box = box_id
            break
        elif double and (box_pos[0] == next_pos or box_pos[1] == next_pos):
            found_box = box_id
            break

    if found_box is not None:
        # Trace the push path
        push_chain, valid_push = trace_push_path(found_box, direction, objects, double)
        if not valid_push:
            return objects  # Abort movement

        # Move all boxes in the chain
        for box_id in push_chain:
            if not double:
                bx, by = objects["boxes"][box_id]
                objects["boxes"][box_id] = (bx + dx, by + dy)
            else:
                (bx1, by1), (bx2, by2) = objects["boxes"][box_id]
                objects["boxes"][box_id] = [(bx1 + dx, by1 + dy), (bx2 + dx, by2 + dy)]

    # Move the robot
    objects["robot"] = next_pos

    return objects


def direct_robot(warehouse_map, instructions, double=False):
    objects = get_objects(warehouse_map, double)
    for instruction in instructions:
        objects = move_object(objects, instruction, double=True)
    objects.pop("walls")
    return objects


def calculate_gps_sum(warehouse_map, instructions, double=False):
    """
    Calculate the sum of GPS coordinates for all boxes.
    """
    if double:
        warehouse_map = double_warehouse(warehouse_map)
    objects = direct_robot(warehouse_map, instructions, double)
    gps_sum = 0
    for _, positions in objects["boxes"].items():
        if not double:
            x, y = positions
            gps_sum += 100 * y + x
        else:
            x1, y1 = positions[0]
            x2, y2 = positions[1]
            # Use the leftmost and topmost coordinates for GPS
            gps_sum += 100 * min(y1, y2) + min(x1, x2)
    return gps_sum


def double_warehouse(warehouse_map):
    new_warehouse = []
    for row in warehouse_map:
        new_row = ""
        for cell in row:
            if cell == "@":
                new_row += "@."
            if cell == "O":
                new_row += "[]"
            if cell == "#" or cell == ".":
                new_row += cell * 2
        new_warehouse.append(new_row)
    return new_warehouse


test_warehouse_map = [
    "########",
    "#..O.O.#",
    "##@.O..#",
    "#...O..#",
    "#.#.O..#",
    "#...O..#",
    "#......#",
    "########",
]
test_instructions = "<^^>>>vv<v>>v<<"

test_warehouse_map_2 = [
    "##########",
    "#..O..O.O#",
    "#......O.#",
    "#.OO..O.O#",
    "#..O@..O.#",
    "#O#..O...#",
    "#O..O..O.#",
    "#.OO.O.OO#",
    "#....O...#",
    "##########",
]
test_instructions_2 = "<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"

warehouse_map = get_input("Data/15_input.txt")
instructions = get_instructions("Data/15_input_moves.txt")

test_map_2 = double_warehouse(test_warehouse_map_2)

# print(objects)
# Calculate the GPS sum
gps_sum = calculate_gps_sum(warehouse_map, instructions, double=True)
print(f"GPS Sum: {gps_sum}")  # Should output 9021
