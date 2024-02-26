from sys import argv
import csv
import urllib.parse, urllib.request
import json
from time import sleep
import requests
import os

# Function to get contents of file if it exists
def get_connection_data(f,prompt):
    if os.path.exists(f):
        with open(f,'r') as file:
            return file.read().rstrip('\n')
    else:
            return input(prompt)

def create_apple_music_playlist(session, playlist_name, description):
    url = "https://amp-api.music.apple.com/v1/me/library/playlists"
    data = {
        'attributes': {
            'name': playlist_name,
            'description': description,
        }
    }
    # test if playlist exists and create it if not
    print(f"Checking if playlist {playlist_name} exists...")
    response = session.get(url)
    if response.status_code == 200:
        for playlist in response.json()['data']:
            if playlist['attributes']['name'] == playlist_name:
                print(f"Playlist {playlist_name} already exists!")
                return playlist['id']

    print(f"Playlist {playlist_name} doesn't exist, creating it...")
    response = session.post(url, json=data)

    if response.status_code == 201:
        sleep(1.5)
        return response.json()['data'][0]['id']
    else:
        raise Exception(f"Error {response.status_code} while creating playlist {playlist_name}!")
        return None

# Function to get the iTunes ID of a song
def get_itunes_id(title, artist, album):
    BASE_URL = "https://itunes.apple.com/search?country=ES&media=music&entity=song&limit=5&term="
    # Search the iTunes catalog for a song
    try:
        # Search for the title + artist + album
        url = BASE_URL + urllib.parse.quote(title + " " + artist + " " + album)
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        data = json.loads(response.read().decode('utf-8'))
        # If no result, search for the title + artist
        if data['resultCount'] == 0:
            url = BASE_URL + urllib.parse.quote(title + " " + artist)
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            data = json.loads(response.read().decode('utf-8'))
            # If no result, search for the title + album
            if data['resultCount'] == 0:
                url = BASE_URL + urllib.parse.quote(title + " " + album)
                request = urllib.request.Request(url)
                response = urllib.request.urlopen(request)
                data = json.loads(response.read().decode('utf-8'))
                # If no result, search for the title
                if data['resultCount'] == 0:
                    url = BASE_URL + urllib.parse.quote(title)
                    request = urllib.request.Request(url)
                    response = urllib.request.urlopen(request)
                    data = json.loads(response.read().decode('utf-8'))
    except:
        return print("An error occured with the request.")
    
    # Try to match the song with the results
    try:
        response = urllib.request.urlopen(request)
        data = json.loads(response.read().decode('utf-8'))
        
        for each in data['results']:
            #Trying to match with the exact track name, the artist name and the album name
            if each['trackName'].lower() == title.lower() and each['artistName'].lower() == artist.lower() and each['collectionName'].lower() == album.lower():
                return each['trackId']           
            #Trying to match with the exact track name and the artist name
            elif each['trackName'].lower() == title.lower() and each['artistName'].lower() == artist.lower():
                return each['trackId']
            #Trying to match with the exact track name and the album name
            elif each['trackName'].lower() == title.lower() and each['collectionName'].lower() == album.lower():
                return each['trackId']
            #Trying to match with the exact track name and the artist name, in the case artist name are different between Spotify and Apple Music
            elif each['trackName'].lower() == title.lower() and (each["artistName"].lower() in artist.lower() or artist.lower() in each["artistName"].lower()):
                return each['trackId']
            #Trying to match with the exact track name and the album name, in the case album name are different between Spotify and Apple Music
            elif each['trackName'].lower() == title.lower() and (each["collectionName"].lower() in album.lower() or album.lower() in each["collectionName"].lower()):
                return each['trackId']  
            #Trying to match with the exact track name
            elif each['trackName'].lower() == title.lower():
                return each['trackId']        
            #Trying to match with the track name, in the case track name are different between Spotify and Apple Music
            elif title.lower() in each['trackName'] or each['trackName'].lower() in title.lower():
                return each['trackId']
        try:
            #If no result, return the first result
            return data['results'][0]['trackId']
        except:
            #If no result, return None
            return None
    except:
        #The error is handled later in the code
        return None

