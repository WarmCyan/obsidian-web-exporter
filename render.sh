#!/usr/bin/env bash

filename=$1

target=$(get-target.py "${filename}")
target_dirpath=$(dirname "${target}")

mkdir -p "output/${target_dirpath}"
# --template
pandoc -i "processed/${filename}" -o "output/${target}.html"

