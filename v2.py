import os
import sys
import time
import requests
import argparse
from pytube import Playlist, YouTube
import re

# Set up command line arguments
parser = argparse.ArgumentParser(description='Download MP3 files from a YouTube playlist')
parser.add_argument('playlist_link', help='YouTube playlist link')
parser.add_argument('output_folder', help='Output folder to save MP3 files')
args = parser.parse_args()

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
    except Exception as e:
        raise Exception(f"Error while downloading {url}") from e

def main():
    playlist = Playlist(args.playlist_link)
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
    os.makedirs(args.output_folder, exist_ok=True)

    # Loop through all videos in playlist and download them as mp3
    for url in playlist.video_urls:
        try:
            download_mp3(url, args.output_folder)
            print(f"Downloaded {url}")
        except Exception as e:
            print(f"Error while downloading {url}: {e}")
    
if __name__ == '__main__':
    main()
