import pytest


@pytest.mark.utils
def test_reading_warehouse_map(warehouse_map1):
    """
    Test if ``utils.read_warehouse_map`` works properly.
    """
    map_ = [
        [2,  2,  2,  2,  3],
        [1, "a", 1, "b", 3],
        [1, "c", 1, "d", 3],
        [1, "e", 1, "f", 3],
        [1,  4,  4,  4,  9],
    ]
    assert map_ == warehouse_map1
