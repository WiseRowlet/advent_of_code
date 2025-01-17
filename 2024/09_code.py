def get_input(file_path):
    with open(file_path, "r") as file:
        disk_map = [line.strip() for line in file]
    return disk_map[0]


def unpack_disk_map(disk_map):
    unpacked_disk_map = [
        str(int(i / 2)) if i % 2 == 0 else "." for i in range(len(disk_map)) for _ in range(int(disk_map[i]))
    ]
    return unpacked_disk_map


def compact_disk_map(disk_map):
    unpacked_disk_map = unpack_disk_map(disk_map)
    left = 0
    right = len(unpacked_disk_map) - 1

    while left < right:
        while left < right and unpacked_disk_map[left] != ".":
            left += 1
        while left < right and unpacked_disk_map[right] == ".":
            right -= 1
        if left < right:
            unpacked_disk_map[left] = unpacked_disk_map[right]
            unpacked_disk_map[right] = "."
            left += 1
            right -= 1
    return unpacked_disk_map


def compact_disk_map_whole_file(disk_map):
    unpacked_disk_map = unpack_disk_map(disk_map)
    file_blocks = {}
    for i, block in enumerate(unpacked_disk_map):
        if block != ".":
            file_id = int(block)
            if file_id not in file_blocks:
                file_blocks[file_id] = [i, i]  # Initialize start and end
            else:
                file_blocks[file_id][1] = i  # Update end index

    for file_id in sorted(file_blocks.keys(), reverse=True):
        start, end = file_blocks[file_id]
        file_length = end - start + 1

        left = 0
        while left < len(unpacked_disk_map):
            # Look for a contiguous span of free space
            span_start = left
            while left < len(unpacked_disk_map) and unpacked_disk_map[left] == ".":
                left += 1
            span_end = left - 1

            if span_end - span_start + 1 >= file_length and span_end < start:
                # Found a valid span; move the file
                unpacked_disk_map[span_start : span_start + file_length] = [str(file_id)] * file_length
                unpacked_disk_map[start : end + 1] = ["."] * file_length
                break

            # Move to the next span
            left += 1
    return unpacked_disk_map


def checksum_disk_map(disk_map, whole_file=False):
    if whole_file:
        compacted_disk_map = compact_disk_map_whole_file(disk_map)
    else:
        compacted_disk_map = compact_disk_map(disk_map)

    check_sum = sum(
        i * int(compacted_disk_map[i]) if compacted_disk_map[i] != "." else 0 for i in range(len(compacted_disk_map))
    )

    return check_sum


disk_map = "2333133121414131402"

disk_map = get_input("Data/09_input.txt")

print(checksum_disk_map(disk_map, False))
print(checksum_disk_map(disk_map, True))
