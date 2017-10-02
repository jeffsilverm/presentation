#! /usr/bin/python
# -*- coding: utf-8 -*-
#
# This demonstrates that the named parameters in method calls are now ordered
# in python 3.6
from __future__ import print_function

import sys


def subr(arg_a: any, arg_b: int =42, arg_c: bool=False, *args, **kwargs):
    """
    :param arg_a:   type:   any
    :param arg_b:   type:   int
    :param arg_c:   type:   bool
    :param args:
    :param kwargs:
    :return:
    """

    print("\n\n")
    print("arg_a: {}\targ_b: {:d}\t arg_c: {:b}".format(arg_a, arg_b, arg_c))
    for arg in args:
        print(arg)
    print(40*"-")
    for k in kwargs:
        print("kargs[{}]={}".format(k, kwargs[k]))


print("Running python version {:d}.{:d}".format(sys.version_info.major,
                                                sys.version_info.minor))

subr ( arg_a="All arguments explicitly named", arg_b=11, arg_c=True,
       arg_d="arg_d", arg_e="Detroit", complex=3.4+2j, new_jersey="Trenton" )
subr ( "six", 11, truth=True, arg_d="arg_d", arg_e="Chicago",
       my_dictionary={'q':5, 'r':3}, maine="Portland")
subr ( 7.1, "Bee!", "Sea", "Eric", "Gretchen", "Felicia", "Wu", p="P", w="W",
       seven=7 )


