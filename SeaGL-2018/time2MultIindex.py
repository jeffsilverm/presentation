#! /usr/bin/python
# -*- coding: utf-8 -*-
#
#
# This program converts the output of the measure2.sh bash script into a
# pandas multiframe and then saves
# it in a file

# For debugging
import pprint
import sys
from typing import Tuple, List

import numpy as np
import pandas as pd

pp = pprint.PrettyPrinter(indent=2, width=80)


def parse_line(i: int, line: str, filename: str) -> Tuple:
    """
    :param  i: the line number, used to report errors
    :param line: a line from the time file
    :param filename: str  in case of an error
    :return: a tuple of size (int), loss (float), delay (float),
    protocol (string, either "IPv4" or "IPv6"
    """
    words = line.split()
    if words[0] != "parameters":
        raise ValueError(
            f"In line {i} of file {filename}, words {words[0]} should be "
            f"'parameters'")
    size: List = words[1].split("=")
    if size[0] != "SIZE":
        raise ValueError(
            f"In line {i} of file {filename}, words {words[1]} should begin "
            f"with 'SIZE'")
    size: str = size[1][:-5]  # e.g. 2048.data becomes 2048
    size: int = int(size)  # pycharm needs that type hint

    loss: List = words[2].split("=")
    if loss[0] != "LOSS":
        raise ValueError(
            f"In line {i} of file {filename}, words {words[2]} should begin "
            f"with 'LOSS'")
    loss = float(loss[1])
    delay: List = words[3].split("=")
    if delay[0] != "DELAY":
        raise ValueError(
            f"In line {i} of file {filename}, words {words[3]} should begin "
            f"with 'DELAY'")
    delay = float(delay[1])
    protocol: List = words[4].split("=")
    if protocol[0] != "PROTOCOL":
        raise ValueError(
            f"In line {i} of file {filename}, words {words[4]} should begin "
            f"with 'PROTOCOL'")
    protocol: str = protocol[1]
    if protocol != "IPv4" and protocol != "IPv6":
        raise ValueError(
            f"In line {i} of file {filename}, words {words[4]} should have "
            f"value either 'IPv4' or 'IPv6'"
            f"begin with 'PROTOCOL'")
    elapsed = float(words[5])
    bandwidth: float = float(size) / elapsed
    return size, loss, delay, protocol, bandwidth


def load_data(filename: str) -> Tuple:
    """

    :param filename: A string which is the name of the file that contains the
    data
    :return: A tuple.  The first element is a list of indexes.  The second
    element is the data
    """
    with open(filename, "r") as f:
        contents = f.readlines()

    # The data dictionary, keyed by a tuple of the values of each degree of
    # freedom

    d3 = dict()
    all_values_list = list()
    for i in range(len(contents)):
        values: Tuple[int, float, float, str, float] = parse_line(i,
                                                                  contents[i],
                                                                  filename)
        (size, loss, delay, protocol, bandwidth) = values
        d3[(size, loss, delay, protocol)] = bandwidth
        all_values_list.append([size, loss, delay, protocol, bandwidth])

    # Just a list of the independent variables
    parameter_name_list = ['SIZE', 'LOSS', 'DELAY', 'PROTOCOL']
    values_list = list(d3.values())

    np_array = np.array(all_values_list)

    # assert len(parameter_name_list) == len(d3.keys()), \
    #    f"The length of the parameter_name_list, {len(parameter_name_list)}" \
    #    f" is not the same as the length of d3.keys, {len(d3.keys())}."
    mux = pd.MultiIndex.from_tuples(d3.keys(), names=parameter_name_list)
    # A MultiIndex DataFrame
    data_frame_mi = pd.DataFrame(values_list, index=mux, columns=['bandwidth'])
    data_frame_mi.rename_axis(axis=1, mapper="data_rate", inplace=True)
    # A DataFrame that just has columns
    data_frame_cs = pd.DataFrame(columns=parameter_name_list + ['bandwidth'],
                                 data=np_array)

    return data_frame_mi, data_frame_cs


if "__main__" == __name__:
    file_name = sys.argv[1]
    df_mi, df_cs = load_data(filename=file_name)
    print(df_mi)  # MultiIndex
    print(df_cs)  # 5 column regular DataFrame
    output_filename = file_name + '.h5'
    store = pd.HDFStore(output_filename)
    store['df_mi'] = df_mi
    store['df_cs'] = df_cs
    print("The dataframes were saved in " + output_filename)
    store.close()
    #
