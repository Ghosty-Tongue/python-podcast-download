import os
import requests
from xml.etree import ElementTree

def download_podcasts(feed_url, folder_name, max_episodes=9999999):
    if not feed_url or not folder_name:
        print("Error: Feed URL and folder name must be specified.")
        return

    folder_path = os.path.join(os.getcwd(), folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    try:
        feed_xml = requests.get(feed_url).text
    except requests.RequestException as e:
        print(f"Error downloading feed: {e}")
        return

    root = ElementTree.fromstring(feed_xml)

    url_list = [item.find('./enclosure').get('url') for item in root.findall('./channel/item')][:max_episodes]
    title_list = [item.find('./title').text for item in root.findall('./channel/item')][:max_episodes]
    guid_list = [item.find('./guid').text for item in root.findall('./channel/item')][:max_episodes]

    for i, (url, title, guid) in enumerate(zip(url_list, title_list, guid_list), start=1):
        after_slash = url.split('/')[-1]
        file_name = after_slash.split('?')[0]
        file_extension = file_name.split('.')[-1]

        if f"{feed_url} â¢ {guid}" in open('podarchive.txt').read():
            print(f"Skipping episode \"{title}\" because it has already been downloaded.")
        else:
            try:
                response = requests.get(url, stream=True)
                response.raise_for_status()

                with open(os.path.join(folder_path, f"{title}.{file_extension}"), 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            file.write(chunk)

                with open('podarchive.txt', 'a') as archive_file:
                    archive_file.write(f"{feed_url} â¢ {guid}\n")

            except requests.RequestException as e:
                print(f"Error downloading episode \"{title}\": {e}")

        if i >= max_episodes:
            break

    print("All downloads complete.")

if __name__ == "__main__":
    folder_name = input("Enter the folder name where files will be saved: ")
    feed_url = input("Enter the RSS feed URL: ")

    download_podcasts(feed_url, folder_name)
