# coding: utf-8


def remove_line_ending(line):
    return line.rstrip()


def filter_out_empty(line):
    return len(line)


def process_lines(lines):
    lines = map(remove_line_ending, lines)  # get rid of line endings
    lines = filter(filter_out_empty, lines)  # get rid of empty lines
    return lines


def read_warehouse_map(name):
    """
    Read the file line by line and represent it as an array or list of lists.
    """
    with open(name, 'r') as f:
        lines = process_lines(f.readlines())
    lines = map(list, lines)  # split each line into list (ie. mutable string)

    # change '0' to '9' into integers 0-9
    for k1, v1 in enumerate(lines):
        for k2, v2 in enumerate(v1):
            try:
                v2_ = int(v2)
            except ValueError:
                v2_ = v2
            lines[k1][k2] = v2_

    return lines


def read_robots_positions(name):
    """
    Read a file declaring number of robots and their starting positions.  All
    robots can start from the same position.
    """
    with open(name, 'r') as f:
        lines = process_lines(f.readlines())

    # robots_number = len(lines)
    starting_positions = []
    for line in lines:
        y_pos, x_pos = map(int, line.split(","))
        starting_positions.append((y_pos, x_pos))

    return starting_positions


def read_order(name):
    """
    Read a file with products sequence.  This sequence is important: our robots
    have to bring products to the drop zone in this exact sequence.
    """
    with open(name, 'r') as f:
        lines = process_lines(f.readlines())
    return lines
