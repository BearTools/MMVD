# coding: utf-8
from .utils.io import read_warehouse_map, read_robots_positions, read_order
from .utils.map import drop_zone, products, distances
from .utils.tabu import tabu_search
from .logic import Magazine


def run_application(warehouse_filename, robots_filename, order_filename):
    """
    Start application and:
    - load specified warehouse map
    - load initial robots positions
    - load specific order

    Then:
    - calculate distances between products on the map and the dropzone
    - start tabu search loop
    - represent results
    """
    map = read_warehouse_map(warehouse_filename)
    robot_positions = read_robots_positions(robots_filename)
    order = read_order(order_filename)

    # calculate distances
    drop_zone_coords = drop_zone(map)
    product_distances = distances(map, products(map, order),
                                  start_pos=drop_zone_coords,
                                  end_pos=drop_zone_coords)

    # start tabu loop

    # if there are 4 robots, create list [0, 1, 2, 3]
    robots = range(len(robot_positions))
    result, steps = tabu_search(map, robots, order, product_distances)

    # representing results
    width = len(map[0])
    height = len(map)
    warehouse = Magazine(width, height)

    # visual
    warehouse.show()
    for step in steps:
        warehouse.update(map, step)
        # TODO: wait for half a second or so?
    warehouse.end()  # TODO: what an unfortunate name
