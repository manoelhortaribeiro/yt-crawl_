#!/bin/bash

# Path to the file containing the lines
file="./data/2_all_to_disambiguate.csv"
pathv="/scratch/manoel/miniconda3/bin/yt-dlp"

pids=()
counter=0
counterglobal=0

# Loop through each line in the file
while IFS= read -r line; do

    counterglobal=$((counterglobal + 1))

    line2=${line//\//_}

    
    echo "$counterglobal,$line,$line2,$($pathv --quiet --no-warnings --ignore-errors  --playlist-items 0 -O playlist:channel_url "$line")" >> ./data/3_mapping.csv &
    pids[${counter}]=$!

    counter=$((counter + 1))

    if ((counter % 500 == 0)); then
        echo "$counter"
        # Reset counter
        for pid in ${pids[*]}; do
            wait $pid
        done
        # Reset counter and pids
        counter=0
        pids=()
    fi

    sleep 0.01
done < "$file"