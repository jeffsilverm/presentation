#! /usr/bin/python3.6
#  -*- coding: utf-8 -*-
#
# Demonstrates why use typing - this program does and mypy will detect the problem
# This program is NOT version agnostic, only 3.6
# Python 2 and 3:
from __future__ import print_function
# Python 2 and 3:
from builtins import input



def get_first_name(full_name: str ) -> str:
    return full_name.split(" ")[0]


fallback_name = {
    "first_name": "UserFirstName",
    "last_name": "UserLastName"
}

raw_name = input("Please enter your name: ")
first_name: str = get_first_name(raw_name)

# If the user didn't type anything in, use the fallback name
if not first_name:
    first_name: str = get_first_name(fallback_name)

print("Hi, {} !".format(first_name))
