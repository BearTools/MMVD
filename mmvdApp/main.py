#!/usr/bin/env python

# start application:
# 1 load specified map
# 2 load robots selection
# 3 load order

import click
from .utils import read_warehouse_map, read_robots_positions

_click_path = click.Path(exists=True, dir_okay=False, readable=True,
                         resolve_path=False)


@click.command()
@click.argument("warehouse", type=_click_path)
@click.argument("robots", type=_click_path)
@click.argument("order", type=_click_path)
def main(warehouse, robots, order):
    """
    Start application and:
    - load specified warehouse map
    - load initial robots positions
    - load specific order
    """
    map = read_warehouse_map(click.format_filename(warehouse))
    robots = read_robots_positions(click.format_filename(robots))
    # order = click.format_filename(order)


if __name__ == "__main__":
    main()
