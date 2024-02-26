![Spotify2AppleMusicBannerV2](https://github.com/therealmarius/Spotify-2-AppleMusic/assets/70507259/67dff9c5-49a6-494d-9594-92b2663540ef)

# Spotify to Apple Music
This application allows you to transfer your playlists from Spotify to Apple Music for **free** using Python, and also sends confirmation or error messages to a Telegram bot.

**The work of getting the songs and adding them to Apple Music is based on the general project of [@therealmarius](https://github.com/therealmarius/Spotify-2-AppleMusic).**

## Features

- Fetches the songs from the specified Spotify playlist using the Spotify API for developers and downloads them in a CSV file.
- Processes the CSV file and finds the corresponding songs on Apple Music using the public API. Then, adds them to the appropriate playlists.
- Sends the status of the transfer to a specific Telegram chat.

## Requirements

To use this application, you will need the following:

- A Spotify account and a Spotify free developer account.
- A Apple Music account and a web browser.
- A Telegram account and a Telegram bot.

## Usage

1. Install the requirements with `pip install -r requirements.txt`
2. Run the `app.py` script with the Spotify playlist ID as an argument. For example: `python app.py "<Spotify_playlist_link_1><Spotify_playlist_link_2>" "<name_playlist_1><name_playlist_2>"`.
3. Wait for the script to finish and check the Telegram chat for the confirmation or error message.
4. Enjoy your transferred playlist on Apple Music!

## How to get the Spotify and Apple Music credentials

### Spotify

To get the Spotify credentials, you need to sign up for the free [Spotify developers program](https://developer.spotify.com).

Then, you need to create an app and get the `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET`, which will be stored in the GitHub Secrets of the project.

### Apple Music

To get the Apple Music credentials, you need to do the following steps:

1. Open your web browser and go to the [Apple Music web player](https://music.apple.com). 
3. Open DevTools (**Ctrl + Shift + I or Cmd + Opt + I**) and go to the Network tab.
3. Log in to your Apple Music account. If you are already logged in, please log out and log in again.
4. Go back to the DevTools and look for a GET request to *https://buy.music.apple.com/account/web/info* (It seems like there are 2 requests to this URL; it should be the second one).
5. In the **Requests Headers**, copy the **Authorization**, the **Media-User-Token** and the **Cookies**.
6. Create differents variables and put their values on the GitHub Secrets `APPLE_MUSIC_TOKEN`, `APPLE_MUSIC_MEDIA_USER_TOKEN` and `APPLE_MUSIC_COOKIES`.

These credentials allow you to make multiple HTTP requests to the Apple Music server as if you were authenticated with your account, without the need of having an Apple developer account.

## Use of services

This program makes use of several APIs of already popular services to achieve its function successfully.

In addition, [GitHub Actions](https://docs.github.com/en/actions) is used to schedule this process at least once a week.

During this process, [GitHub Secrets](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions) is also used, which allows the private credentials for each of the services to be stored securely.

These private credentials are:

```
SPOTIFY_CLIENT_ID=<your Spotify client ID>
SPOTIFY_CLIENT_SECRET=<your Spotify client secret>
APPLE_MUSIC_COOKIES=<your Apple Music cookies>
APPLE_MUSIC_MEDIA_USER_TOKEN=<your Apple Music media user token>
APPLE_MUSIC_TOKEN=<your Apple Music authorization token>
TELEGRAM_CHAT_ID=<your Telegram chat ID>
TELEGRAM_TOKEN=<your Telegram bot token>
```


## Limitations

### Missing songs

The script to retrieve the Apple Music identifier for a Spotify song is quite basic. It simply compares the title, artist, and album name in many different combinations of search terms. The goal is to match an Apple Music song with your Spotify song and then get their iTunes identifier (it's the same as Apple Music identifiers). Some songs don't have the exact same title, artist, or album name (extraneous spacing, for example) in both services. This results in the script failing to retrieve an identifier for some songs. Hopefully, you'll be able to add the missing songs manually thanks to the noresult.txt file.
