# coding: utf-8
from .utils.io import read_warehouse_map, read_robots_positions, read_order
from .utils.map import drop_zone, products, distances
from .utils.tabu import tabu_search, initial_solution, generate_solution
from .visualization import Visualization


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
    map_ = read_warehouse_map(warehouse_filename)
    robot_positions = read_robots_positions(robots_filename)
    order = read_order(order_filename)

    product_positions = products(map_, order)

    # calculate distances
    drop_zone_coords = drop_zone(map_)
    product_distances = distances(map_, product_positions,
                                  start_pos=drop_zone_coords,
                                  end_pos=drop_zone_coords)

    # start tabu loop

    # if there are 4 robots, create list [0, 1, 2, 3]

    result, solution, steps = tabu_search(map_, robot_positions,
                                          product_positions, order,
                                          product_distances)
    # just for testing
    # robots = range(len(robot_positions))
    # solution = initial_solution(robots, order)
    # steps = generate_solution(map_, robot_positions, product_positions,order,
    #                           drop_zone_coords, solution)

    # representing results
    gui = Visualization(map_)

    # visual
    # print "Order:", order
    # import pprint
    # pprint.pprint(steps)
    # return

    gui.draw_robots(robot_positions)
    for k, step in enumerate(steps):
        print "Step", k
        robots_update = []
        shelves_update = []
        for robot_id, pos_y, pos_x, product in step:
            if (pos_y, pos_x) != drop_zone_coords:
                robots_update.append((robot_id, (pos_y, pos_x)))
                if product:
                    shelves_update.append((product, (pos_y, pos_x)))
            else:
                pass
                robots_update.append((robot_id, 0))  # hide the robot
                if product:
                    shelves_update.append((product, 0))  # and hide the shelf

        gui.animate(robots_update, shelves_update)

    gui.end()  # TODO: misleading function name, should be "loop" or sth
