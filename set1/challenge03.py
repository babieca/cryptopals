#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Single-byte XOR cipher

The hex encoded string:

    1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736

... has been XOR'd against a single character. Find the key, decrypt the message.

You can do this by hand. But don't: write code to do it for you.

How?
    Devise some method for "scoring" a piece of English plaintext.
    Character frequency is a good metric.
    Evaluate each output and choose the one with the best score.

Achievement Unlocked

    You now have our permission to make "ETAOIN SHRDLU" jokes on Twitter.
'''
import string

from libcrypt.hexxor import hexxor
from libcrypt.freqchars import freqchars

def is_hex(s):
    hex_digits = set(string.hexdigits)
    # if s is long, then it is faster to check against a set
    return all(c in hex_digits for c in s)

def char2hex(c):
    return "{:02x}".format((ord(c)))

def main():
    
    hextext = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
    
    keyspace = string.ascii_letters + string.digits
    keyshex = dict((el.encode('ascii').hex(),0) for el in list(keyspace))
    
    freqhex = freqchars()
    
    for keyhex in keyshex:    
        # 1 Byte length key
        
        for (c1, c2) in zip(hextext[0::2], hextext[1::2]):
            # C1 + C2 is 1 char size or 1 byte
            ciphertext = c1+c2
            
            plaintext_bin = hexxor(ciphertext, keyhex, 'big')
            plaintext_int = int.from_bytes(plaintext_bin, byteorder='big')
            plaintext_hex = '{:02x}'.format(plaintext_int)
            if plaintext_hex in freqhex:
                keyshex[keyhex] += freqhex[plaintext_hex]
    
    keyshex = dict(sorted(keyshex.items(), key=lambda kv: kv[1], reverse=True))
    
    codeascii ="".join(map(chr,range(128)))
    fltr = ''.join([['.', chr(x)][chr(x) in string.printable[:-5]] for x in range(128)])
    
    for k, v in keyshex.items():
        ch = bytes.fromhex(k).decode('utf-8')
        print("ASCII: ""{0:8}""\tHEX: {1:8}\tVALUE: {2:12.8f}\t".format(ch, k, float(v)), end='')
        
        for (ch1, ch2) in zip(hextext[0::2], hextext[1::2]):
            r = hexxor(ch1+ch2, k, 'big').decode("ascii")
            print(r[-1].translate(str.maketrans(codeascii, fltr)), end='')
        print("")

if __name__ == "__main__":
    # execute only if run as a script
    main()