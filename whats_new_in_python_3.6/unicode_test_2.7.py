#! /usr/bin/python2.7
# -*- coding: utf-8 -*-
#
#
import sys

print (u"\u0589 \u05d0 \u05d1  ג")

# Note that the Hebrew is backwards. I copied and pasted the text from an
# HTML document which had the characters in the correct order
print """
Daniel  דניאל    דניאל   Unicode
Isaac    יצחק Unicode
Judith    יהודית  Unicode
Sarah    שרה Unicode
"""
# The 2nd column is the Hebrew in the "correct" order
# The 3rd column is the order that the code arrived in when I pasted it
print """
Daniel  לאינד    דניאל   Unicode
Isaac    קחצי     יצחק   Unicode
Judith    יתדוהי  יהודית Unicode
Sarah    הרש שרה  Unicode
"""

# Python 2.7 evidently cannot handle unicode characters in identifiers
# Python 3.6, at least, can.
if sys.version_info.major == 3:
    #    ΑΒΓΔΕ = "ΑΒΓΔΕ"
    #    αβγδε = "αβγδε"
    #    print("It's all Greek to me: {} or lower case {}".format(ΑΒΓΔΕ, αβγδε)
    #    sys.stdout.write("Writing a string " + ΑΒΓΔΕ + "\n" )
    pass
else:
    ABCDE = "ΑΒΓΔΕ"
    abcde = "αβγδε"
    print "It's all Greek to me: {} or lower case {}".format(ABCDE, abcde)
    sys.stdout.write("Writing a string " + ABCDE + "\n")

# שרה

# דניאל
# יצחק
# יהודית
# דניאל
#
