# coding: utf-8
import numpy as np


def read_warehouse_map(name, use_numpy=False):
    """
    Read the file line by line and represent it as an array or list of lists.
    """
    with open(name, 'r') as f:
        lines = f.readlines()
    lines = map(lambda x: x.rstrip(), lines)  # get rid of line endings
    lines = filter(len, lines)  # get rid of empty lines
    lines = map(list, lines)  # split each line into list (ie. mutable string)

    # change '0' to '9' into integers 0-9
    for k1, v1 in enumerate(lines):
        for k2, v2 in enumerate(v1):
            try:
                v2_ = int(v2)
            except ValueError:
                v2_ = v2
            lines[k1][k2] = v2_

    if use_numpy:
        # CAUTION: Numpy arrays don't support mixed ints and chars, there's
        #          gonna be all characters.
        lines = np.array(lines)

    return lines
