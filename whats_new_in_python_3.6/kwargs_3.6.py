#! /usr/bin/python3.6
# -*- coding: utf-8 -*-
#
# This demonstrates that the named parameters in method calls are now ordered
# in python 3.6.  This version is the original, written for python 2.7
# Description: kwargs.py converted to python 3.6 using 2to3.
import sys


def subr(arg_a, arg_b=42, arg_c=False, *args, **kwargs):
    """
    :param arg_a:   type:   any
    :param arg_b:   type:   int
    :param arg_c:   type:   bool
    :param args:
    :param kwargs:
    :return:
    """

    print("\n\n", 40 * "*")
    print("arg_a: {}\targ_b: {:d}\t arg_c: {:b}".format(arg_a, arg_b, arg_c))
    for i, arg in enumerate(args):
        print(i, arg)
    print(40 * "-")
    for k in kwargs:
        print("kwargs[{}]={}".format(k, kwargs[k]))


print("Running python version {:d}.{:d}".format(sys.version_info.major,
                                                sys.version_info.minor))

# kwarg_1="one", kwarg_2="two", kwarg_3="three", kwarg_4="four"
subr(arg_a="All arguments explicitly named", arg_b=11, arg_c=True,
     kwarg_1="one", kwarg_2="two", kwarg_3="three", kwarg_4="four")
# Pycharm detects that there is a data type error in this call
subr("no arguments explicitly named", 11, True,
     "unamed_1", "unamed_2", "unamed_3",
     kwarg_1="one", kwarg_2="two", kwarg_3="three", kwarg_4="four")
subr(arg_a="arg_b is missing", arg_c=True,
     arg_d="arg_d_again", kwarg_1="one", kwarg_3="two", kwarg_2="three",
     kwarg_4="four")
subr("six", 11, truth=True, arg_d="arg_d",
     kwarg_1="one", kwarg_4="two", kwarg_2="three", kwarg_3="four")
# Uncomment the following line to see mypy report an error or see subr raise
# a ValueError exception.  Pycharm also detects that the data type is wrong
try:
    subr(7.1, 8, "Bee!", False, "Sea", "Eric", "Gretchen", "Felicia", "Wu",
         kwarg_1="one", kwarg_4="four", kwarg_2="two", kwarg_3="three",
         kwarg_5="five", kwarg_6="six")
except ValueError as e:
    sys.stderr.write("The subr call with Bee! raised a ValueError exception, "
                     "as expected: {}\n\n".format(str(e)))
else:
    sys.stderr.write("The subr call with Bee! did **not** raise a ValueError "
                     "exception, which is unexpected, in fact it is a FAIL\n\n")
subr(7.2, 6, False, "Gretchen", "Felicia", "Wu")
