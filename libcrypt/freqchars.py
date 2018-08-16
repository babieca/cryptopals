#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os
import string
from libcrypt.lcrypt import str2Hex, removeNonAscii
from libcrypt.common import wfile, printJSON

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

    asciihex = dict(("{:#04x}".format(el),0) for el in range(0,128))
    
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
            asciihex[str2Hex(c).pop(0)] += 1   # Add 1 to the dictionary
    
    total = sum(asciihex.values(), 0.0)
    freqdic = {k: v / total for k, v in asciihex.items()}
    
    for c in string.ascii_lowercase:
        freqdic[str2Hex(c.upper()).pop(0)] = freqdic[str2Hex(c).pop(0)]
    
    # sort descending
    freqdic = dict(sorted(freqdic.items(), key=lambda kv: kv[1], reverse=True))
    
    printJSON(freqdic)    # print all frequencies
    
    return freqdic

if __name__ == "__main__":
    # execute only if run as a script
    freqchars()