#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import string      # definitions of ascii printable chars
import requests
import os
import binascii
import base64
from libcrypt.common import wfile


def hexToBase64(s):

    decoded = binascii.unhexlify(s)
    encoded = base64.b64encode(decoded).decode('ascii')
    return encoded

def to_bytes(n, length, endianess='big'):
    h = '%x' % n
    s = ('0'*(len(h) % 2) + h).zfill(length*2).decode('hex')
    return s if endianess == 'big' else s[::-1]

''' this is guaranteed to work with UTF-8 encoding
    (because all bytes in multi-byte characters have
    the highest bit set to 1).
''' 
def removeNonAscii(s):
    return "".join(i for i in s if ord(i)<128)

def char2hex(c):
    return "{:02x}".format((ord(c)))

def is_hex(s):
    hex_digits = set(string.hexdigits)
    # if s is long, then it is faster to check against a set
    return all(c in hex_digits for c in s)

def freqchars():
    # define text - from url
    top10_books = {
        'https://www.gutenberg.org/files/1342/1342-0.txt', # Pride and Prejudice, by Jane Austen
        'https://www.gutenberg.org/files/11/11-0.txt', # Alice�s Adventures in Wonderland, by Lewis Carroll
        'https://www.gutenberg.org/files/2701/2701-0.txt', # Moby Dick; or The Whale, by Herman Melville
        'https://www.gutenberg.org/files/30254/30254-0.txt', # The Romance of Lust, by Anonymous
        'http://www.gutenberg.org/cache/epub/1661/pg1661.txt', # The Adventures of Sherlock Holmes, by Arthur Conan Doyle
        'https://www.gutenberg.org/files/74/74-0.txt', # The Adventures of Tom Sawyer, Complete by
        'http://www.gutenberg.org/cache/epub/345/pg345.txt', # Dracula, by Bram Stoker
        'https://www.gutenberg.org/files/98/98-0.txt', # A Tale of Two Cities, by Charles Dickens
        'https://www.gutenberg.org/files/57594/57594-0.txt', # The Western Echo, by George W. Romspert
        'http://www.gutenberg.org/cache/epub/6130/pg6130.txt', # The Iliad of Homer by Homer
        }
    
    text = ''
    
    fname = 'C:\\Users\\Laptop2\\Desktop\\tmp\\books.txt'

    asciihex = dict(("{:02x}".format(el),0) for el in range(0,128))
    
    if not os.path.isfile(fname) or os.stat(fname).st_size == 0:
     
        for url in top10_books:
            text += requests.get(url).text.strip()
            
        text = removeNonAscii(text)
        wfile(fname, text)
    else:
        with open(fname, 'r', encoding='ascii', errors='ignore') as books:
            text=books.read()
    
    for c in text.lower():              # loop over each character
        if ord(c) < 128:   # Only ASCII code
            asciihex[char2hex(c)] += 1   # Add 1 to the dictionary
    
    total = sum(asciihex.values(), 0.0)
    freqdic = {k: v / total for k, v in asciihex.items()}
    
    for c in string.ascii_lowercase:
        freqdic[char2hex(c.upper())] = freqdic[char2hex(c)]
    
    # sort descending
    freqdic = dict(sorted(freqdic.items(), key=lambda kv: kv[1], reverse=True))
    
    #printJSON(freqdic)    # print all frequencies
    
    return freqdic


def hexxor(x_hex, y_hex, endinness='big'):
    '''
        param
            X: in hexadecimal
            Y: in hexadecimal
            endiness (optional): [big,littel] (default big endian)
        return
            xor of X and Y in bytes
        
        Note
            endines:
                import sys
                endiness = sys.byteorder  # <-- 'little' or 'big'
    '''
    if not is_hex(x_hex):
        if isinstance(x_hex, int):
            x_hex = str(x_hex)
        else:
            print("Error: X must be hex")
            return -1
    if not is_hex(y_hex):
        if isinstance(y_hex, int):
            y_hex = str(y_hex)
        else:
            print("Error: Y must be hex")
            return -1
    
    if len(x_hex) < len(y_hex):
        print("error, len(x) < len(y). Cutting len(y) to match len(x)")
        y_hex = y_hex[:len(x_hex)]
    elif len(x_hex) > len(y_hex):
        print("error, len(x) > len(y)")
        return
          
    x_bytes = binascii.unhexlify(x_hex)
    y_bytes = binascii.unhexlify(y_hex)
    
    x_int = int.from_bytes(x_bytes, byteorder=endinness, signed=False)
    y_int = int.from_bytes(y_bytes, byteorder=endinness, signed=False)
    
    enc_int = x_int ^ y_int
    
    #print("X: {}\nY: {}". format(x_hex, y_hex))
    #print("X(bytes): {}\nY(bytes): {}". format(x_bytes, y_bytes))
    #print("X(int): {}\nY(int): {}". format(x_int, y_int))
    #print("X(bits): {:08b}\nY(bits): {:08b}". format(x_int, y_int))
    #print("X^Y(int): {}\nX^Y(bits): {:08b}\nX^Y(hex): {}". format(enc_int, enc_int, hex(enc_int)))
    
    return enc_int.to_bytes(len(x_hex), byteorder=endinness, signed=False)
