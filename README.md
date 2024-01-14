# Podcast Downloader

## Description

A Python script to download media from a podcast XML feed.

### Usage

Execute the script and provide the RSS feed URL when prompted.

```
python podcast_downloader.py
```

# Feed Requirements

```
	<?xml version="1.0" encoding="UTF-8"?>
	<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:media="http://search.yahoo.com/mrss/">
  	<channel>
  		...nodes...
		<item>
			...nodes...
			<enclosure url="http://theFileToDownload.extension"/>
		</item>
		<item>
			...nodes...
			<enclosure url="http://theFileToDownload.extension"/>
		</item>
	</channel>
	</rss>
 ```

### Features

- Downloads podcast episodes based on the provided RSS feed.
- Renames files to the title of the item + original file extension.
- Allows setting start and end parameters to limit the range of downloaded podcasts.

## Prerequisites

Make sure you have the required Python libraries installed:

```
pip install requests beautifulsoup4 tqdm
```

## How to Use

1. Run the script: `python podcast_downloader.py`.
2. Input the RSS feed URL when prompted. Optionally, set start and end episode parameters.
3. The script will download podcast episodes, displaying a progress bar for each download.

## License

This script is licensed under the GNU v3.0 License.

## Credits

- Original Bash script by [Andrew Morton](https://github.com/mortocks) ([GitHub Repository](https://github.com/mortocks/bash-podcast-download)).
- Wowfunhappy's Modified Bash script ([Gist](https://gist.github.com/Wowfunhappy/e042b04a34b25bfe25d04b28914196d4)).
- Modified to Python by GhostyTongue, adapting Wowfunhappy's changes.

## Changelog

- **vForked (12/13/2024):**
  - ~~TODO: Create option to rename files to the title of the item + original file extension.~~ Completed.
    - Files are now renamed to the title of the podcast episode along with the original file extension.
  - ~~TODO: Create start and end parameters to limit the range of downloaded podcasts.~~ Completed.
    - Users can set start and end parameters to download a specific range of episodes.
```
