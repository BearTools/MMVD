import pytest
from mmvdApp.utils import read_warehouse_map


@pytest.fixture
def warehouse_map1(tmpdir):
    content = """22223
1a1b3
1c1d3
1e1f3
14449
"""
    file_ = tmpdir.join("warehouse.map")
    file_.write(content)
    return read_warehouse_map(str(file_), use_numpy=False)
