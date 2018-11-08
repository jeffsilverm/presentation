#! /usr/bin/python3
#  -*- coding: utf-8 -*-

import csv
import datetime
import sys


def str_to_time_delta(string) -> datetime.timedelta:
    """
    :param string:  Input in format 0:01:37.083557
    :return: datetime.timedelta

    """
    flds = string.split(":")
    hours = flds[0]
    minutes = flds[1]
    seconds = flds[2]
    td = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
    return td


# From
# with open('eggs.csv', 'w', newline='') as csv_file:
#    spamwriter = csv.writer(csv_file, delimiter=' ',
#                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
#
with open(file=sys.argv[2], mode="w", newline="") as csv_file:
    spamwriter = csv.writer(csv_file)
    # git tag MONDAY
    spamwriter.writerow(
        ['retries', 'elapsed', 'delay', 'loss', 'size', 'rate', 'proto', 'GTRs'])
    with open(file=sys.argv[1], mode="r") as f:
        for line in f:
            # format of a line is:
            # Retries: 0 Elapsed time: 0:01:16.489403 Delay: 10.3 loss percent: 20 size: 1000000 bytes data rate:
            # 13073.706432249184 bytes/sec protocol: IPv6
            # I'm not going to do any sanity checking.  I might regret that later
            # 0     "Retries:
            # 1     retries as an string of an integer
            # 2     "Elapsed"
            # 3     "time:"
            # 4     elapsed_time as a string of a datetime.timedelta
            # 5     "Delay:"
            # 6     delay_ms as a string of a float
            # 7     "loss"
            # 8     "percent:"
            # 9     loss_percent as a float
            # 10    "size:"
            # 11    size a string as a integer
            # 12    "bytes"
            # 13    "data"
            # 14    "rate:"
            # 15    data_rate a string as a float
            # 16    "bytes/sec"
            # 17    "protocol:"
            # 18    a string either IPv4 or IPv6
            # After the November 5th, added Global TCP Retries (GTRs)
            # 19:   "Global"
            # 20:   "TCP"
            # 21:   "retries:"
            # 22    GTRs a string as an int
            fields = line.split()
            # I'm converting the strings to data types and then
            # back to strs again because I am doing some sanity checking
            retries = int(fields[1])
            # Pandas can handle an elapsed time, no need to convert
            elapsed_time = fields[4]
            delay_ms = float(fields[6])
            loss_percent = float(fields[9])
            size = int(fields[11])
            data_rate = float(fields[15])
            if fields[18] == "IPv4":
                protocol = "IPv4"
            elif fields[18] == "IPv6":
                protocol = "IPv6"
            else:
                raise ValueError("fields[18] should be 'IPv4' or 'IPv6' but is "
                                 f"{fields[18]}")
            gtrs = int(fields[22])
            row_str = [str(retries), str(elapsed_time), str(delay_ms),
                       str(loss_percent), str(size), str(data_rate), protocol, gtrs]
            spamwriter.writerow(row_str)
