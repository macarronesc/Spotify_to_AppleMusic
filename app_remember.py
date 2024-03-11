import datetime
import send_telegram_message
import asyncio

# If this week has the day number 1 or 15, the playlist is old.
# This is due a limitation of the Apple Music API, that doesn't allow to know the creation date of a playlist.
# If it is old, ask to the user to delete it, API not allow edit name, put it in folders or delete it.
def check_playlist_age():
    today = datetime.datetime.now()
    start_week = today - datetime.timedelta(days=today.weekday())
    end_week = start_week + datetime.timedelta(days=6)
    
    if any(day.day == 1 or day.day == 15 for day in [start_week + datetime.timedelta(days=i) for i in range(7)]):
        return True
    else:
        return False

async def main():
    if check_playlist_age():
        message = 'Playlists are old, delete them.'
        print(message)
        await send_telegram_message.send_to_telegram(message)

# Run the main function
if __name__ == '__main__':
    asyncio.run(main())