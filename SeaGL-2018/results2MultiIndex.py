#! /usr/bin/python
# -*- coding: utf-8 -*-
#
#
# This program converts the output of the measure2.sh bash script into a
# pandas multiframe and then saves
# it in a file

import re
import sys
from typing import Tuple, List

import pandas as pd

# For debugging
import pprint
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
    get_bytes_per_sec_pc = re.compile("""\((\d*?\.\d*?) MB\/s\)""")

    # Get the names of all of the indices
    parameter_name_list = []
    parameter_value_list = []
    parameter_idx_list = []
    with open(filename, "r") as f:
        contents = f.readlines()
        word_list = contents[0].split()
        for j in range(len(word_list)):
            word=word_list[j]
            if "=" not in word:
                continue
            kv_pair = word.split("=")
            parameter_name_list.append(kv_pair[0])   # The key
            parameter_value_list.append(kv_pair[1])  # The value
            parameter_idx_list.append(j)

    # The data dictionary, keyed by a tuple of the values of each degree of
    # freedom
    d3 = dict()
    for i in range(0, len(contents), 2):
        keys_list = []
        # There will be one match in this line, but it won't be at the start of the line
        # The end of the number will be followed by the string " MB/s)" which we want to filterr
        # out, hence the [1:-6)
        data_rate_str: str = get_bytes_per_sec_pc.search(contents[i + 1])[0][1:-6]
        data_rate_value: float = float(data_rate_str)
        words = contents[i].split()
        for j in range(0, len(words)):
            key, value = words[j].split("=")
            assert key == parameter_name_list[j] and value == \
                parameter_value_list[j], \
                f"In line {i}, word {j} shouold be " \
                f"{parameter_name_list[j]}={parameter_value_list[j]}" \
                f"but is actually {key}={value}"
            keys_list.append(value)
        keys_tuple = tuple(keys_list)
        d3[keys_tuple] = data_rate_value
    mux = pd.MultiIndex.from_tuples(d3.keys(), levels=len(parameter_name_list),
                                    names=parameter_name_list)
    data_frame = pd.DataFrame(list(d3.values()), index=mux)
    return parameter_name_list, data_frame


if "__main__" == __name__:
    parameter_name_lst, df = load_data(sys.argv[1])
