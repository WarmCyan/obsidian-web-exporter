#!/usr/bin/env bash

rm -rf output

for file in processed/*.md; do
  mdname=$(basename "${file}")
  echo "${mdname}"
  ./render.sh "${mdname}"
done
