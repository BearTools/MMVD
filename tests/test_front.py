# coding: utf-8
import pytest

from mmvdApp.visualization import Visualization


@pytest.mark.frontend
@pytest.mark.slow
def test_magazine_class(warehouse_map1):
    app = Visualization(warehouse_map1)
    robots = ((0, 0), (1, 1), (2, 3), (4, 2))
    app.draw_robots(robots)
    app.animate([[0, 2], [1, 2], [2, 3], [3, 3]], [["a", 3]])
    app.animate([[0, 2], [1, 3], [2, 4], [3, 3]], [["b", 0]])
    app.animate([[0, 2], [1, 3], [2, 4], [3, 4]], [["c", 0]])
    app.animate([[0, 2], [1, 3], [2, 1]], [["d", 2]])
    # new robots are given new id numbers
    app.draw_robots(robots)
    # in order to move new robots one has to use proper id
    app.animate([[4, 2], [5, 3], [6, 1]], [["d", 2]])
    app.animate([[0, 3]], [])
    app.animate([[0, 3]], [])
    app.animate([[0, 3]], [])
    app.animate([[0, 3]], [])
    app.animate([[0, 4]], [])
    app.animate([[0, 4]], [])
    app.animate([[0, 4]], [])
    app.animate([[0, 4]], [])
    app.animate([[0, 1]], [])
    app.animate([[0, 1]], [])
    app.animate([[0, 1]], [])
    app.animate([[0, 1]], [])
    app.animate([[0, 2]], [])
    app.animate([[0, 2]], [])
    app.animate([[0, 2]], [])
    app.animate([[0, 2]], [])
