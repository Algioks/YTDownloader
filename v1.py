import argparse
import os
import requests
import json
from pytube import YouTube
from pytube.exceptions import VideoUnavailable, PytubeError
from googleapiclient.discovery import build
from pytube import YouTube
from pytube.exceptions import VideoUnavailable
from pytube.exceptions import PytubeError

# Load the config file
with open('config.json') as f:
    config = json.load(f)

# Get the developer key
developer_key = config.get('DEVELOPER_KEY')

def download_playlist(playlist_url, output_dir):
    # Parse the playlist ID from the URL
    playlist_id = playlist_url.split('list=')[1]

    # Set up the YouTube Data API client
    youtube = build('youtube', 'v3', developerKey=developer_key)

    # Get playlist items
    playlist_items = []
    next_page_token = None
    while True:
        request = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=500,
            pageToken=next_page_token
        )
        response = request.execute()
        playlist_items += response['items']
        next_page_token = response.get('nextPageToken')
        if next_page_token is None:
            break

    # Download each video as mp3
    for playlist_item in playlist_items:
        video_id = playlist_item['snippet']['resourceId']['videoId']
        try:
            # Validate URL
            youtube_url = f'https://www.youtube.com/watch?v={video_id}'
            if not YouTube.validate_url(youtube_url):
                print(f"Skipping video {video_id}: invalid YouTube URL")
                continue

            # Download audio
            youtube_video = YouTube(youtube_url)
            output_path = os.path.join(output_dir, f'{video_id}.mp3')
            print(f'Downloading audio for video {video_id}')
            youtube_audio = youtube_video.streams.filter(only_audio=True).first()
            youtube_audio.download(output_path)

        except (PytubeError, VideoUnavailable) as e:
            print(f"Skipping video: {video_id} due to error: {str(e)}")
            continue
    print(f'Download complete: {len(playlist_items)} videos downloaded.')

if __name__ == '__main__':
    # Parse the command-line arguments
    parser = argparse.ArgumentParser(description='Download a YouTube playlist')
    parser.add_argument('playlist_url', help='The URL of the playlist to download')
    parser.add_argument('output_dir', help='The name of the directory to save the audios in')
    args = parser.parse_args()

    try:
        download_playlist(args.playlist_url, args.output_dir)
    except Exception as e:
        print(f'Error: {str(e)}')