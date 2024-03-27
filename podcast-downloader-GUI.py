import os
import requests
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from xml.etree import ElementTree
import threading
import configparser

config = configparser.ConfigParser()

if os.path.exists('config.ini'):
    config.read('config.ini')
    default_concurrent_downloads = int(config.get('Settings', 'default_concurrent_downloads'))
    default_use_threading = config.getboolean('Settings', 'default_use_threading')
else:
    # Default settings
    default_concurrent_downloads = 1
    default_use_threading = False

def download_podcasts(feed_url, output_location, max_episodes=9999999999999, concurrent_downloads=default_concurrent_downloads, use_threading=default_use_threading):
    if not feed_url or not output_location:
        messagebox.showerror("Error", "Feed URL and output location must be specified.")
        return

    if not os.path.exists(output_location):
        os.makedirs(output_location)

    try:
        feed_xml = requests.get(feed_url).text
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Error downloading feed: {e}")
        return

    root = ElementTree.fromstring(feed_xml)

    url_list = [item.find('./enclosure').get('url') for item in root.findall('./channel/item')][:max_episodes]
    title_list = [item.find('./title').text for item in root.findall('./channel/item')][:max_episodes]
    guid_list = [item.find('./guid').text for item in root.findall('./channel/item')][:max_episodes]

    if use_threading:
        thread_pool = []

    for i, (url, title, guid) in enumerate(zip(url_list, title_list, guid_list), start=1):
        after_slash = url.split('/')[-1]
        file_name = after_slash.split('?')[0]
        file_extension = file_name.split('.')[-1]

        if f"{feed_url} • {guid}" in open('podarchive.txt').read():
            print(f"Skipping episode \"{title}\" because it has already been downloaded.")
        else:
            try:
                if use_threading:
                    if len(thread_pool) >= concurrent_downloads:
                        for thread in thread_pool:
                            thread.join()
                        thread_pool = []
                    thread = threading.Thread(target=download_episode, args=(url, title, file_extension, output_location))
                    thread.start()
                    thread_pool.append(thread)
                else:
                    download_episode(url, title, file_extension, output_location)

                with open('podarchive.txt', 'a') as archive_file:
                    archive_file.write(f"{feed_url} • {guid}\n")

            except requests.RequestException as e:
                messagebox.showerror("Error", f"Error downloading episode \"{title}\": {e}")

        if i >= max_episodes:
            break

    if use_threading:
        for thread in thread_pool:
            thread.join()

    messagebox.showinfo("Download Complete", "All downloads complete.")

def download_episode(url, title, file_extension, output_location):
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(os.path.join(output_location, f"{title}.{file_extension}"), 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)

def browse_output_location():
    output_location = filedialog.askdirectory()
    if output_location:
        output_location_entry.delete(0, tk.END)
        output_location_entry.insert(tk.END, output_location)

def on_download_click():
    feed_url = feed_url_entry.get()
    output_location = output_location_entry.get()

    download_podcasts(feed_url, output_location)

def open_settings_window():
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")

    concurrent_downloads_frame = tk.Frame(settings_window)
    concurrent_downloads_frame.pack(pady=5)

    concurrent_downloads_label = tk.Label(concurrent_downloads_frame, text="Default Concurrent Downloads:")
    concurrent_downloads_label.pack(side=tk.LEFT)

    concurrent_downloads_entry = tk.Entry(concurrent_downloads_frame, width=10)
    concurrent_downloads_entry.pack(side=tk.LEFT)
    concurrent_downloads_entry.insert(tk.END, default_concurrent_downloads)

    threading_frame = tk.Frame(settings_window)
    threading_frame.pack(pady=5)

    threading_var = tk.BooleanVar(value=default_use_threading)
    threading_checkbox = tk.Checkbutton(threading_frame, text="Use Threading", variable=threading_var)
    threading_checkbox.pack()

    def save_settings():
        config['Settings'] = {
            'default_concurrent_downloads': concurrent_downloads_entry.get(),
            'default_use_threading': str(threading_var.get())
        }
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        messagebox.showinfo("Settings Saved", "Settings have been saved successfully.")

    save_button = tk.Button(settings_window, text="Save Settings", command=save_settings)
    save_button.pack()

root = tk.Tk()
root.title("Podcast Downloader")

download_button = tk.Button(root, text="Download", command=on_download_click)
download_button.pack()

# Settings button
settings_button = tk.Button(root, text="Settings", command=open_settings_window)
settings_button.pack()

root.mainloop()
