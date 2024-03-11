import datetime
import send_telegram_message
import asyncio

# If this week has the day number 1 or 15, the playlist is old.
# This is due a limitation of the Apple Music API, that doesn't allow to know the creation date of a playlist.
# If it is old, ask to the user to delete it, API not allow edit name, put it in folders or delete it.
def check_playlist_age():
    today = datetime.now()
    if today.day == 1 or today.day == 15:
        return True
    else:
        return False

async def main():
    if check_playlist_age:
        message = 'Playlists are old, delete them.'
        print(message)
        await send_telegram_message.send_to_telegram(message)