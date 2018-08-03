#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import datetime

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, datetime.date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

def printJSON(data):
    print(json.dumps(data, sort_keys=False, indent=4, default=json_serial))