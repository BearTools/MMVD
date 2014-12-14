from .utils import read_warehouse_map, read_robots_positions
from .logic import Magazine


def run_application(warehouse_filename, robots_filename, order_filename):
    """
    Start application and:
    - load specified warehouse map
    - load initial robots positions
    - load specific order
    """
    map = read_warehouse_map(warehouse_filename)
    robots = read_robots_positions(robots_filename)
    # robots = read_robots_positions(robots_filename)
    # order = read_order(order_filename)

    width = len(map[0])
    height = len(map)
    warehouse = Magazine(width, height)

    warehouse.show()
    warehouse.update(map, [[3, 1, 2, None]])
    warehouse.end()  # TODO: what an unfortunate name
