import os
import re
import tkinter as tk
from tkinter import filedialog
from pytube import YouTube
import youtube_dl


class Downloader:
    def __init__(self, master=None, url=None, output_folder=None):
        self.master = master
        self.master.title("YouTube Downloader")
        self.url = url
        self.output_folder = output_folder
        self.status = ""
        self.progress = ""
        self.download = None

        # Create input fields for URL and output folder path
        self.url_label = tk.Label(self.master, text="YouTube Video URL:")
        self.url_label.pack()
        self.url_entry = tk.Entry(self.master)
        self.url_entry.pack()

        self.output_folder_label = tk.Label(self.master, text="Output Folder Path:")
        self.output_folder_label.pack()
        self.output_folder_entry = tk.Entry(self.master)
        self.output_folder_entry.pack()

        # Create a button to start the download
        self.download_button = tk.Button(self.master, text="Download", command=self.download)
        self.download_button.pack()


    def get_video_info(self):
        """Get video info from YouTube."""
        self.video = YouTube(self.url)
        self.video_title = self.video.title
        self.stream = self.video.streams.filter(only_audio=True).first()
        self.file_size = self.stream.filesize

    def download_video(self):
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(self.output_folder, '%(title)s.%(ext)s'),
            'progress_hooks': [self.progress_hook],
        }
        
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            self.download = ydl.extract_info(self.url, download=True)

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            self.progress = f"{d['_percent_str']} of {d['_total_bytes_str']}"
        elif d['status'] == 'finished':
            self.status = "Download completed!"
        elif d['status'] == 'error':
            self.status = "Error during download!"
    
    def cancel_download(self):
        if self.download:
            self.download.cancel()
            self.status = "Download cancelled."


def validate_url(url):
    """Validate if the input URL is a valid YouTube playlist or video URL."""
    regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$"
    if re.match(regex, url):
        return True
    else:
        return False


def download_mp3(url, output_folder, progress_callback):
    """Download YouTube video as mp3 file."""
    dl = Downloader(url, output_folder)
    try:
        dl.get_video_info()
        dl.download_mp3()
        progress_callback(100, "Download completed.")
    except Exception as e:
        if not dl.cancelled:
            progress_callback(-1, str(e))
