import pytest


@pytest.mark.utils
@pytest.mark.io
def test_reading_robots_positions(robots_positions1):
    """
    Test if ``utils.read_robots_positions`` works properly.
    """
    robots = [
        (4, 4),
        (4, 4),
        (4, 4),
    ]
    assert len(robots) == len(robots_positions1)
    assert robots == robots_positions1
