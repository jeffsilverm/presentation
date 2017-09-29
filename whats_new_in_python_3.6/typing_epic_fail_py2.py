#! /usr/bin/python
#  -*- coding: utf-8 -*-
#
# Demonstrates why use typing - this does not and it will fail.  Why?
#
# This version uses comments to annotate types, and will work (and fail) until python 2.7 as well as python 3.6
# http://mypy.readthedocs.io/en/latest/python2.html
import typing
from typing import Dict


def get_first_name(full_name) :
    # Type: -> str
    return full_name.split(" ")[0]

fallback_name = {
    "first_name": "UserFirstName",
    "last_name": "UserLastName"
}   # Type: Dict

raw_name = input("Please enter your name: ")    # Type: str
first_name = get_first_name(raw_name)   # Type: str

# If the user didn't type anything in, use the fallback name
if not first_name:
    first_name = get_first_name(fallback_name)  # Type: str

print("Hi, %s!" % first_name )