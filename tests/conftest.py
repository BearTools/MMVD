import pytest
from mmvdApp.utils import read_warehouse_map, read_robots_positions


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
def robots_positions1(tmpdir):
    content = """4,4
4,4
4,4
4,4
4,4
"""
    file_ = tmpdir.join("robots1.map")
    file_.write(content)
    return read_robots_positions(str(file_))
