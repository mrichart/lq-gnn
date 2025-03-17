#!/bin/bash

# Set the directory where your files are located
directory="../../uqsim-results/reduced/social_net_ut"

# Change to the specified directory
cd "$directory" || exit

# Specify the pattern to match files you want to rename
file_pattern="depl_*.out"

# Loop through each file that matches the pattern
for file in $file_pattern; do
    # Replace the string "utMongoIO<number>" with "utMongoIO_<number>"
    new_name=$(echo "$file" | sed 's/utMongoIO\([0-9]\)/utMongoIO_\1/')

    # Rename the file
    mv "$file" "$new_name"

    #echo "Renamed: $file to $new_name"
done
