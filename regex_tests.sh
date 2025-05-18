#!/usr/bin/env bash


regex="s/.*\[\[([a-zA-Z0-9\-\_\.\s[:space:]]*)\]\]/\1/g"


echo "![[testing.png]]" | sed -r -e ${regex}
echo "![[Pasted image 20250418105140.png]]" | sed -r -e ${regex}


