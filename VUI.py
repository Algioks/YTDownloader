import os
import re
import threading
import time
import tkinter as tk
from tkinter import filedialog
from pytube import Playlist
import youtube_dl

class DownloadStatus:
    def __init__(self, parent):
        self.parent = parent
        self.status_var = tk.StringVar()
        self.status_var.set("Waiting for download...")

        self.status_label = tk.Label(parent, textvariable=self.status_var)
        self.status_label.pack()

    def update_status(self, message):
        self.status_var.set(message)

class PlaylistDownloader:
    def __init__(self, parent):
        self.parent = parent
        self.playlist_link = tk.StringVar()
        self.output_folder = tk.StringVar()

        self.playlist_label = tk.Label(parent, text="Playlist Link:")
        self.playlist_label.pack()
        self.playlist_entry = tk.Entry(parent, textvariable=self.playlist_link, width=50)
        self.playlist_entry.pack()

        self.output_label = tk.Label(parent, text="Output Folder:")
        self.output_label.pack()
        self.output_entry = tk.Entry(parent, textvariable=self.output_folder, width=50)
        self.output_entry.pack()
        self.output_button = tk.Button(parent, text="Select Folder", command=self.select_folder)
        self.output_button.pack()

        self.download_button = tk.Button(parent, text="Download Playlist", command=self.download)
        self.download_button.pack()

        self.status = DownloadStatus(parent)

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        self.output_folder.set(folder_path)

    def download(self):
        playlist_link = self.playlist_link.get()
        output_folder = self.output_folder.get()

        if not playlist_link:
            self.status.update_status("Please enter a playlist link.")
            return

        if not output_folder:
            self.status.update_status("Please select an output folder.")
            return

        try:
            playlist = Playlist(playlist_link)
            playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
            os.makedirs(output_folder, exist_ok=True)

            for url in playlist.video_urls:
                t = threading.Thread(target=self.download_mp3, args=(url, output_folder))
                t.start()

        except Exception as e:
            self.status.update_status(f"Error: {str(e)}")

    def download_mp3(self, url, output_folder):
        try:
            yt = youtube_dl(url)
            stream = yt.streams.filter(only_audio=True).first()
            stream.download(output_folder)

            # Rename file to match YouTube video title
            original_file_name = stream.default_filename
            new_file_name = re.sub(r'\.webm$', '.mp3', original_file_name)
            os.rename(os.path.join(output_folder, original_file_name), os.path.join(output_folder, new_file_name))

            self.status.update_status(f"Downloaded {yt.title}")

        except Exception as e:
            self.status.update_status(f"Error while downloading {url}: {str(e)}")

def main():
    root = tk.Tk()
    root.title("Playlist Downloader")
    root.geometry("500x300")
    app = PlaylistDownloader(root)
    root.mainloop()

if __name__ == '__main__':
    main()
