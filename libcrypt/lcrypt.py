#!/usr/bin/env python3
# -*- coding: utf-8 -*-


''' Library to convert between types: 
        Hex <--> Bits <--> Oct <--> Dec <--> Base64 <-->  Str
    Remove Non Ascii characters
    Check if it is hexadecimal
    
    Format (https://docs.python.org/3.2/library/string.html):
        format_spec ::=  [[fill]align][sign][#][0][width][,][.precision][type]
            fill        ::=  <a character other than '{' or '}'>
            align       ::=  "<" | ">" | "=" | "^"
            sign        ::=  "+" | "-" | " "
            width       ::=  integer
            precision   ::=  integer
            type        ::=  "b" | "c" | "d" | "e" | "E" | "f" | "F" | "g" | "G" | "n" | "o" | "s" | "x" | "X" | "%"
                Strings:
                    's'     String format. This is the default type for strings and may be omitted.
                    None     The same as 's'.
                Integers:
                    'b'     Binary format. Outputs the number in base 2.
                    'c'     Character. Converts the integer to the corresponding unicode character before printing.
                    'd'     Decimal Integer. Outputs the number in base 10.
                    'o'     Octal format. Outputs the number in base 8.
                    'x'     Hex format. Outputs the number in base 16, using lower- case letters for the digits above 9.
                    'X'     Hex format. Outputs the number in base 16, using upper- case letters for the digits above 9.
                    'n'     Number. This is the same as 'd', except that it uses the current locale setting to insert the appropriate number separator characters.
                    None     The same as 'd'.
'''


import string      # definitions of ascii printable chars
import requests
import os
import codecs
import binascii
import base64
import re
from libcrypt.common import wfile


def toBytes(n, length=8, endianess='big'):
    h = '%x' % n
    s = ('0'*(len(h) % 2) + h).zfill(length*2).decode('hex')
    return s if endianess == 'big' else s[::-1]

def removeNonAscii(s):
    return "".join(i for i in s if ord(i)<128)

def char2Hex(s):
    s = removeNonAscii(s)
    return "{:02x}".format((ord(s)))

def isHex(s):
    hex_digits = set(string.hexdigits)
    # if s is long, then it is faster to check against a set
    return all(c in hex_digits for c in s)

def isBitStr(bstr):
    if isinstance(bstr, str):
        return bool(re.match('^(0b)?[0,1]+$', bstr))
    else:
        raise ValueError('You must specify a string')
    
def isBase64(s):
    try:
        return base64.b64encode(base64.b64decode(s)) == s
    except Exception:
        return False

def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))


''' Hexadecimal to:
        Bits
        Octal
        Decimal
        Base64
        String
'''
def hex2Bits(h):
    if isinstance(h, int): h = str(h)         
    num_of_bits = 8
    if isHex(h):
        return bin(int(h, 16))[2:].zfill(num_of_bits)
    else:
        raise ValueError('You must specify a hex value')
def hex2Oct(h):
    if isinstance(h, int): h = str(h)
    if isHex(h):
        return oct(int(h,16))
    else:
        raise ValueError('You must specify a hex value')
def hex2Dec(h):
    if isinstance(h, int): h = str(h)
    if isHex(h):
        return int(h,16)
    else:
        raise ValueError('You must specify a hex value')
def hex2Base64(h):
    if isinstance(h, int): h = str(h)
    if isHex(h):
        decoded = binascii.unhexlify(h)
        encoded = base64.b64encode(decoded).decode('ascii')
        return encoded
    else:
        raise ValueError('You must specify a hex value')
def hex2Str(h):
    if isinstance(h, int): h = str(h)
    if isHex(h):
        return codecs.decode(h, "hex").decode('utf-8')
    else:
        raise ValueError('You must specify a hex value')



''' bits to:
        Octal
        Decimal
        Base64
        String
        Hexadecimal
'''
def bits2Oct(bstr):
    if isBitStr(bstr):
        return '{:#02o}'.format(int(bstr, 2))
    else:
        raise ValueError('You must specify a string of bits')
def bits2Dec(bstr):
    if isBitStr(bstr):
        return int(bstr, 2)
    else:
        raise ValueError('You must specify a string of bits')
def bits2Base64(bstr):
    pass
def bits2Str(bstr,encoding='utf-8', errors='surrogatepass'):
    if isBitStr(bstr):
        return int2bytes(int(bstr, 2)).decode(encoding, errors)
    else:
        raise ValueError('You must specify a string of bits')    
def bits2Hex(bstr):
    if isBitStr(bstr):
        return '{:#02X}'.format(int(bstr, 2))
    else:
        raise ValueError('You must specify a string of bits')



