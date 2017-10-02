#! /usr/bin/python
# -*- coding: utf-8 -*-
#
# This demonstrates that the named parameters in method calls are now ordered
# in python 3.6
from __future__ import absolute_import
# 3to2 should have either removed this or else left the print function calls as
# functions calls and not as statements
# from __future__ import print_function
# import typing
import sys


def subr(arg_a, arg_b =42, arg_c=False, *args, **kwargs):
    u"""
    :param arg_a:   type:   any
    :param arg_b:   type:   int
    :param arg_c:   type:   bool
    :param args:
    :param kwargs:
    :return:
    """

    print ("\n\n",40*"*")
    if not isinstance(arg_b, int):
        # I think 3to2 caught that you can't use a format string in 2.7
        # print f"Casting {arg_b} from {type(arg_b)} to str"
        print "Casting {} from {} to str".format(arg_b, str(type(arg_b)))
        arg_b = unicode(arg_b)
    if not isinstance(arg_c, int) and not isinstance(arg_c, bool) :
        # print f"Casting {arg_c} from {type(arg_c)} to bool"
        print "Casting {} from {} to bool".format(arg_c,  str(type(arg_c)) )
        arg_c = bool(arg_c)
    print u"arg_a: {}\targ_b: {:d}\t arg_c: {:b}".format(arg_a, arg_b, arg_c)
    for arg in args:
        print arg
    print 40*u"-"
    for k in kwargs:
        print u"kwargs[{}]={}".format(k, kwargs[k])


print u"Running python version {:d}.{:d}".format(sys.version_info.major,
                                                sys.version_info.minor)

subr ( arg_a=u"All arguments explicitly named", arg_b=11, arg_c=True,
       arg_d=u"arg_d", arg_e=u"Detroit", complex=3.4+2j, new_jersey=u"Trenton" )
subr ( arg_a=u"arg_b is missing", arg_c=True,
       arg_d=u"arg_d_again", arg_e=u"Elbe", BC=u"Victoria", new_jersey=u"Murray Hill" )
subr ( u"six", 11, truth=True, arg_d=u"arg_d", arg_e=u"Chicago",
       my_dictionary={u'q':5, u'r':3}, maine=u"Portland")
# Uncomment the following line to see mypy report an error
# subr ( 7.1, 8, "Bee!", False, "Sea", "Eric", "Gretchen", "Felicia", "Wu", p="P", w="W",seven=7 )
subr ( 7.2, 6, False, u"Gretchen", u"Felicia", u"Wu", p=u"P", w=u"W", seven=7 )


