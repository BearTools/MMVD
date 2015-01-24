# coding: utf-8


def gantt_values(states, dropzone):
    """
    Generate data for each robot from given list of states that is later fed
    to Gantt chart generating function :func:`gantt_chart()`.

    :param list states: complete solution states
    :param tuple dropzone: drop zone coordinates
    :return: data that helps generating Gantt chart
    :rtype: dict
    """
    # robot: [(start_index, stop_index, product)]
    data = {robot: [] for robot in range(len(states[0]))}

    for index, state in enumerate(states):

        for robot, pos_y, pos_x, product in state:
            if (pos_y, pos_x) == dropzone:
                # close if possible
                if len(data[robot]) and not data[robot][-1][1]:
                    data[robot][-1][1] = index

            else:
                if not len(data[robot]) or (len(data[robot]) and
                                            data[robot][-1][1]):
                    # start new
                    data[robot].append([index, None, product])
                else:
                    # update product
                    data[robot][-1][2] = product

    return data


def gantt_chart(data, savename=None, show=False):
    """
    Generate Gantt chart.

    :param data: something returned by :func:`gantt_values` function
    """
    import matplotlib.pyplot as plt
    from matplotlib.colors import cnames

    colors_ = cnames.values()

    max = 0
    i = 0
    for robot in data.keys():
        for start_index, stop_index, product in data[robot]:
            plt.hlines(robot, start_index, stop_index, label=product, lw=10,
                       color=colors_[i])
            if max < stop_index:
                max = stop_index

            i += 1

    # add some styling
    plt.margins(0.1)
    plt.grid()
    plt.xticks(range(max + 2))
    plt.yticks(range(len(data.keys())))
    plt.legend()

    if savename:
        plt.savefig(savename)
    if show:
        plt.show()

    return True
