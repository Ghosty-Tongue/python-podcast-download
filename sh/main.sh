#!/bin/bash

download_podcasts() {
    feed_url=$1

    if [ -z "$feed_url" ]; then
        echo "Error: Feed URL must be specified."
        return
    fi

    if [ ! -f "podarchive.txt" ]; then
        touch "podarchive.txt"
    fi

    feed_xml=$(curl -s "$feed_url")

    domain=$(echo "$feed_url" | awk -F/ '{print $3}')
    folder_path="$HOME/Downloads/$domain"

    if [ ! -d "$folder_path" ]; then
        mkdir -p "$folder_path"
    fi

    for enclosure in $(echo "$feed_xml" | grep -o '<enclosure url="[^"]*'); do
        url=$(echo "$enclosure" | sed 's/<enclosure url="//' | sed 's/"//')
        title=$(echo "$enclosure" | grep -o 'title=".*"' | sed 's/title="//' | sed 's/"//')

        if [ -f "$folder_path/${title}.mp3" ]; then
            echo "Skipping episode \"$title\" because it has already been downloaded."
        else
            if curl -s "$url" -o "$folder_path/${title}.mp3"; then
                echo "$feed_url • $title" >> "$folder_path/podarchive.txt"
            else
                echo "Error downloading episode \"$title\"."
            fi
        fi
    done

    echo "All downloads complete."
}

read -p "Enter the RSS feed URL: " feed_url

download_podcasts "$feed_url"
