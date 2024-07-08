import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import requests
import os
import hide_from_GIT

client_id, client_secret = hide_from_GIT.get_credentials()

credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
spotify = spotipy.Spotify(client_credentials_manager=credentials)

# Sample DataFrame with Spotify IDs (replace with your own DataFrame)
df = pd.read_csv('../static/SpotifyAudioFeaturesApril2019_scraped_selection.csv')
track_ids = df['track_id'].tolist()
print(track_ids)

# Function to download images
def download_image(url, path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(path, 'wb') as file:
            file.write(response.content)
    else:
        print(f"Failed to download image from {url}")

# Fetch album details from track IDs and download covers
for track_id in track_ids:
    track_info = spotify.track(track_id)
    album = track_info['album']  # Get the album data from the track info
    cover_url = album['images'][0]['url']  # Getting the URL of the cover image
    file_path = os.path.join('../static/album_covers', f"{track_id}.jpg")
    download_image(cover_url, file_path)

print("All album covers have been downloaded successfully.")
