#!/usr/bin/env python

import json
import sys


inputname = sys.argv[1]

with open("processed/data.json", 'r') as infile:
    data = json.load(infile)

name = data["file_to_name"][inputname]
target = data["name_to_url"][name]

print(target)
