import pytest

from mmvdApp.utils import products, distances
from mmvdApp.shortest_path import a_star, neighbors


@pytest.mark.utils
@pytest.mark.map
def test_drop_zone(drop_zone1):
    """
    Test if correct coordinates are returned for the drop zone in
    warehouse_map1.

    :param fixture drop_zone1: provided by `conftest.py`
    """
    assert drop_zone1 == (4, 4)


@pytest.mark.utils
@pytest.mark.map
def test_products_coords(warehouse_map1, order1):
    """
    Test:
    * if correct coordinates are being returned
    * if coordinates are returned in the same order as products are in `order1`
    """
    coords = products(warehouse_map1, order1)

    # order1 == ['f', 'b', 'a']
    assert coords == [(3, 3), (1, 3), (1, 1)]


@pytest.mark.utils
@pytest.mark.map
def test_products_distances(warehouse_map1, order1, drop_zone1):
    """
    Test if distances between various points are calculated correctly.
    Test not only products, but also some points that aren't reachable.
    """
    # test distances from drop zone to products and back
    D = distances(warehouse_map1, products(warehouse_map1, order1),
                  start_pos=drop_zone1, end_pos=drop_zone1)
    assert D == [(2, 2), (6, 4), (6, 8)]
