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
from typing import Tuple, List, Union, Match

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
    # (277 MB/s) is also a valid output
    # (136 KB/s) has been seen
    get_bytes_per_sec_str = """\(([0-9.]*) ([MK])B/s\)"""
    get_bytes_per_sec_pc = re.compile(get_bytes_per_sec_str)

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
        if word_list[0] != "parameters":
            raise ValueError(
                f"The first word in line {i} should be 'parameters', but is "
                f"really {word_list[0]}.  The line is \n{contents[i]}\n" +
                ("The line before is \n{contents[i-1]\n" if i > 0 else ""))
        for j in range(len(word_list)):
            word: str = word_list[j]
            if "=" not in word:
                continue
            kv_pair: List[str] = word.split("=")
            key: str = kv_pair[0]
            value: str = kv_pair[1]
            # This is a special case.  The sizes come from the file name and the
            # filename always ends with .data
            if ".data" in value:
                end = value.find(".data")
                value = value[:end]
                value = int(value)
            elif key == "PROTOCOL":
                # value needs no further processing, it can be only be:
                assert value == "IPv4" or value == "IPv6", \
                    f"value is {value} and should be either IPv4 or IPv6, " \
                    f"i={i}, contents[{i}]=\n{contents[i]}"
            elif key == "SERVICE":
                # value needs no further processing, I assume new services
                # will be added in the future
                pass
            elif key in ["LOSS", "DELAY", "bandwidth"]:
                value = float(value)
            else:
                raise ValueError(
                    f"key is {key} but it should be one of LOSS, DELAY, "
                    f"PROTOCOL, SERVICE or BANDWIDTH")
            parameter_name_list.append(key)  # The key
            parameter_value_list.append(value)  # The value
        dict_key_tuple = tuple(parameter_value_list)
        # There will be one match in this line, but it won't be at the start
        # of the line
        mo = [None, None]
        assert len(dict_key_tuple) == 5, f"Length of dict_key_tuple is " \
                                         f"{len(dict_key_tuple)}, i is {i}, " \
                                         f"contents[{i}] is {contents[i]}"
        # This might happen if we run results2MultiIndex.py on a results file
        # that is still getting written to
        if i >= len(contents) - 1:
            print(
                "Exiting perhaps prematurely - are you analyzing data from a "
                "running measurement run?"
                f'  i is {i}, len(contents) is {len(contents)} and\n ' +
                "\n".join(contents[-4:]), file=sys.stderr)
            break
        if "saved" not in contents[i + 1]:
            # If "saved" is not in contents[i+1], then that means wget failed
            # to transfer the file.  This will happen if the loss rate is so
            # high that TCP can't recover.  In that case, just mark the
            # bandwidth as 0, and skip this step
            print(f"'saved' is not in contents[{i+1}],\n{contents[i:i+1]}\n"
                  f"{dict_key_tuple}, so set bandwidth to 0", file=sys.stderr)
            d3[dict_key_tuple] = 0.0
            i -= 1  # Because we're incrementing by 2
            continue
        try:
            # The type hint comes from
            # https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html
            mo: Match[str] = get_bytes_per_sec_pc.search(contents[i + 1])
            if mo is None:
                raise TypeError(
                    f"The search for {get_bytes_per_sec_str} "
                    f"FAILED\ncontents[i+1] for {i} is {contents[i + 1]}")
            data_rate_value: float = float(mo[1])
            if mo[2] == "M":
                data_rate_value *= 1000000
            elif mo[2] == "K":
                data_rate_value *= 1000
            else:
                # Something of a "hail Mary" play
                raise ValueError(f"mo[1] is {mo[1]}  "
                                 f"contents[{i+1}] is \n{contents[i+1]}\n"
                                 f"Continue with 1")
        except TypeError as t:
            print("RE Search failed to find the data rate string. i+1 is "
                  f"{i+1}, contents[i+1] is\n{contents[i+1]}\n{str(t)} "
                  "Continue with 0")
            data_rate_value = 0.0
        except ValueError as v:
            print(f"RE Search returned a bad floating point number: {mo[1]}"
                  f" {str(v)} contents[{i+1} is \n{contents[i+1]}\n"
                  "Continue with 0")
            data_rate_value = 0.0
        except IndexError as v:
            print(f"There is an index error.  i id {i} and len(contents)"
                  f" {str(v)} contents[{i+1} is \n{contents[-5:i]}\n"
                  "Continue with 0")
            data_rate_value = 0.0
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
