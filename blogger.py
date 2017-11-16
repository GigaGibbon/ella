#!/usr/bin/env python

import os
import json
import sys

if len(sys.argv) != 2:
    print("Usage:")
    print("\tblogger.py config.json")
    sys.exit(1)

config = {}
with open(sys.argv[-1], 'r') as f:
    config = json.load(f)

