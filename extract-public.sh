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
rg "#public" --no-heading --sort=path | cut -d : -f 1 | uniq | xargs -d "\n" rg --no-heading -e "\[\[.*\.(jpg|png|svg|JPG|PNG|SVG|txt|pdf)\]\]" | cut -d : -f 2 | sed -r -e "s/.*\[\[([a-zA-Z0-9\-\_\.\s[:space:]]*)\]\]/\1/g" | xargs -I src cp attachments/src "${script_path}/notes/attachments/"


# scale down any images with imagemagic
# (see https://www.imagemagick.org/script/command-line-processing.php#geometry)
for imgfilename in ${script_path}/notes/attachements/*.jpg ${script_path}/notes/attachments/*.JPG ${script_path}/notes/attachments/*.png ${script_path}/notes/attachments/*.PNG;
do
  echo -e "Checking size of ${imgfilename}..."
  convert -resize "800x800>" "${imagefilename}" "${imgfilename}"
done


popd
