#!/usr/bin/env bash

mkdir -p output/res
cp -r assets/fonts output/res
cp assets/style.css output/res
cp assets/code-syntax-hl.css output/res
cp assets/robots.txt output

mkdir -p output/res/files
cp -r notes/attachments/* output/res/files
