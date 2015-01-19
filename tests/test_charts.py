# coding: utf-8
import pytest
from mmvdApp.charts import gantt_values, gantt_chart


@pytest.mark.utils
@pytest.mark.charts
def test_gantt_values(states1, drop_zone1):
    data = {
        0: [[1, 16, 'a'], ],
        1: [[2, 11, 'b'], ],
        2: [[3, 6, 'f'], ]
    }
    assert gantt_values(states1, drop_zone1) == data


@pytest.mark.utils
@pytest.mark.charts
@pytest.mark.slow
def test_gantt_chart(states1, drop_zone1):
    data = gantt_values(states1, drop_zone1)
    assert gantt_chart(data)
