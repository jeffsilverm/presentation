#! /usr/bin/python3.6
# -*- coding: utf-8 -*-
#
# secrets.py - a demonstration of the secrets module new in python 3.6
# secrets implements a cryptographically secure random number generator

# PEP-506 describes the motivation for CSPRNG https://www.python.org/dev/peps/pep-0506/

import secrets
import sys
print(sys.version_info, sys.version)


# Generate a ten-character alphanumeric password with at least one lowercase character, at least one uppercase
# character, and at least three digits.
# This works by generating a password from the string of characters and numbers, then testing to see if the password
# meets the criteria.  If not, then loop until you find one that does.

import string
cntr = 0
alphabet = string.ascii_letters + string.digits
while True:
    cntr += 1
    password = ''.join(secrets.choice(alphabet) for i in range(10))
    print("cntr={:d} password is {}".format(cntr, password))
    if (any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and sum(c.isdigit() for c in password) >= 3):
        break
