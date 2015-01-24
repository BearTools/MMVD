#!/usr/bin/env python
# coding: utf-8
import click
import logging
from mmvdApp.main import run_application

_click_path = click.Path(exists=True, dir_okay=False, readable=True,
                         resolve_path=False)


@click.command()
@click.argument("warehouse", type=_click_path)
@click.argument("robots", type=_click_path)
@click.argument("order", type=_click_path)
@click.option("--gantt/--no-gantt", default=True,
              help="whether or not to generate Gantt chart to visualize "
              "handling order by robots")
@click.option("--gui/--no-gui", default=True,
              help="whether or not to visualize robot movements in Tk GUI")
@click.option("--tabu-rounds", default=10**3, help="number of Tabu iterations")
@click.option("--tabu-memory", default=5,
              help="number of Tabu items held in short-term memory")
@click.option("--verbose/--no-verbose", default=False,
              help="how loud should the program output be")
def main(warehouse, robots, order, gantt, gui, tabu_rounds, tabu_memory,
         verbose):
    """
    Start application and load specific warehouse map from WAREHOUSE, load
    initial robots positions from ROBOTS.  Finally load products order from
    ORDER.

    All paths must be readable, existing files.
    """
    # if verbose, allow DEBUG, too
    verbosity_level = 10 if verbose else 20
    logging.basicConfig(format='%(levelname)s: %(message)s',
                        level=verbosity_level)

    return run_application(click.format_filename(warehouse),
                           click.format_filename(robots),
                           click.format_filename(order),
                           gantt, gui, tabu_rounds, tabu_memory)

if __name__ == "__main__":
    main()
