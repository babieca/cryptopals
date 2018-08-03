#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Fixed XOR

Write a function that takes two equal-length buffers and produces their XOR combination.

If your function works properly, then when you feed it the string:

    1c0111001f010100061a024b53535009181c

... after hex decoding, and when XOR'd against:

    686974207468652062756c6c277320657965

... should produce:

    746865206b696420646f6e277420706c6179
'''
#import sys
import binascii

def hexxor(x_hex, y_hex, endinness='big'):
    '''
        param
            X: in hexadecimal
            Y: in hexadecimal
            endiness (optional): [big,littel] (default big endian)
        return
            xor of X and Y in bytes
    '''
    
    if len(x_hex) < len(y_hex):
        print("error, len(x) < len(y). Cutting len(y) to match len(x)")
        y_hex = y_hex[:len(x_hex)]
    elif len(x_hex) > len(y_hex):
        print("error, len(x) > len(y)")
        return
    
    print("X: {}\nY: {}". format(x_hex, y_hex))
          
    x_bytes = binascii.unhexlify(x_hex)
    y_bytes = binascii.unhexlify(y_hex)
    
    print("X(bytes): {}\nY(bytes): {}". format(x_bytes, y_bytes))
    
    #byord = sys.byteorder  # <-- 'little endian'
    
    x_int = int.from_bytes(x_bytes, byteorder=endinness, signed=False)
    y_int = int.from_bytes(y_bytes, byteorder=endinness, signed=False)
    
    print("X(int): {}\nY(int): {}". format(x_int, y_int))
    
    print("X(bits): {:08b}\nY(bits): {:08b}". format(x_int, y_int))
    
    enc_int = x_int ^ y_int
    
    print("X^Y(int): {}\nX^Y(bits): {:08b}\nX^Y(hex): {}". format(enc_int, enc_int, hex(enc_int)))
    
    return enc_int.to_bytes(len(x_hex), byteorder=endinness, signed=False)

def to_bytes(n, length, endianess='big'):
    h = '%x' % n
    s = ('0'*(len(h) % 2) + h).zfill(length*2).decode('hex')
    return s if endianess == 'big' else s[::-1]

def hexxor2(a, b):    # xor two hex strings of the same length
    return "".join(["%x" % (int(x,16) ^ int(y,16)) for (x, y) in zip(a, b)])

def main():
    x_hex = "1c0111001f010100061a024b53535009181c"
    y_hex = "686974207468652062756c6c277320657965"
    
    hexxor(x_hex, y_hex)

if __name__ == "__main__":
    # execute only if run as a script
    main()