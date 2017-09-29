#! /usr/bin/python3.6
# -*- coding: utf-8 -*-

import decimal
import datetime
import sys
print("Running python version {}".format(sys.version_info) )

# From https://docs.python.org/3/whatsnew/3.6.html#whatsnew36-pep498
name = "Fred"
print ( f"He said his name is {name}." )
width = 10
precision = 4
value_str = "12.123_456_789_0"
value = decimal.Decimal(value_str)
print( f"value_str is {value_str} result: {value:{width}.{precision}}")  # nested fields
for w in range(20,9,-1):
    print(f"result: {value:{w}.{24-w}}")
print("String literals using the format protocol")
print ("He said his name is {}".format(name) )
print ("result: ")

# From https://docs.python.org/2/tutorial/inputoutput.html
# or x in range(1,11):
# ...     print '{0:2d} {1:3d} {2:4d}'.format(x, x*x, x*x*x)
print("The following works quite nicely in python 2.7")
print("*{:6,d}*".format(1000000000))
print("*{:12,d}*".format(1000000000))
print("*{:24,d}*".format(1000000000))
for i in range(13,24):
    fstr="*{:"+str(i)+",d}*"
    print(fstr.format(1000000000))

# See https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior
# Compare https://docs.python.org/2/library/datetime.html#id1 with
# https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
d = datetime.datetime(2017, 10, 7, 12, 15, 58)
print ('{:%Y-%m-%d %H:%M:%S}'.format(d) )

print("I may have found a bug in strfmt in the standard C library")
print("""September, 1752, was an interesting month:
jeffs@jeffs-laptop:~ $ cal sep 1752
   September 1752   
Su Mo Tu We Th Fr Sa
       1  2 14 15 16 
17 18 19 20 21 22 23 
24 25 26 27 28 29 30 
                     
                     
                     
jeffs@jeffs-laptop:~ $ 
""")

print('{:%a %Y-%m-%d}'.format(datetime.date(1752,8,31)))
for day in range(1,31):
    do = datetime.date(1752,9,day)
    print('{:%a %Y-%m-%d}'.format(do) )
print('{:%a %Y-%m-%d}'.format(datetime.date(1752,10,1)))






