import os
import sys
import time
import argparse
import threading
import queue
from pytube import Playlist, YouTube
import re

# Set up command line arguments
parser = argparse.ArgumentParser(description='Download MP3 files from a YouTube playlist')
parser.add_argument('playlist_link', help='YouTube playlist link')
parser.add_argument('output_folder', help='Output folder to save MP3 files')
args = parser.parse_args()

# Set up a queue to hold URLs to download
url_queue = queue.Queue()

def download_mp3(url, output_folder):
    """
    Downloads mp3 file from given url and saves it to output folder
    
    Args:
        url (str): URL of the YouTube video
        output_folder (str): Output folder to save MP3 file
    
    Raises:
        Exception: If unable to download video or extract audio stream
    """
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        stream.download(output_folder)
        
        # Rename file to match YouTube video title
        original_file_name = stream.default_filename
        new_file_name = re.sub(r'\.webm$', '.mp3', original_file_name)
        os.rename(os.path.join(output_folder, original_file_name), os.path.join(output_folder, new_file_name))
        print(f"Downloaded {url}")
    except Exception as e:
        raise Exception(f"Error while downloading {url}") from e

def worker(output_folder):
    """
    Worker function to download MP3 files
    
    Args:
        output_folder (str): Output folder to save MP3 files
    """
    while True:
        # Get the next URL from the queue
        url = url_queue.get()

        # Download the MP3 file
        try:
            download_mp3(url, output_folder)
        except Exception as e:
            print(f"Error while downloading {url}: {e}")

        # Mark the task as done
        url_queue.task_done()

def main():
    playlist = Playlist(args.playlist_link)
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
    os.makedirs(args.output_folder, exist_ok=True)

    # Create worker threads to download MP3 files
    num_workers = 4
    for i in range(num_workers):
        t = threading.Thread(target=worker, args=(args.output_folder,))
        t.daemon = True
        t.start()

    # Add each URL to the queue
    for url in playlist.video_urls:
        url_queue.put(url)

    # Wait for all URLs to be processed
    url_queue.join()

if __name__ == '__main__':
    main()
    