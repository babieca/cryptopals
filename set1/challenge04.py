#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''

Detect single-character XOR

One of the 60-character strings in this file has been encrypted by single-character XOR.

Find it.

(Your code from #3 should help.)

'''

from libcrypt.common import readfile
from libcrypt.lcrypt import is_hex, hexxor, char2hex

def main():
    fname = r"C:\Users\Laptop2\Desktop\tmp\challenge4.txt"
    lines = readfile(fname)
    
    for line in lines:
        char2hex(line)


if __name__ == "__main__":
    # execute only if run as a script
    main()