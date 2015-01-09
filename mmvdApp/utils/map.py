# coding: utf-8


def drop_zone(map):
    """
    Find the drop zone coordinates.
    """
    dz = (-1, -1)

    # TODO: can optimize by breaking the loop
    for row_index, row in enumerate(map):
        for column_index, point in enumerate(row):
            if point == 9 or point == "9":
                dz = (row_index, column_index)

    return dz


def products(map, order):
    """
    Find coordinates for each product in order.
    """
    # CAUTION:
    # Make sure to return coordinates in the same order as corresponding
    # products in `order`
    pass
