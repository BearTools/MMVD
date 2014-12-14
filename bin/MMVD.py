#!/usr/bin/env python

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
def main(warehouse, robots, order):
    """
    Start application and:
    - load specified warehouse map
    - load initial robots positions
    - load specific order
    """
    return run_application(click.format_filename(warehouse),
                           click.format_filename(robots),
                           click.format_filename(order))

if __name__ == "__main__":
    main()
