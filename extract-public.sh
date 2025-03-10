#!/usr/bin/env bash


notes_path="$1"
echo "${notes_path}"

script_path="$(dirname $(realpath $0))"

rm -rf ${script_path}/notes
mkdir ${script_path}/notes
mkdir ${script_path}/notes/attachments

pushd "${notes_path}"

rg "#public" --no-heading --sort=path | cut -d : -f 1 | uniq | xargs -I src cp src "${script_path}/notes/"

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

# extract any images/attachments found (anything with an actual extension)
rg "#public" --no-heading --sort=path | cut -d : -f 1 | uniq | xargs -d "\n" rg --no-heading -e "\[\[.*\.(jpg|png|svg|JPG|PNG|SVG|txt|pdf)\]\]" | cut -d : -f 2 | sed -e "s/.*\[\[\([a-zA-Z0-9\-\_\.\s]*\)\]\]/\1/g" | xargs -I src cp attachments/src "${script_path}/notes/attachments/"


popd
