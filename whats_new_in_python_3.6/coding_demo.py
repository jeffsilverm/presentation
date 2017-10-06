#! /usr/bin/python3.6
#  -*- coding: utf-8 -*-
#
# Demonstrates how Python3.6 handles coding issues

import sys
import locale
print("Running python version %s.%s.%s" % ( sys.version_info.major, sys.version_info.minor, sys.version_info.micro ), file=sys.stderr )

print("The current system default locale is ", locale.getpreferredencoding(), file=sys.stderr )

def eprint(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)

# This list of codecs is from https://docs.python.org/3/library/codecs.html#standard-encodings
# cp850 is western Europe, cp737 is Greek, cp856
CODECS_LIST = ['ascii', 'utf-8', 'utf-16', 'cp850', 'cp737', 'cp856']
FILENAME="Ishmael"

text_dict = { "English": "Call me Ishmael",
                "Hebrew": "התקשר אלי ישמעאל",
              "Spanish": "Llamame Ishmael",
"Greek": "Καλέστε μου Ishmael"}

text = " ".join(text_dict.values())

for codec in CODECS_LIST:
    eprint("Writing using codec: "+codec )
    with open(FILENAME+"."+codec, mode="w", encoding=codec, errors='replace') as f:
        f.write(codec+"\n")
        f.write(text)

new_text=dict()
for codec in CODECS_LIST:
    print("Reading using codec: "+codec, file=sys.stderr )
    with open(FILENAME+"."+codec, mode="r", encoding=codec, errors='replace') as f:
        codec_name = f.readline()
        if codec != codec_name[:-1]:
            eprint(f"codec {codec} is not the same as the codec named in the file {codec_name[:-1]}")
        new_text[codec] = f.read()

for codec in CODECS_LIST:
    eprint("Testing using codec: "+codec )
    if text == new_text[codec] :
        eprint("Good")
    else:
        eprint(f"BAD.  Original was {text} read back was {new_text[codec]}")








