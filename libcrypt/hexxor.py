#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import string
import binascii

def is_hex(s):
    hex_digits = set(string.hexdigits)
    # if s is long, then it is faster to check against a set
    return all(c in hex_digits for c in s)

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
