#! /usr/bin/python
#  -*- coding: utf-8 -*-
#
# DemonstrateJs why use typing - this program does not and it will fail.  Why?
# This program is version agnostic
# Python 2 and 3:
from __future__ import print_function
import builtins
# Python 2 and 3:
from builtins import input



def get_first_name(full_name):
    return full_name.split(" ")[0]


fallback_name = {
    "first_name": "UserFirstName",
    "last_name": "UserLastName"
}

raw_name = input("Please enter your name: ")
first_name = get_first_name(raw_name)

# If the user didn't type anything in, use the fallback name
if not first_name:
    first_name = get_first_name(fallback_name)

print("Hi, {} !".format(first_name))
