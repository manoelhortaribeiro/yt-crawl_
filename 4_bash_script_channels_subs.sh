#!/bin/bash

# Path to the file containing the lines
file="./data/4_all_filtered.csv"
pathv="/scratch/manoel/miniconda3/bin/yt-dlp"

pids=()
counter=0
counterglobal=0

# Loop through each line in the file
while IFS= read -r line; do

    counterglobal=$((counterglobal + 1))

    if ((counterglobal == 1)); then
       continue
    fi

    # if ((counterglobal < 3700000)); then
    #     continue
    # fi

    # line2=${sed -n 2p line}
    line2=$(echo "$line" | awk -F "," '{print $2}')

    echo "$line,$($pathv --quiet --no-warnings --ignore-errors  -I0 -O playlist:channel_follower_count "$line2")" >> ./data/5_wsubscribers.csv &
    
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