#!/usr/bin/env python
# coding: utf-8

# start application:
# 1 load specified map
# 2 load robots selection
# 3 load order

import click
from mmvdApp.main import run_application

_click_path = click.Path(exists=True, dir_okay=False, readable=True,
                         resolve_path=False)


@click.command()
@click.argument("warehouse", type=_click_path)
@click.argument("robots", type=_click_path)
@click.argument("order", type=_click_path)
@click.option("--gantt/--no-gantt", default=False,
              help="whether or not to generate Gantt chart to visualize "
              "handling order by robots")
def main(warehouse, robots, order, gantt):
    """
    Start application and load specific warehouse map from WAREHOUSE, load
    initial robots positions from ROBOTS.  Finally load products order from
    ORDER.

    All paths must be readable, existing files.
    """
    return run_application(click.format_filename(warehouse),
                           click.format_filename(robots),
                           click.format_filename(order),
                           gantt)

if __name__ == "__main__":
    main()
