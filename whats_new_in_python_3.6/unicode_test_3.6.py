#! /usr/bin/python3.6
# -*- coding: utf-8 -*-
#
#
import sys
print("\u0589 \u05d0 \u05d1  ג")

# Note that the Hebrew is backwards...
print("""
Daniel  דניאל    דניאל   Unicode
Isaac    יצחק Unicode
Judith    יהודית  Unicode
Sarah    שרה Unicode
""")

# The 2nd column is the Hebrew in the "correct" order
# The 3rd column is the order that the code arrived in when I pasted it
print("""
Daniel  לאינד    דניאל   Unicode
Isaac    קחצי     יצחק   Unicode
Judith    יתדוהי  יהודית Unicode
Sarah    הרש שרה  Unicode
""")

# Unicode characters are allowed as identifier names.  See PEP 3131
# https://www.python.org/dev/peps/pep-3131/
ΑΒΓΔΕ = "ΑΒΓΔΕ"
αβγδε = "αβγδε"
print("It's all Greek to me: {ΑΒΓΔΕ} or lower case {αβγδε}")

sys.stdout.write("Writing a string " + ΑΒΓΔΕ + "\n" )
