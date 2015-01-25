# coding: utf-8


def remove_line_ending(line):
    """
    Strip line from the RHS end.

    :param str line: line to be stripped
    :return: stripped line
    :rtype: str
    """
    return line.rstrip()


def filter_out_empty(line):
    """
    Filter used to determinate if line is not empty.

    :param str line: line to be tested
    :return: length of the line; for non-empty lines this returns value greater
             than zero, which evaluates to boolean ``True``
    :rtype: int
    """
    return len(line)


def process_lines(lines):
    """
    Filter and alter a list of lines (for example from a file).  This function
    is used for initial processing of input files.

    :param list lines: lines to be stripped and filtered out
    :return: the same line without line-ending white characters. Additionally
             empty lines get dropped.
    :rtype: list
    """
    lines = map(remove_line_ending, lines)  # get rid of line endings
    lines = filter(filter_out_empty, lines)  # get rid of empty lines
    return lines


def read_warehouse_map(name):
    """
    Read the file line by line and represent it as an array or list of lists.

    :param string name: path to the warehouse map file
    :return: immutable map
    :rtype: tuple
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
        lines[k1] = tuple(lines[k1])

    return tuple(lines)


def read_robots_positions(name):
    """
    Read a file declaring number of robots and their starting positions.  All
    robots can start from the same position.

    :param string name: path to the file with robot initial positions
    :return: list of pairs (y, x)
    :rtype: list
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

    :param string name: path to the file requested order
    :return: requested order sequence
    :rtype: tuple
    """
    with open(name, 'r') as f:
        lines = process_lines(f.readlines())
    return tuple(lines)
