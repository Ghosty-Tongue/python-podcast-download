#!/bin/bash

download_podcasts() {
    feed_url=$1
    folder_name=$2

    if [ -z "$feed_url" ]; then
        echo "Error: Feed URL must be specified."
        return
    fi

    if [ -z "$folder_name" ]; then
        folder_path="$HOME/Downloads"
    else
        folder_path="$HOME/Downloads/$folder_name"
    fi

    if [ ! -d "$folder_path" ]; then
        mkdir -p "$folder_path"
    fi

    feed_xml=$(curl -s "$feed_url")

    url_list=($(echo "$feed_xml" | grep -o '<enclosure url="[^"]*' | grep -o 'url="[^"]*' | cut -d'"' -f2))
    title_list=($(echo "$feed_xml" | grep -o '<title>.*</title>' | sed -e 's/<title>//' -e 's/<\/title>//'))
    guid_list=($(echo "$feed_xml" | grep -o '<guid>.*</guid>' | sed -e 's/<guid>//' -e 's/<\/guid>//'))

    for ((i = 0; i < ${#url_list[@]}; i++)); do
        url="${url_list[i]}"
        title="${title_list[i]}"
        guid="${guid_list[i]}"

        after_slash=$(basename "$url")
        file_name=$(echo "$after_slash" | cut -d'?' -f1)
        file_extension=$(echo "$file_name" | rev | cut -d'.' -f1 | rev)

        episode_folder="$folder_path/$title"

        if [ ! -d "$episode_folder" ]; then
            mkdir -p "$episode_folder"
        fi

        if grep -qFx "$feed_url • $guid" podarchive.txt; then
            echo "Skipping episode \"$title\" because it has already been downloaded."
        else
            if curl -s "$url" | pv -s $(curl -sI "$url" | grep -i Content-Length | awk '{print $2}') -N "$title" | tar -xzf - -C "$episode_folder"; then
                echo "$feed_url • $guid" >>podarchive.txt
            else
                echo "Error downloading episode \"$title\"."
            fi
        fi
    done

    echo "All downloads complete."
}

read -p "Enter the RSS feed URL: " feed_url

download_podcasts "$feed_url"
