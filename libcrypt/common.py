#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' Common functions
'''

import os           # for existsdir(), existsfile(), readfile()
import json         # for printJSON()
import datetime     # for printJSON()

def existsdir(pdir):
    return True if os.path.isdir(pdir) else False

def existsfile(pfile):
    return True if os.path.exists(pfile) else False

def readfile(pfile):
    
    pdir = os.path.dirname(os.path.dirname(pfile))
    
    if not existsdir(pdir): return "Directory does not exist. Please check"
    if not existsfile(pfile): return "File does not exist. Please check"
    
    with open(pfile) as f:
        content = f.readlines()
    
    # to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    
    return content


def wfile(pfile, line):
    
    pdir = os.path.dirname(os.path.dirname(pfile))
    
    if not existsdir(pdir): return "Directory does not exist. Please check"
    
    with open(pfile, 'a') as f:
        f.write(line)


def printJSON(data):
    
    def json_serial(obj):
        """JSON serializer for objects not serializable by default json code"""
    
        if isinstance(obj, (datetime, datetime.date)):
            return obj.isoformat()
        raise TypeError ("Type %s not serializable" % type(obj))

    
    print(json.dumps(data, sort_keys=False, indent=4, default=json_serial))
