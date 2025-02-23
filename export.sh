#!/usr/bin/env bash

notes_path="$1"
export_path="$2"

script_path="$(dirname $(realpath $0))"

rm -rf "${script_path}/notes"
rm -rf "${script_path}/processed"
rm -rf "${script_path}/output"

echo "Extracting public notes..."
extract-public.sh "${notes_path}"
echo "Processing..."
process.py
echo "Rendering..."
render-all.sh
echo "Copying resources..."
copy-resources.sh
echo "Exporting to ${export_path}..."
rsync -r "${script_path}/output" "${export_path}" --info=progress2
