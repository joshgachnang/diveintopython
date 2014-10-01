#!/bin/bash
for file in $(find markdown -name *.md); do
    OUTPUT=$(sed -e's|markdown/|website/|; s|.md|.html|' <<< ${file})
    mkdir -p "$(dirname "$OUTPUT")"
	pandoc -f markdown -t html "${file}" -o $OUTPUT
done
