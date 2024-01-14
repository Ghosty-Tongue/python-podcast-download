import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# Description: A Python script to download most recent media from a podcast XML feed
#
# Usage: Execute the script and provide the RSS feed URL.
#
# Based on script by Wowfunhappy under the original Bash command-line code
# Modified to Python by GhostyTongue, adapting Wowfunhappy's modifications from the Bash script
#
# Licence: GNU v3.0

# Set the maximum number of episodes to download
max_episodes = 9999999

# Input RSS feed URL
feed = input("Enter the RSS feed URL: ")

# Create download folder named 'downloaded_podcast'
folder = 'downloaded_podcast'

# Check if feed is empty
if not feed:
    print("Error: No feed specified")
    exit()

# Create destination folder if it doesn't exist
if not os.path.exists(folder):
    os.makedirs(folder)

retry_count = 1
feed_xml = None

while not feed_xml and retry_count <= 10:
    try:
        response = requests.get(feed)
        response.raise_for_status()
        feed_xml = response.text
    except requests.exceptions.RequestException:
        retry_count += 1

# Parse XML using BeautifulSoup
soup = BeautifulSoup(feed_xml, 'xml')

# Extract enclosure URLs
url_list = [enclosure['url'] for enclosure in soup.find_all('enclosure')]

# Get the xml | extract title elements | remove literal "<title>" | remove literal "</title>" and add newline | remove empty lines | replace colons | correct ampersands
title_list = [title.text.strip().replace(':', ' -').replace('&amp;', '&') for title in soup.find_all('title')]

# Get the xml | extract guid elements | remove literal guid opening tag | remove literal "</guid>" and add newline | remove empty lines
guid_list = [guid.text.strip() for guid in soup.find_all('guid')]

# Ensure the existence of the podarchive.txt file
podarchive_file = 'podarchive.txt'
if not os.path.exists(podarchive_file):
    with open(podarchive_file, 'w'):
        pass

for i, url in enumerate(url_list):
    if i >= max_episodes:
        break

    title = title_list[i]
    guid = guid_list[i]

    after_slash = url.split('/')[-1]
    file_name = after_slash.split('?')[0]
    file_extension = file_name.split('.')[-1]

    if f"{feed} â¢ {guid}" in open(podarchive_file).read():
        print(f"Skipping episode \"{title}\" because it has already been downloaded.")
    else:
        print(f"Preparing to download episode \"{title}\"...")
        # Repeat in case downloads break mid-transfer.
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            file_size = int(response.headers.get('content-length', 0))
            block_size = 8192
            with tqdm(total=file_size, unit='B', unit_scale=True, desc=title, ncols=80) as progress_bar:
                with open(os.path.join(folder, f"{title}.{file_extension}"), 'wb') as file:
                    for chunk in response.iter_content(chunk_size=block_size):
                        file.write(chunk)
                        progress_bar.update(len(chunk))
            with open(podarchive_file, 'a') as archive_file:
                archive_file.write(f"{feed} â¢ {guid}\n")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading episode \"{title}\": {e}")

print("All downloads complete.")
