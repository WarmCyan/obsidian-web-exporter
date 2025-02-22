#!/usr/bin/env bash

script_path="$(dirname $(realpath $0))"

rm -rf "${script_path}/notes"
rm -rf "${script_path}/processed"
rm -rf "${script_path}/output"

echo "Extracting public notes..."
extract-public.sh
echo "Processing..."
process.py
echo "Rendering..."
render-all.sh
echo "Copying resources..."
copy-resources.sh
