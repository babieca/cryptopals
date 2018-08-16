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

import codecs
import binascii
import base64
import re

''' Global variables '''

# Frequencies of English letters in hexadecimal
FREQ_ENG = {"0x20": 0.16803388484629145,    "0x45": 0.09467692662363238,    "0x65": 0.09467692662363238,    \
            "0x54": 0.06863717380164468,    "0x74": 0.06863717380164468,    "0x41": 0.05966659937195416,    \
            "0x61": 0.05966659937195416,    "0x4f": 0.05720860388206428,    "0x6f": 0.05720860388206428,    \
            "0x4e": 0.051667419055882034,   "0x6e": 0.051667419055882034,   "0x49": 0.05145866900917404,    \
            "0x69": 0.05145866900917404,    "0x53": 0.049077518887522015,   "0x73": 0.049077518887522015,   \
            "0x48": 0.04895168789795041,    "0x68": 0.04895168789795041,    "0x52": 0.04491096830313412,    \
            "0x72": 0.04491096830313412,    "0x0a": 0.03863130212892039,    "0x44": 0.03364810446111129,    \
            "0x64": 0.03364810446111129,    "0x4c": 0.031059392623187944,   "0x6c": 0.031059392623187944,   \
            "0x55": 0.022346685898254354,   "0x75": 0.022346685898254354,   "0x4d": 0.01932159271664353,    \
            "0x6d": 0.01932159271664353,    "0x43": 0.018355612108347744,   "0x63": 0.018355612108347744,   \
            "0x57": 0.018074770015148574,   "0x77": 0.018074770015148574,   "0x46": 0.016916940059688516,   \
            "0x66": 0.016916940059688516,   "0x47": 0.016001265439878336,   "0x67": 0.016001265439878336,   \
            "0x59": 0.015058391256739979,   "0x79": 0.015058391256739979,   "0x2c": 0.014622009913052503,   \
            "0x50": 0.01288176600691001,    "0x70": 0.01288176600691001,    "0x42": 0.011659634171154705,   \
            "0x62": 0.011659634171154705,   "0x2e": 0.007863842683007178,   "0x56": 0.007199301895479472,   \
            "0x76": 0.007199301895479472,   "0x4b": 0.006004369623052343,   "0x6b": 0.006004369623052343,   \
            "0x2d": 0.0025372175190010735,  "0x3b": 0.002001544565494238,   "0x27": 0.001829764799038139,   \
            "0x22": 0.0013428133934346856,  "0x4a": 0.001172882140991181,   "0x6a": 0.001172882140991181,   \
            "0x58": 0.0011418535129226314,  "0x78": 0.0011418535129226314,  "0x21": 0.0009601709928276336,  \
            "0x51": 0.0008552018042553057,  "0x71": 0.0008552018042553057,  "0x5f": 0.0008285303877878714,  \
            "0x3f": 0.0006667854116858567,  "0x3a": 0.000617139606776177,   "0x5a": 0.0005244498327160837,  \
            "0x7a": 0.0005244498327160837,  "0x29": 0.00022499056267578213, "0x28": 0.00022433037909985553, \
            "0x31": 0.00020993837714465587, "0x2a": 0.00015580332391867542, "0x32": 0.00011223120790752043, \
            "0x30": 9.691494894602353e-05,  "0x33": 7.328037692785158e-05,  "0x38": 6.98474223330333e-05,   \
            "0x35": 6.549021073191781e-05,  "0x34": 6.245336628265549e-05,  "0x36": 5.6115603953760213e-05, \
            "0x37": 5.571949380820426e-05,  "0x39": 5.373894308042449e-05,  "0x2f": 3.525380295447995e-05,  \
            "0x5b": 1.5316258961496907e-05, "0x7e": 1.5052185531126269e-05, "0x5d": 1.4656075385570314e-05, \
            "0x26": 1.0959047360381407e-05, "0x7d": 9.37460677815759e-06,   "0x7b": 9.110533347786953e-06,  \
            "0x7c": 4.753321746671454e-06,  "0x24": 3.1688811644476354e-06, "0x40": 2.508697588521045e-06,  \
            "0x23": 1.3203671518531816e-06, "0x25": 1.3203671518531816e-06, "0x2b": 1.1883304366678635e-06, \
            "0x3d": 1.1883304366678635e-06, "0x3e": 1.1883304366678635e-06,                                 \
            "0x00": 0.0,"0x01": 0.0,"0x02": 0.0,"0x03": 0.0,"0x04": 0.0,"0x05": 0.0,"0x06": 0.0,"0x07": 0.0,\
            "0x08": 0.0,"0x09": 0.0,"0x0b": 0.0,"0x0c": 0.0,"0x0d": 0.0,"0x0e": 0.0,"0x0f": 0.0,"0x10": 0.0,\
            "0x11": 0.0,"0x12": 0.0,"0x13": 0.0,"0x14": 0.0,"0x15": 0.0,"0x16": 0.0,"0x17": 0.0,"0x18": 0.0,\
            "0x19": 0.0,"0x1a": 0.0,"0x1b": 0.0,"0x1c": 0.0,"0x1d": 0.0,"0x1e": 0.0,"0x1f": 0.0,"0x3c": 0.0,\
            "0x5c": 0.0,"0x5e": 0.0,"0x60": 0.0,"0x7f": 0.0}


