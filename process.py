#!/usr/bin/env python

import re
import os


file_to_url = {}

file_contents = {}


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
    i = 0
    if lines[0] == "---\n":
        i = 1
        while lines[i] != "---\n":
            yaml_lines.append(lines[i])
            i += 1
        i += 1

    # clean out unnecessary markdown pieces for next step, so remove public tag, 
    # remove yaml lines etc
    file_contents[filename] = "\n".join(lines[i:])

    # find the url yaml property
    for line in yaml_lines:
        if line.strip().startswith("url:"):
            file_to_url[note_name] = line[line.index("url:") + 4:].strip()

print(file_to_url)
print(file_contents)

# find and replace all links
for filename, contents in file_contents.items():
    print("\n", filename)
    matches = re.findall(r"\[\[([A-Za-z0-9\-\_\s]*)\]\]", contents)
    for match in matches:
        pattern = f"[[{match}]]"
        replacement = f"[{match}]({file_to_url[match]}.html)"
        contents = contents.replace(pattern, replacement)
        file_contents[filename] = contents

        # contents = re.sub(pattern, replacement, contents)

print("\n")
print(file_contents)
