import Spotify_playlist_to_CSV
import CSV_to_AppleMusic
import send_telegram_message
import asyncio
import time
import csv
import os
import sys

# Get argument with a playlists urls
if len(sys.argv) >= 3:
    playlists_urls = sys.argv[1]
    playlists_names = sys.argv[2]
else:
    playlists_urls = os.environ.get('SPOTIFY_PLAYLISTS_URLS') 
    playlists_names = os.environ.get('SPOTIFY_PLAYLISTS_NAMES') 

if not playlists_urls or not playlists_names:
    print('Error: Spotify playlist URLs or names were not provided.')
    sys.exit(1)

# Split the string to get a list
playlists_urls = playlists_urls.split(',')
playlists_names = playlists_names.split(',')

# Create empty lists
successful_playlists = []
failed_playlists = []
messages = []

# Define if file exist and is not empty
def file_is_not_empty(file_path):
    return os.path.isfile(file_path) and os.path.getsize(file_path) > 0

async def main():
    for playlist_name, playlist_url in zip(playlists_names, playlists_urls):
        # Print an advise
        print('Getting tracks from playlist:', playlist_name)

        try: 
            # Get tracks from playlist
            tracks, description = Spotify_playlist_to_CSV.get_track_details(playlist_url)

            # Create CSV file
            Spotify_playlist_to_CSV.create_csv_file(playlist_name, tracks)

            # Print an advise if exist csv
            if file_is_not_empty(playlist_name + '.csv') and tracks:
                print('Tracks saved to CSV file:', playlist_name + '.csv')
            else:
                print('No tracks saved to CSV file:', playlist_name + '.csv')

            # Create playlist and add songs to Apple Music
            CSV_to_AppleMusic.create_playlist_and_add_song(playlist_name + '.csv', description)
            
            # Print an advise
            print('Playlist created and songs added to Apple Music:', playlist_name)
            successful_playlists.append(playlist_name)

            time.sleep(5)
        except Exception as e:
            print('Error getting tracks from playlist:', playlist_name)
            print(e)
            failed_playlists.append(playlist_name)
            continue

        finally:
            print('')   

    # Create messages
    if successful_playlists:
        messages.append('Playlist updated to Apple Music: \n' + '\n'.join('* ' + playlist for playlist in successful_playlists))
    if failed_playlists:
        messages.append('Error with playlist: \n' + '\n'.join('* ' + playlist for playlist in failed_playlists))

    await send_telegram_message.send_to_telegram('\n\n'.join(messages))

# Run the main function
asyncio.run(main())