''' Generic functions '''

def removeNonAscii(s):
    return "".join(i for i in s if ord(i)<128)

def isHex(data):
    if isinstance(data, str):
        return bool(re.match('^(0[xX])?[0-9a-fA-F]+$', data))
    elif isinstance(data, int):
        return bool(re.match('^(0[xX])?[0-9a-fA-F]+$', "{:#x}".format(data)))
    else:
        raise ValueError('You must specify a string')

def isOct(data):
    if isinstance(data, str):
        return bool(re.match('^(0o)?[0-7]+$', data))
    elif isinstance(data, int):
        return bool(re.match('^(0o)?[0-7]+$', "{:#o}".format(data)))
    else:
        raise ValueError('You must specify a string')

def isBits(data):
    if isinstance(data, str):
        return bool(re.match('^(0b)?[0,1]+$', data))
    elif isinstance(data, int):
        return bool(re.match('^(0b)?[0,1]+$', "{:#b}".format(data)))
    else:
        raise ValueError('You must specify a string')
    
def isBase64(s):
    try:
        return base64.b64encode(base64.b64decode(s)) == s
    except Exception:
        return False

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
    if isBits(bstr):
        return '{:#02o}'.format(int(bstr, 2))
    else:
        raise ValueError('You must specify a string of bits')
def bits2Dec(bstr):
    if isBits(bstr):
        return int(bstr, 2)
    else:
        raise ValueError('You must specify a string of bits')
def bits2Base64(bstr):
    if isBits(bstr):
        return base64.b64encode(int2bytes(int(bstr, 2)))
    else:
        raise ValueError('You must specify a string of bits')
def bits2Str(bstr,encoding='utf-8', errors='surrogatepass'):
    if isBits(bstr):
        return int2bytes(int(bstr, 2)).decode(encoding, errors)
    else:
        raise ValueError('You must specify a string of bits')    
def bits2Hex(bstr):
    if isBits(bstr):
        return '{:#02x}'.format(int(bstr, 2))
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
        return base64.b64encode(int2bytes(int(o, 8)))
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
        return '{:#02x}'.format(int(str(o),8))
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
def dec2Base64(data):
    if isinstance(data, int):
        return base64.b64encode(bytes(data))                   # encodes the 1-byte integer
        # return base64.b64encode(bytes(str(i), 'ascii'))      # encodes the 1-byte character string
    elif isinstance(data, str):
        return base64.b64encode(bytes(int(data)))
    else:
        raise ValueError('You must specify a deciaml value')
def dec2Str(data):
    if isinstance(data, int):
        return '{:}'.format(chr(int(str(data))))
    elif isinstance(data, str):
        return '{:}'.format(chr(int(data)))
    else:
        raise ValueError('You must specify a decimal value')
def dec2Hex(data):
    if isinstance(data, int):
        return '{:#04x}'.format(data)
    elif isinstance(data, str):
        return '{:#04x}'.format(int(data))
    else:
        raise ValueError('You must specify a decimal value')
def dec2Bits(data):
    if isinstance(data, int):
        return '{:#10b}'.format(data)
    elif isinstance(data, str):
        return '{:#10b}'.format(int(data))
    else:
        raise ValueError('You must specify a decimal value')
def dec2Oct(data):
    if isinstance(data, int):
        return '{:#05o}'.format(data)
    elif isinstance(data, str):
        return '{:#05o}'.format(int(data))
    else:
        raise ValueError('You must specify a decimal value')



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
        return ''.join('{0:#04x}'.format(x, 'b') for x in bytearray(s.encode(encoding, errors)))
    else:
        raise ValueError('You must specify a string')
def str2Bits(s, encoding='utf-8', errors='surrogatepass'):
    if isinstance(s, str):
        return ''.join('{0:#010b}'.format(x, 'b') for x in bytearray(s.encode(encoding, errors)))
    else:
        raise ValueError('You must specify a string')
def str2Oct(s, encoding='utf-8', errors='surrogatepass'):
    if isinstance(s, str):
        return ''.join('{0:#04o}'.format(x, 'b') for x in bytearray(s.encode(encoding, errors)))
    else:
        raise ValueError('You must specify a string')
def str2Dec(s, encoding='utf-8', errors='surrogatepass'):
    if isinstance(s, str):
        return ','.join('{0:0d}'.format(x) for x in s.encode(encoding, errors)) 
    else:
        raise ValueError('You must specify a string')
def str2Base64(s, encoding='utf-8', errors='surrogatepass'):
    if isinstance(s, str):
        return base64.b64encode(s.encode(encoding, errors))
    else:
        raise ValueError('You must specify a string')
    


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
    if not isHex(x_hex):
        print("Error: X must be hex")
        return -1
    if not isHex(y_hex):
        print("Error: Y must be hex")
        return -1
    
    if len(x_hex) < len(y_hex):
        print("Warning, len(x) < len(y). Cutting len(y) to match len(x)")
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
