#!/usr/bin/env python

import re
import os
import json


file_to_name = {}  # Thing.md: Thing

name_to_url = {}  # Thing: thing

file_contents = {}  # Thing.md: ...


# process for url properties
for filename in os.listdir("notes"):

    if not filename.endswith(".md"):
        # TODO: handle images and stuff too
        continue
    
    print(filename)

    # by default just do a "safe" filename as url
    note_name = filename[:filename.rindex(".")]
    safe_note_name = note_name.replace(" ", "-").lower()
    name_to_url[note_name] = safe_note_name
    file_to_name[filename] = note_name

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
    # file_contents[filename] = "\n".join(lines[i:])
    # (no actually not necessary since pandoc can handle)
    # add title property to yaml
    # yaml_lines.append(f"title: {note_name}\n"
    file_contents[filename] = "\n".join(lines)

    # find the url yaml property
    for line in yaml_lines:
        if line.strip().startswith("url:"):
            name_to_url[note_name] = line[line.index("url:") + 4:].strip()

print(name_to_url)
print(file_contents)

# find and replace all links
for filename, contents in file_contents.items():
    print("\n", filename)
    matches = re.findall(r"\[\[([A-Za-z0-9\-\_\s]*)\]\]", contents)
    for match in matches:
        pattern = f"[[{match}]]"
        if match in name_to_url:
            replacement = f"[{match}]({name_to_url[match]}.html)"
        else:
            replacement = match
        contents = contents.replace(pattern, replacement)
        file_contents[filename] = contents

print("\n")
print(file_contents)

os.makedirs("processed", exist_ok=True)
for filename in file_contents:
    with open(f"processed/{filename}", 'w') as outfile:
        outfile.write(file_contents[filename])

with open("processed/data.json", 'w') as outfile:
    data = {
        "file_to_name": file_to_name,
        "name_to_url": name_to_url,
    }
    json.dump(data, outfile, indent=4)
