from collections import defaultdict


def get_input(file_path):
    with open(file_path, "r") as file:
        antenna_map = [line.strip() for line in file]
    return antenna_map


def find_character_coordinates(strings):
    char_coordinates = defaultdict(list)

    for y, string in enumerate(strings):
        for x, char in enumerate(string):
            if char != ".":
                char_coordinates[char].append((x, y))
    return char_coordinates


def get_antinodes(antenna, char_coordinates, map_width, map_height):
    antinodes = set()  # Use a set to collect antinodes
    antenna_coordinates = char_coordinates[antenna]
    for i in range(len(antenna_coordinates)):
        for j in range(i + 1, len(antenna_coordinates)):
            node_i = antenna_coordinates[i]
            node_j = antenna_coordinates[j]
            diff_x = abs(node_i[0] - node_j[0])
            diff_y = abs(node_i[1] - node_j[1])
            k = 1
            antinodes.add(node_i)
            antinodes.add(node_j)
            while True:
                break_counter = 0
                if node_i[0] <= node_j[0]:
                    antinode_i_x = node_i[0] - (diff_x * k)
                    antinode_j_x = node_j[0] + (diff_x * k)
                else:
                    antinode_i_x = node_i[0] + (diff_x * k)
                    antinode_j_x = node_j[0] - (diff_x * k)
                if node_i[1] <= node_j[1]:
                    antinode_i_y = node_i[1] - (diff_y * k)
                    antinode_j_y = node_j[1] + (diff_y * k)
                else:
                    antinode_i_y = node_i[1] + (diff_y * k)
                    antinode_j_y = node_j[1] - (diff_y * k)
                if 0 <= antinode_i_x < map_width and 0 <= antinode_i_y < map_height:
                    antinodes.add((antinode_i_x, antinode_i_y))  # Add to set
                else:
                    break_counter += 1
                if 0 <= antinode_j_x < map_width and 0 <= antinode_j_y < map_height:
                    antinodes.add((antinode_j_x, antinode_j_y))  # Add to set
                else:
                    break_counter += 1
                if break_counter == 2:
                    break

                k += 1
    return antinodes


def count_unique_antinodes(antenna_map):
    char_coordinates = find_character_coordinates(antenna_map)
    map_width = len(antenna_map[0])
    map_height = len(antenna_map)
    antinodes = set()
    for antenna in char_coordinates:
        antinodes.update(get_antinodes(antenna, char_coordinates, map_width, map_height))
    # print(sorted(antinodes))
    return len(antinodes)


antenna_map = [
    "............",
    "........0...",
    ".....0......",
    ".......0....",
    "....0.......",
    "......A.....",
    "............",
    "............",
    "........A...",
    ".........A..",
    "............",
    "............",
]

antenna_map = get_input("Data/08_input.txt")
print(count_unique_antinodes(antenna_map))
