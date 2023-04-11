#!/bin/bash

# specify the directory to perform the replacement in
dir="scripts"

# loop through all files and directories in the specified directory
for file in "$dir"/*; do
    # check if the file name contains "-"
    if [[ "$file" == *-* ]]; then
        # replace "-" with "_"
        new_file="${file//-/_}"
        # rename the file with the new name
        mv "$file" "$new_file"
    fi
done
