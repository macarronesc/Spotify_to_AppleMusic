import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import csv
import os

# Set up Spotify Web API credentials
SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_track_details(playlist_url):
    # Get playlist id from url
    playlist_id = playlist_url.split('/')[-1]
    # Get playlist data
    playlist = sp.playlist(playlist_id)

    # Get playlist description
    playlist_description = playlist['description']

    # Extract track details
    tracks = []
    for item in playlist['tracks']['items']:
        track = item['track']
        song = track['name']
        album = track['album']['name']
        artist = track['artists'][0]['name']
        tracks.append((song, artist, album))
    return tracks, playlist_description

def create_csv_file(playlist_name, tracks):
    # Open CSV file in write mode
    with open(playlist_name + '.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        # Write headers
        writer.writerow(["Song", "Artist", "Album"])
        # Write tracks to CSV
        for track in tracks:
            writer.writerow(track)