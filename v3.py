import tkinter as tk
from tkinter import filedialog
import threading
import os
import sys
import time
import requests
import argparse
from pytube import Playlist, YouTube
import re

class DownloadThread(threading.Thread):
    def __init__(self, url, output_folder, status_bar):
        threading.Thread.__init__(self)
        self.url = url
        self.output_folder = output_folder
        self.status_bar = status_bar

    def run(self):
        try:
            yt = YouTube(self.url)
            stream = yt.streams.filter(only_audio=True).first()
            stream.download(self.output_folder)
        
            # Rename file to match YouTube video title
            original_file_name = stream.default_filename
            new_file_name = re.sub(r'\.webm$', '.mp3', original_file_name)
            os.rename(os.path.join(self.output_folder, original_file_name), os.path.join(self.output_folder, new_file_name))
            
            self.status_bar.config(text=f"Downloaded {self.url}")
        except Exception as e:
            self.status_bar.config(text=f"Error while downloading {self.url}: {e}")

class DownloadManager:
    def __init__(self, playlist_link, output_folder, status_bar):
        self.playlist_link = playlist_link
        self.output_folder = output_folder
        self.status_bar = status_bar
        
        # Set up playlist
        self.playlist = Playlist(self.playlist_link)
        self.playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
        
        # Create output folder if it doesn't exist
        os.makedirs(self.output_folder, exist_ok=True)
        
    def download_all(self):
        # Loop through all videos in playlist and download them as mp3
        for url in self.playlist.video_urls:
            download_thread = DownloadThread(url, self.output_folder, self.status_bar)
            download_thread.start()

def select_folder():
    folder_path = filedialog.askdirectory()
    output_folder_entry.delete(0, tk.END)
    output_folder_entry.insert(0, folder_path)

def download_button_clicked():
    playlist_link = playlist_link_entry.get()
    output_folder = output_folder_entry.get()

    download_manager = DownloadManager(playlist_link, output_folder, status_bar)
    download_manager.download_all()

# Set up UI
root = tk.Tk()
root.title("YouTube Playlist MP3 Downloader")

playlist_link_label = tk.Label(root, text="Playlist Link")
playlist_link_label.grid(row=0, column=0, padx=5, pady=5)

playlist_link_entry = tk.Entry(root)
playlist_link_entry.grid(row=0, column=1, padx=5, pady=5)

output_folder_label = tk.Label(root, text="Output Folder")
output_folder_label.grid(row=1, column=0, padx=5, pady=5)

output_folder_entry = tk.Entry(root)
output_folder_entry.grid(row=1, column=1, padx=5, pady=5)

select_folder_button = tk.Button(root, text="Select Folder", command=select_folder)
select_folder_button.grid(row=1, column=2, padx=5, pady=5)

download_button = tk.Button(root, text="Download", command=download_button_clicked)
download_button.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

status_bar = tk.Label(root, text="")
status_bar.grid(row=3, column=0, columnspan=3, padx=5, pady=5)
root.mainloop()
