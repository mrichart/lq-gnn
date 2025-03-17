#!/bin/bash

# Set the directory where your files are located
directory="../../uqsim-results/exp_uqsim_4tier/"

# Change to the specified directory
cd "$directory" || exit

# Specify the pattern to match files you want to rename
file_pattern="deployment_edge_fog_cloud_kqps_*.out"

# Loop through each file that matches the pattern
for file in $file_pattern; do
    # Replace underscores only between "edge" and "fog" and between "fog" and "cloud"
    new_name=$(echo "$file" | sed 's/edge_fog/edge-fog/' | sed 's/fog_cloud/fog-cloud/')

    # Rename the file
    mv "$file" "$new_name"

    #echo "Renamed: $file to $new_name"
done

# Specify the pattern to match files you want to rename
file_pattern="deployment_edge_cloud_kqps_*.out"

# Loop through each file that matches the pattern
for file in $file_pattern; do
    # Replace underscores only between "edge" and "fog" and between "fog" and "cloud"
    new_name=$(echo "$file" | sed 's/edge_cloud/edge-cloud/')

    # Rename the file
    mv "$file" "$new_name"

    #echo "Renamed: $file to $new_name"
done

# Specify the pattern to match files you want to rename
file_pattern="deployment_edge_fog_kqps_*.out"

# Loop through each file that matches the pattern
for file in $file_pattern; do
    # Replace underscores only between "edge" and "fog" and between "fog" and "cloud"
    new_name=$(echo "$file" | sed 's/edge_fog/edge-fog/')

    # Rename the file
    mv "$file" "$new_name"

    #echo "Renamed: $file to $new_name"
done
