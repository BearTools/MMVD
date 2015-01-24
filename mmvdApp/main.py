# coding: utf-8
import logging
import tempfile
from multiprocessing import Process

from .utils.io import read_warehouse_map, read_robots_positions, read_order
from .utils.map import drop_zone, products, distances
from .utils.tabu import tabu_search
from .visualization import Visualization
from .charts import gantt_values, gantt_chart


def run_application(warehouse_filename, robots_filename, order_filename,
                    gantt, gui, summary, tabu_rounds, tabu_memory):
    """
    Start application.

    :param string warehouse_filename: path to the warehouse map
    :param string robots_filename: path to the file containing initial robot
                                   positions
    :param string order_filename: path to the file containing requested order
                                  of products
    :param bool gantt: whether or not to generate Gantt chart at the end
    """
    map_ = read_warehouse_map(warehouse_filename)
    robot_positions = read_robots_positions(robots_filename)
    order = read_order(order_filename)

    product_positions = products(map_, order)

    # calculate distances from dropzone to products and back
    drop_zone_coords = drop_zone(map_)
    product_distances = distances(map_, product_positions,
                                  start_pos=drop_zone_coords,
                                  end_pos=drop_zone_coords)

    # start tabu loop
    logging.info("Starting Tabu Search. This may take a while…")
    result, solution, steps = tabu_search(
        map_, robot_positions, product_positions, order,
        product_distances,
        rounds=tabu_rounds, memsize=tabu_memory
    )

    # show Gantt chart for the best solution
    graph_proc = None
    if gantt:

        file_, fname = tempfile.mkstemp(suffix=".png")
        logging.info("Generating Gantt chart…")
        gantt_data = gantt_values(steps, drop_zone_coords)

        # run this in subprocess to show the chart in a non-blocking way
        # (`plt.show(block=False)` didn't work)
        graph_proc = Process(target=gantt_chart, args=(gantt_data, ),
                             kwargs=dict(savename=fname, show=True))
        graph_proc.start()

    # handle GUI for representing robots animation
    if gui:
        frontend = Visualization(map_)

        frontend.draw_robots(robot_positions)
        for k, step in enumerate(steps):
            # TODO: drop step counter into GUI
            logging.debug("Step %d", k)

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
                        shelves_update.append((product, 0))  # hide the shelf

            frontend.animate(robots_update, shelves_update)

        frontend.end()  # TODO: misleading function name, should be "loop"

    if summary:
        logging.info("Order was: %s", order)
        logging.info("Best solution is: %s", solution)
        logging.info("Objective function value is: %d", result)

    if graph_proc and gantt:
        graph_proc.join()
