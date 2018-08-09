#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''

Detect single-character XOR

One of the 60-character strings in this file has been encrypted by single-character XOR.

Find it.

(Your code from #3 should help.)

'''
import string
from libcrypt.common import readfile
from libcrypt.lcrypt import is_hex, hexxor, freqchars

def main():
    fname = r"C:\Users\Laptop2\Desktop\tmp\challenge4.txt"
    lines = readfile(fname)
    
    keyspace = string.ascii_letters + string.digits
    keyshex = dict((el.encode('ascii').hex(),0) for el in list(keyspace))
    
    freqhex = freqchars()
    
    for line in lines:
        for (c1, c2) in zip(line[0::2], line[1::2]):
            # C1 + C2 is 1 char size or 1 byte
            ciphertext = c1+c2


if __name__ == "__main__":
    # execute only if run as a script
    main()