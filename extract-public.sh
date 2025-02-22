#!/usr/bin/env bash

script_path="$(dirname $(realpath $0))"

rm -rf ${script_path}/notes
mkdir ${script_path}/notes

pushd ~/lazuli

rg "#public" --no-heading --sort=path | cut -d : -f 1 | uniq | xargs -I src cp src ${script_path}/notes/

# get list of names
names="$(ls ${script_path}/notes/*.md)"

# extract edit times
git ls-tree -r --name-only HEAD | while read filename; do
  if [[ "${names}" =~ .*$filename.* ]]; then
    echo "Found edit time for ${filename}"
    modify_time=$(git log -1 --format="%ai" -- "${filename}")
    echo "${filename}:${modify_time}" >> "${script_path}/notes/editdata.dat"
  fi
done

popd
