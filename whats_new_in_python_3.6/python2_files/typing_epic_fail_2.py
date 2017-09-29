#! /usr/bin/python
#  -*- coding: utf-8 -*-
#
# Demonstrates why use typing - this does not and it will fail.  Why?
#
# Works (or fails) equally well on python 2.7 and 3.6 (and 3.5)
# Description: no hinting, , python2 or python3, 2 calls to get_first_name
#
import sys

print(("Running on python version %s" % sys.version ))

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

# if
if not first_name:
    first_name = get_first_name(fallback_name)


print(("Hi, %s!" % first_name ))

