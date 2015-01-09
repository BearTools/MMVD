# coding: utf-8
import pytest
from mmvdApp.utils import (read_warehouse_map, read_robots_positions,
                           read_order, drop_zone)


@pytest.fixture
def warehouse_map1(tmpdir):
    content = """22223
1a1b3
1c1d3
1e1f3
14449
"""
    file_ = tmpdir.join("warehouse1.map")
    file_.write(content)
    return read_warehouse_map(str(file_), use_numpy=False)


@pytest.fixture
def drop_zone1(warehouse_map1):
    """
    Find the drop zone coordinates.
    """
    return drop_zone(warehouse_map1)


@pytest.fixture
def robots_positions1(tmpdir):
    content = """4,4
4,4
4,4
"""
    file_ = tmpdir.join("robots1.map")
    file_.write(content)
    return read_robots_positions(str(file_))


@pytest.fixture
def order1(tmpdir):
    """
    Specify requested order of products.
    """
    content = """f
b
a
"""
    file_ = tmpdir.join("warehouse1.map")
    file_.write(content)
    return read_order(str(file_))


@pytest.fixture
def states1():
    """
    Return states that provide a complete solution for the warehouse1,
    robots_positions1 and order1.

    In this solution, robot R3 goes for product "f", robot R2 goes for product
    "b", and robot R1 goes for product "a".
    """
    # one tuple, e.g. (0, 4, 4, None), means:
    # - robot 0
    # - on position (4, 4)
    # - carries None (nothing)
    return [
        [(0, 4, 4, None), (1, 4, 4, None), (2, 4, 4, None)],
        [(0, 4, 3, None), (1, 4, 4, None), (2, 4, 4, None)],
        [(0, 4, 2, None), (1, 4, 3, None), (2, 4, 4, None)],
        [(0, 4, 1, None), (1, 4, 2, None), (2, 4, 3, None)],
        [(0, 4, 0, None), (1, 3, 2, None), (2, 3, 3, "f")],
        [(0, 3, 0, None), (1, 2, 2, None), (2, 3, 4, "f")],
        [(0, 2, 0, None), (1, 1, 2, None), (2, 4, 4, "f")],
        [(0, 1, 0, None), (1, 1, 3, "b"), (2, 4, 4, None)],
        [(0, 1, 1, "a"), (1, 1, 4, "b"), (2, 4, 4, None)],
        [(0, 0, 1, "a"), (1, 2, 4, "b"), (2, 4, 4, None)],
        [(0, 0, 2, "a"), (1, 3, 4, "b"), (2, 4, 4, None)],
        [(0, 0, 3, "a"), (1, 4, 4, "b"), (2, 4, 4, None)],
        [(0, 0, 4, "a"), (1, 4, 4, None), (2, 4, 4, None)],
        [(0, 1, 4, "a"), (1, 4, 4, None), (2, 4, 4, None)],
        [(0, 2, 4, "a"), (1, 4, 4, None), (2, 4, 4, None)],
        [(0, 3, 4, "a"), (1, 4, 4, None), (2, 4, 4, None)],
        [(0, 4, 4, "a"), (1, 4, 4, None), (2, 4, 4, None)],
    ]
