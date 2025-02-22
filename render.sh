#!/usr/bin/env bash

script_path="$(dirname $(realpath $0))"

filename=$1

target=$(get-target.py "${filename}")
target_dirpath=$(dirname "${target}")

mkdir -p "output/${target_dirpath}"
# --template
# --standalone?
pandoc -i "processed/${filename}" -o "output/${target}.html" --from markdown+backtick_code_blocks+yaml_metadata_block+tex_math_dollars+auto_identifiers --mathml  --toc --template "${script_path}/template/main.html"

