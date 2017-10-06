#! /usr/bin/python3.6
# -*- coding: utf-8 -*-
#
# secrets.py - a demonstration of the secrets module new in python 3.6
# secrets implements a cryptographically secure random number generator

# PEP-506 describes the motivation for CSPRNG https://www.python.org/dev/peps/pep-0506/

import tempfile
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
print(password)

with tempfile.NamedTemporaryFile(delete=False) as f:
    tempfile_name = f.name
    encoded_tempfile_name = tempfile_name+"_base64_encoded.txt"
    decoded_tempfile_name = tempfile_name + "_decoded"
    random_buffer = secrets.token_bytes(1024)
    f.write( random_buffer )
    with open(encoded_tempfile_name, "w+b") as o:
# See https://docs.python.org/3/library/base64.html?highlight=base64#module-base64
        secrets.base64.encode(f, o )


with tempfile.NamedTemporaryFile(delete=True) as f:
    with open(encoded_tempfile_name, mode="r+b") as encoded:
        secrets.base64.decode(encoded, f)
    retreived_random_buffer = f.read(1024)
    if secrets.compare_digest(random_buffer, retreived_random_buffer):
        print("Successfully recovered a token using a random file {}".format(tempfile_name))
    else :
        print("FAILED to recover a token using a random file {}".format(tempfile_name))


