#! /usr/bin/python
# -*- coding: utf-8 -*-
#
#
# This program converts the output of the measure2.sh bash script into a
# pandas multiframe and then saves
# it in a file

# For debugging
import pprint
import re
import sys
from typing import Tuple, List, Union

import numpy as np
import pandas as pd

pp = pprint.PrettyPrinter(indent=2, width=80)


def load_data(filename: str) -> Tuple:
    """

    :param filename: A string which is the name of the file that contains the
    data
    :return: A tuple.  The first element is a list of indexes.  The second
    element is the data
    """

    # parameters Wed Oct  3 13:16:29 PDT 2018 LOSS=5 DELAY=0.5
    # IPv4--2018-10-03 13:16:29--  ftp://192.168.0.25/8192.data
    # parameters Wed Oct  3 14:01:16 PDT 2018 LOSS=10 DELAY=0.5
    # IPv6!--2018-10-03 14:01:16--  ftp://[
    # 2602:4b:ac60:9b00:bf35:14d2:bba0:ae44]/8192.data
    # get_params_pc = re.compile(""" (\S+?)=(\d*?) """, flags=1)
    # (11.1 MB/s)"
    get_bytes_per_sec_pc = re.compile("""\((\d*?\.\d*?) MB/s\)""")

    with open(filename, "r") as f:
        contents = f.readlines()

    # The data dictionary, keyed by a tuple of the values of each degree of
    # freedom

    d3 = dict()
    parameter_name_list = []
    all_values_list = list()
    for i in range(0, len(contents), 2):
        # Get the names of all of the indices
        parameter_name_list: List[str] = []
        parameter_value_list: List[Union[str, float]] = []
        word_list: List[str] = contents[i].split()
        for j in range(len(word_list)):
            word: str = word_list[j]
            if "=" not in word:
                continue
            kv_pair: List[str] = word.split("=")
            key = kv_pair[0]
            value = kv_pair[1]
            # This is a special case.  The sizes come from the file name and the
            # filename always ends with .data
            if ".data" in value:
                end = value.find(".data")
                value = value[:end]
                value = int(value)
            elif key == "PROTOCOL":
                pass
            elif key in ["LOSS", "DELAY", "bandwidth"]:
                value = float(value)
            else:
                raise ValueError(
                    f"key is {key} but it should be one of LOSS, DELAY, "
                    f"PROTOCOL or BANDWIDTH")
            parameter_name_list.append(key)  # The key
            parameter_value_list.append(value)  # The value
        dict_key_tuple = tuple(parameter_value_list)
        # There will be one match in this line, but it won't be at the start
        # of the line
        # The end of the number will be followed by the string " MB/s)" which
        #  we want to filterr
        # out, hence the [1:-6)
        data_rate_str: str = get_bytes_per_sec_pc.search(contents[i + 1])[0][
                             1:-6]
        data_rate_value: float = float(data_rate_str)
        d3[dict_key_tuple] = data_rate_value
        parameter_value_list.append(data_rate_value)
        all_values_list.append(parameter_value_list)
        pass

    # parameter_name_list.append("data_rate")
    values_list = list(d3.values())

    np_array = np.array(all_values_list)

    mux = pd.MultiIndex.from_tuples(d3.keys(), names=parameter_name_list)
    # A MultiIndex DataFrame
    data_frame_mi = pd.DataFrame(values_list, index=mux, columns=['bandwidth'])
    data_frame_mi.rename_axis(axis=1, mapper="data_rate", inplace=True)
    # A DataFrame that just has columns
    data_frame_cs = pd.DataFrame(columns=parameter_name_list + ['bandwidth'],
                                 data=np_array)

    return parameter_name_list, data_frame_mi, data_frame_cs


if "__main__" == __name__:
    file_name = sys.argv[1]
    parameter_name_lst, df_mi, df_cs = load_data(filename=file_name)
    print(df_mi)
    print(df_cs)
    output_filename = file_name + '.h5'
    store = pd.HDFStore(output_filename)
    store['df_mi'] = df_mi
    store['df_cs'] = df_cs
    print("The dataframes were saved in " + output_filename)
    store.close()
    #
