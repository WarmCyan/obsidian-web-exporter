#!/usr/bin/env bash

script_path="$(dirname $(realpath $0))"

rm -rf ${script_path}/notes
mkdir ${script_path}/notes

pushd ~/lazuli

rg "#public" --no-heading --sort=path | cut -d : -f 1 | uniq | xargs -I src cp src ${script_path}/notes/

popd
