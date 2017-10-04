#! /usr/bin/python2.7
# -*- coding: utf-8 -*-
#
# This demonstrates that the named parameters in method calls are now ordered
# in python 3.6.  Also demonstrates a case where type annotation actually does
# something useful.
# Description: baseline, a python 3.6 program with kwargs and type annotation
#
# 3to2 added the imports from __future__
from __future__ import absolute_import
# As part of hand-fixing, I removed the import of __future__.print_function
from __future__ import print_function
# As part of hand-fixing, I removed the import of typing, which doesn't exist
# in python 2.7
# import typing
import sys


def subr(arg_a, arg_b=42, arg_c=False, *args,
         **kwargs):
    u"""
    :param arg_a:   type:   any
    :param arg_b:   type:   int
    :param arg_c:   type:   bool
    :param args:
    :param kwargs:
    :return:
    """

    # pycharm doesn't recognize the 40 * u"*" is equivalent to 40 * "*"
    print(u"\n\n", 40 * u"*")
    print(u"arg_a: {}\targ_b: {:d}\t arg_c: {:b}".format(arg_a, arg_b, arg_c))
    for i, arg in enumerate(args):
        print(i, arg)
    print(40 * u"-")
    for k in kwargs:
        print(u"kwargs[{}]={}".format(k, kwargs[k]))


print(u"Running python version {:d}.{:d}".format(sys.version_info.major,
                                                 sys.version_info.minor))

subr(arg_a=u"All arguments explicitly named", arg_b=11, arg_c=True,
     kwarg_1=u"one", kwarg_2=u"two", kwarg_3=u"three", kwarg_4=u"four")
# Pycharm detects that there is a data type error in this call
subr(u"no arguments explicitly named", 11, True,
     u"unamed_1", u"unamed_2", u"unamed_3",
     kwarg_1=u"one", kwarg_2=u"two", kwarg_3=u"three", kwarg_4=u"four")
subr(arg_a=u"arg_b is missing", arg_c=True,
     arg_d=u"arg_d_again", kwarg_1=u"one", kwarg_3=u"two", kwarg_2=u"three",
     kwarg_4=u"four")
subr(u"six", 11, truth=True, arg_d=u"arg_d",
     kwarg_1=u"one", kwarg_4=u"two", kwarg_2=u"three", kwarg_3=u"four")
# Uncomment the following line to see mypy report an error or see subr raise
# a ValueError exception.  Pycharm also detects that the data type is wrong
try:
    subr(7.1, 8, u"Bee!", False, u"Sea", u"Eric", u"Gretchen", u"Felicia",
         u"Wu",
         kwarg_1=u"one", kwarg_4=u"four", kwarg_2=u"two", kwarg_3=u"three",
         kwarg_5=u"five", kwarg_6=u"six")
except ValueError as e:
    # In python 2.7, the first arg to write must be str, not unicode
    sys.stderr.write("The subr call with Bee! raised a ValueError exception, "
                     "as expected: {}\n\n".format(str(e)))
else:
    sys.stderr.write("The subr call with Bee! did **not** raise a ValueError "
                    "exception, which is unexpected, in fact it is a FAIL\n\n")
subr(7.2, 6, False, u"Gretchen", u"Felicia", u"Wu")