''' Octal to:
        Bits
        Decimal
        Base64
        String
        Hexadecimal
'''
def oct2Dec(o):
    if isinstance(o, int):
        return '{:d}'.format(chr(int(str(o),8)))
    elif isinstance(o, str):
        return '{:d}'.format(int(o,8))
    else:
        raise ValueError('You must specify an octal value')
def oct2Base64(o):
    if isinstance(o, int):
        return '{:d}'.format(int(o,8))
    else:
        raise ValueError('You must specify an octal value')
def oct2Str(o):
    if isinstance(o, int):
        return '{}'.format(chr(int(str(o),8)))
    elif isinstance(o, str):
        return '{}'.format(chr(int(o,8)))
    else:
        raise ValueError('You must specify an octal value')
def oct2Hex(o):
    if isinstance(o, int):
        return '{:#02X}'.format(int(str(o),8))
    else:
        raise ValueError('You must specify an octal value')
def oct2Bits(o):
    if isinstance(o, int):
        return '{:#02X}'.format(int(str(o),8))
    else:
        raise ValueError('You must specify an octal value')


''' Decimal to:
        Bits
        Octal
        Base64
        String
        Hexadecimal
'''
def dec2Base64(i):
    if isinstance(i, int):
        return base64.b64encode(bytes(i))                   # encodes the 1-byte integer
        # return base64.b64encode(bytes(str(i), 'ascii'))   # encodes the 1-byte character string
    else:
        raise ValueError('You must specify an int value')
def dec2Str(i):
    if isinstance(i, int):
        return '{0:01d}'.format(i)
    else:
        raise ValueError('You must specify an int value')
def dec2Hex(i):
    if isinstance(i, int):
        return '{:#04x}'.format(i)
    else:
        raise ValueError('You must specify an int value')
def dec2Bits(i):
    if isinstance(i, int):
        return '{:#10b}'.format(i)
    else:
        raise ValueError('You must specify an int value')
def dec2Oct(i):
    if isinstance(i, int):
        return '{:#05o}'.format(i)
    else:
        raise ValueError('You must specify an int value')



''' Base64 to:
        Bits
        Octal
        Decimal
        String
        Hexadecimal
'''
def base642Str(b64):
    if isBase64(b64):
        return base64.b64decode(b64).decode('utf-8')
    else:
        raise ValueError('Incorrect base64 format')
def base642Hex(b64):
    if isBase64(b64):
        s = base64.b64decode(b64).decode('utf-8')
        return str2Hex(s, 'utf-8', 'surrogatepass')
    else:
        raise ValueError('Incorrect base64 format')
def base642Bits(b64):
    if isBase64(b64):
        s = base64.b64decode(b64).decode('utf-8')
        return str2Bits(s, 'utf-8', 'surrogatepass')
    else:
        raise ValueError('Incorrect base64 format')
def base642Oct(b64):
    if isBase64(b64):
        s = base64.b64decode(b64).decode('utf-8')
        return str2Oct(s, 'utf-8', 'surrogatepass')
    else:
        raise ValueError('Incorrect base64 format')
def base642Dec(b64):
    if isBase64(b64):
        s = base64.b64decode(b64).decode('utf-8')
        return str2Dec(s, 'utf-8', 'surrogatepass')
    else:
        raise ValueError('Incorrect base64 format')



''' String to:
        Bits
        Octal
        Decimal
        Base64
        Hexadecimal
'''
def str2Hex(s, encoding='utf-8', errors='surrogatepass'):
    if isinstance(s, str):
        return ['{0:#04x}'.format(x, 'b') for x in bytearray(s.encode(encoding, errors))]
    else:
        raise ValueError('You must specify a string')
def str2Bits(s, encoding='utf-8', errors='surrogatepass'):
    if isinstance(s, str):
        return ['{0:#010b}'.format(x, 'b') for x in bytearray(s.encode(encoding, errors))]
    else:
        raise ValueError('You must specify a string')
def str2Oct(s, encoding='utf-8', errors='surrogatepass'):
    if isinstance(s, str):
        return ['{0:#04o}'.format(x, 'b') for x in bytearray(s.encode(encoding, errors))]
    else:
        raise ValueError('You must specify a string')
def str2Dec(s, encoding='utf-8', errors='surrogatepass'):
    if isinstance(s, str):
        return ['{0:d}'.format(x, 'b') for x in bytearray(s.encode(encoding, errors))]
    else:
        raise ValueError('You must specify a string')
def str2Base64(s, encoding='utf-8', errors='surrogatepass'):
    if isinstance(s, str):
        return base64.b64encode(s.encode(encoding, errors))
    else:
        raise ValueError('You must specify a string')
    





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
