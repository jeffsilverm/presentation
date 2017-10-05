#! /usr/bin/python
#
# This program implements single character input without waiting for a new line character
# USE CAUTION - IT MAY DISABLE CONTROL-C and CONTROL-D
#
# As currently written, it will run with either python 2.7 or python 3.6 on linux
#
#                       python 2.7  python 3.6
# linux Ubuntu 17.4     tested
# linux Fedora 26
# Windows/10
# Mac OS X
#
# From https://stackoverflow.com/questions/510357/python-read-a-single-character-from-the-user
from __future__ import print_function  # put at top of file if using Python 2


def getChar():
    # figure out which function to use once, and store it in _func
    if "_func" not in getChar.__dict__:
        try:
            # for Windows-based systems
            import msvcrt # If successful, we are on Windows
            getChar._func=msvcrt.getch

        except ImportError:
            # for POSIX-based systems (with termios & tty support)
            import tty, sys, termios # raises ImportError if unsupported

            def _ttyRead():
                fd = sys.stdin.fileno()
                oldSettings = termios.tcgetattr(fd)

                try:
                    tty.setcbreak(fd)
                    answer = sys.stdin.read(1)
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings)

                return answer

            getChar._func=_ttyRead

    return getChar._func()

if __name__ == "__main__" :

    # Example of a prompt for one character of input
    promptStr = "Please give me a character:"
    responseStr = "Thank you for giving me a '{}'."
    print(promptStr, end="\n> ")
    answer = getChar()
    print("\n")
    print(responseStr.format(answer))

