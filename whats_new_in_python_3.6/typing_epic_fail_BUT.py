#! /usr/bin/python3.6
#  -*- coding: utf-8 -*-
#
# Demonstrates why use typing - this does and it will fail, BUT the problem
# will be detected by mypy.
# Description: type hinting, hints in code, python3.6
#
import __future__
from typing import Dict
import sys

print("Running python version %s.%s.%s" % ( sys.version_info.major, sys.version_info.minor, sys.version_info.micro ) )
assert sys.version_info.major >= 3, "Must run under Python 3.x or greater"



def get_first_name(full_name: str) -> str:
    return full_name.split(" ")[0]

fallback_name: Dict[str, str] = {
    "first_name": "UserFirstName",
    "last_name": "UserLastName"
}

raw_name: str  = input("Please enter your name: ")
first_name: str  = get_first_name(raw_name)

# If the user didn't type anything in, use the fallback name
if not first_name:
    first_name: str = get_first_name(fallback_name)

print(f"Hi, {first_name}!")
