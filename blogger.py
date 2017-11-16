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

bad_config = False
stanzas_missing = []

# Config handling and setup
def check_stanza(key, description):
    global bad_config, stanzas_missing
    if not key in config:
        bad_config = True
        stanzas_missing.append({'name':key, 'description':description})

check_stanza("outputs", "The output for the ")

if bad_config:
    print("Error parsing config file!\n")
    print("The following stanzas were missing from the config file:\n")
    for st in stanzas_missing:
        print("\tstanza: '{0}'".format(st['name']))
        print("\t{0}\n".format(st['description']))
    sys.exit(1)


