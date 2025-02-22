#!/usr/bin/env python

import re
import os
import json


def link_relative_to_self(self_url: str, target_url: str) -> str:
    self_dirs = self_url.split("/")
    target_dirs = target_url.split("/")

    final_link_parts = []

    # find first _non matching_ dir, everything up until that can be removed
    backwards_count = 0
    matching = 0
    for i, dir in enumerate(self_dirs[:-1]):
        if dir != target_dirs[i]:
            # switch to determining how many dirs back
            backwards_count = len(self_dirs[:-1]) - i
            break
        else:
            matching += 1

    final_link_parts.extend([".."] * backwards_count)
    final_link_parts.extend(target_dirs[matching:])

    return "/".join(final_link_parts)


def process():
    file_to_name = {}  # Thing.md: Thing
    name_to_url = {}  # Thing: thing
    file_contents = {}  # Thing.md: ...
    backlinks = {}  # thing: [other-thing, ...] (the actual html links -extension)

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
        # yaml_lines.append(f"title: {note_name}\n")
        file_contents[filename] = "".join(lines)

        # find the url yaml property
        for line in yaml_lines:
            if line.strip().startswith("url:"):
                name_to_url[note_name] = line[line.index("url:") + 4:].strip()

    # find and replace all links
    for filename, contents in file_contents.items():
        self_url = name_to_url[file_to_name[filename]]

        print("\n", filename)
        matches = re.findall(r"\[\[([A-Za-z0-9\-\_\s]*)\]\]", contents)
        for match in matches:
            pattern = f"[[{match}]]"
            if match in name_to_url:
                replacement = f"[{match}]({link_relative_to_self(self_url, name_to_url[match])}.html)"

                # add to backlink tracking
                if name_to_url[match] not in backlinks:
                    backlinks[name_to_url[match]] = []

                backlinks[name_to_url[match]].append((link_relative_to_self(name_to_url[match], self_url), file_to_name[filename]))
            else:
                replacement = match
            contents = contents.replace(pattern, replacement)
            file_contents[filename] = contents

    # add backlinks to yaml
    for filename, contents in file_contents.items():
        lines = contents.split("\n")

        backlinks_this = backlinks[name_to_url[file_to_name[filename]]]
        if len(backlinks_this) > 0:
            backlink_lines = ["backlinks:"] + [f"  - {{url: {link}, name: {name}}}" for link, name in backlinks_this]

            if lines[0] != "---":
                lines.insert(0, "---")
                lines.insert(0, "---")

            for i in range(len(backlink_lines) - 1, -1, -1):
                lines.insert(1, backlink_lines[i])

        # check for a title in yaml
        title_found = False
        for line in lines[1:]:
            if line.startswith("title:"):
                title_found = True
            if line == "---":
                break
        if not title_found:
            lines.insert(1, f"title: {file_to_name[filename]}")

        lines.remove("#public ")

        contents = "\n".join(lines)
        file_contents[filename] = contents

    os.makedirs("processed", exist_ok=True)
    for filename in file_contents:
        with open(f"processed/{filename}", 'w') as outfile:
            outfile.write(file_contents[filename])

    with open("processed/data.json", 'w') as outfile:
        data = {
            "file_to_name": file_to_name,
            "name_to_url": name_to_url,
            "backlinks": backlinks,
        }
        json.dump(data, outfile, indent=4)


if __name__ == "__main__":
    process()