# Function to add a song to a playlist
def add_song_to_playlist(session, song_id, playlist_id, playlist_name):
    try:   
        request = session.post(f"https://amp-api.music.apple.com/v1/me/library/playlists/{playlist_id}/tracks", json={"data":[{"id":f"{song_id}","type":"songs"}]})
        # Checking if the request is successful
        if requests.codes.ok:
            print(f"Song {song_id} added to playlist {playlist_name}!")
            return True
        # If not, print the error code
        else: 
            print(f"Error {request.status_code} while adding song {song_id} to playlist {playlist_name}!")
            return False
    except:
        print(f"HOST ERROR: Apple Music might have blocked the connection during the add of {song_id} to playlist {playlist_name}!\nPlease wait a few minutes and try again.\nIf the problem persists, please contact the developer.")
        return False

def get_playlist_track_ids(session, playlist_id):
    # test if song is already in playlist
    try:
        offset = 0
        limit = 100
        tracks = []

        while True:
            response = session.get(f"https://amp-api.music.apple.com/v1/me/library/playlists/{playlist_id}/tracks?limit={limit}&offset={offset}")
            if response.status_code == 200:
                data = response.json()['data']
                if not data:
                    break
                tracks.extend([track['attributes']['playParams']['catalogId'] for track in data])
                offset += limit
            elif response.status_code == 404:
                break
            else:
                raise Exception(f"Error {response.status_code} while getting playlist {playlist_id}!")
                return None

        return tracks
    except:
        raise Exception(f"Error while getting playlist {playlist_id}!")
        return None

# Opening session
def create_playlist_and_add_song(file, description):
    # Getting user's data for the connection
    token = os.environ.get('APPLE_MUSIC_TOKEN')
    cookies = os.environ.get('APPLE_MUSIC_COOKIES')
    media_user_token = os.environ.get('APPLE_MUSIC_MEDIA_USER_TOKEN')

    # Creating the session
    with requests.Session() as s:
        s.headers.update({"Authorization": f"{token}",
                    "media-user-token": f"{media_user_token}",
                    "Cookie": f"{cookies}".encode('utf-8'),
                    "Host": "amp-api.music.apple.com",
                    "Accept-Encoding":"gzip, deflate, br",
                    "Referer": "https://music.apple.com/",
                    "Origin": "https://music.apple.com",
                    "Content-Length": "45",
                    "Connection": "keep-alive",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-site",
                    "TE": "trailers"})
    
    # Getting the playlist name
    playlist_name = os.path.basename(file)
    playlist_name = playlist_name.split('.')
    playlist_name = playlist_name[0]
    playlist_name = playlist_name.replace('_', ' ')

    print(f"Apple Music session started")

    playlist_identifier = create_apple_music_playlist(s, playlist_name, description)

    playlist_track_ids = get_playlist_track_ids(s, playlist_identifier)

    print(f"Playlist {playlist_name} tracks retrieved!")

    # Opening the inputed CSV file
    with open(str(file), encoding='utf-8') as file:
        file = csv.reader(file)
        next(file)
        # Initializing variables for the stats
        n = 0
        converted = 0
        failed = 0
        # Looping through the CSV file
        for row in file:
            n += 1
            # Trying to get the iTunes ID of the song
            title, artist, album = row

            track_id = get_itunes_id(title, artist, album)
            # If the song is found, add it to the playlist
            if track_id:
                if str(track_id) in playlist_track_ids:
                    print(f'\nN°{n} | {title} | {artist} | {album} => {track_id}')
                    print(f"Song {track_id} already in playlist {playlist_name}!")
                    failed += 1
                    continue
                print(f'\nN°{n} | {title} | {artist} | {album} => {track_id}')
                sleep(1.5)

                if add_song_to_playlist(s, track_id, playlist_identifier, playlist_name):
                    converted += 1
                else:
                    failed += 1
            # If not, write it in a file
            else:
                print(f'N°{n} | {title} | {artist} | {album} => NOT FOUND')
                with open(f'{playlist_name}_noresult.txt', 'a+', encoding='utf-8') as f:
                    f.write(f'{title} | {artist} | {album} => NOT FOUND')
                    f.write('\n')
                failed += 1
    # Printing the stats report
    converted_percentage = round(converted / n * 100) if n > 0 else 100
    print(f'\n - STAT REPORT -\nPlaylist Songs: {n}\nConverted Songs: {converted}\nFailed Songs: {failed}\nPlaylist converted at {converted_percentage}%')