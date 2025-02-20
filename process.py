#!/usr/bin/env python

import re
import os


file_to_url = {}


# process for url properties
for filename in os.listdir("notes"):
    print(filename)

    # by default just do a "safe" filename as url
    note_name = filename[:filename.rindex(".")]
    safe_note_name = note_name.replace(" ", "-").lower()
    file_to_url[note_name] = safe_note_name

    with open(f"notes/{filename}", 'r') as infile:
        lines = infile.readlines()

    # get yaml if there
    yaml_lines = []
    if lines[0] == "---\n":
        i = 1
        while lines[i] != "---\n":
            yaml_lines.append(lines[i])
            i += 1

    print(yaml_lines)

    # find the url yaml property
    for line in yaml_lines:
        if line.strip().startswith("url:"):
            file_to_url[note_name] = line[line.index("url:") + 4:].strip()

print(file_to_url)
