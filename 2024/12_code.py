from collections import defaultdict


def get_input(file_path):
    with open(file_path, "r") as file:
        garden_map = [line.strip() for line in file]
    return garden_map


garden_map_test_A = [
    "AAAA",
    "BBCD",
    "BBCC",
    "EEEC",
]

garden_map_test_B = [
    "OOOOO",
    "OXOXO",
    "OOOOO",
    "OXOXO",
    "OOOOO",
]

garden_map_test_C = [
    "RRRRIICCFF",
    "RRRRIICCCF",
    "VVRRRCCFFF",
    "VVRCCCJFFF",
    "VVVVCJJCFE",
    "VVIVCCJJEE",
    "VVIIICJJEE",
    "MIIIIIJJEE",
    "MIIISIJEEE",
    "MMMISSJEEE",
]


def get_plot(garden_map):
    plot = {}
    width = len(garden_map[0])
    height = len(garden_map)
    visited = set()

    def add_to_region(x, y):
        region.add((x, y))
        for nx, ny in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            if (
                0 <= nx < width
                and 0 <= ny < height
                and garden_map[ny][nx] == plant
                and (nx, ny) not in region
                and (nx, ny) not in visited
            ):
                add_to_region(nx, ny)
                visited.add((nx, ny))

    for y, row in enumerate(garden_map):
        for x, plant in enumerate(row):
            if (x, y) not in visited:
                visited.add((x, y))

                prefix = plant + "_"
                matching_plants = [region_name for region_name in plot if region_name.startswith(prefix)]
                region = set()
                if not matching_plants:
                    region_name = plant + "_1"
                else:
                    region_name = plant + "_" + str(len(matching_plants) + 1)
                add_to_region(x, y)
                plot[region_name] = region
    return plot


def count_continuous_sides(edges):
    grouped = defaultdict(list)
    for x, y, direction in edges:
        if direction in ("up", "down"):
            grouped[(direction, y)].append(x)
        elif direction in ("left", "right"):
            grouped[(direction, x)].append(y)

    sides = 0

    for (direction, _), coordinates in grouped.items():
        coordinates.sort()

        for i in range(len(coordinates)):
            if i == 0 or coordinates[i] != coordinates[i - 1] + 1:
                sides += 1

    return sides


def get_plot_details(garden_map):
    plot = get_plot(garden_map)
    plot_details = {}
    directions = {
        (-1, 0): "left",
        (1, 0): "right",
        (0, -1): "up",
        (0, 1): "down",
    }

    for plant, coordinates in plot.items():
        area = len(coordinates)
        perimeter = 0
        edges = set()

        for x, y in coordinates:
            for nx, ny in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
                if (nx, ny) not in coordinates:
                    perimeter += 1
                    dx, dy = nx - x, ny - y
                    direction = directions[(dx, dy)]
                    edges.add((x, y, direction))

        num_sides = count_continuous_sides(edges)

        perimeter_price = area * perimeter
        side_price = area * num_sides
        plot_details[plant] = (area, perimeter, num_sides, perimeter_price, side_price)
        print(f"Plant: {plant}, Area: {area}, Perimeter: {perimeter}, Sides: {num_sides}, Side Price: {side_price}")
    return plot_details


def get_garden_cost(garden_map):
    plot_details = get_plot_details(garden_map)
    return (
        sum(perimeter_price for _, (_, _, _, perimeter_price, _) in plot_details.items()),
        sum(side_price for _, (_, _, _, _, side_price) in plot_details.items()),
    )


garden_map = get_input("Data/12_input.txt")

print(get_garden_cost(garden_map))
