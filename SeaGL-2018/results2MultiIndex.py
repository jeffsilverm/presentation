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
from typing import Tuple, List

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
    for i in range(0, len(contents), 2):
        # Get the names of all of the indices
        parameter_name_list = []
        parameter_value_list = []
        word_list: List[str] = contents[i].split()
        for j in range(len(word_list)):
            word: str = word_list[j]
            if "=" not in word:
                continue
            kv_pair: List[str] = word.split("=")
            # This is a special case.  The sizes come from the file name and the
            # filename always ends with .data
            if ".data" in kv_pair[1]:
                end = kv_pair[1].find(".data")
                kv_pair[1] = kv_pair[1][:end]
            parameter_name_list.append(kv_pair[0])  # The key
            parameter_value_list.append(kv_pair[1])  # The value
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

    mux = pd.MultiIndex.from_tuples(d3.keys(), names=parameter_name_list)
    data_frame = pd.DataFrame(list(d3.values()), index=mux)
    return parameter_name_list, data_frame


if "__main__" == __name__:
    file_name = sys.argv[1]
    parameter_name_lst, df = load_data(filename=file_name)
    print(df)
    output_filename = file_name + '.h5'
    store = pd.HDFStore(output_filename)
    store['df'] = df
    print("The dataframe was saved in " + output_filename)
    store.close()
    #
