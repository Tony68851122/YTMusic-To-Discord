from pypresence import Presence
from pypresence.types import ActivityType, StatusDisplayType
from ytmusicapi import YTMusic
from time import sleep, time
import os

# Initialize YTMusic with browser.json
browser_file = 'browser.json'
if os.path.exists(browser_file):
    yt = YTMusic(browser_file)
    print(f"✓ YTMusic initialized with {browser_file}")
else:
    print(f"✗ {browser_file} not found")
    exit()

# Initialize Discord RPC
RPC = Presence(1448110214607011890)
RPC.connect()
print("✓ Discord RPC connected")

# Track song state for time bar
last_track_id = None
song_start_time = None
last_update_time = 0

# List of artists/podcasters where we should shorten the title
SHORTEN_TITLE_FOR = [
    "Sinister",  # Add podcast names/artists that have long titles
    "another_podcast",
]

def is_podcast_artist(artist_name):
    """Check if artist is in the podcast list"""
    if not artist_name:
        return False
    return any(podcast.lower() in artist_name.lower() for podcast in SHORTEN_TITLE_FOR)

def check_song_changed():
    """Check if current song is different from last tracked song"""
    try:
        history = yt.get_history()
        if history and len(history) > 0:
            current_vid = history[0].get('videoId') or history[0].get('video_id')
            return current_vid != last_track_id
    except:
        pass
    return False

def update_discord():
    global last_track_id, song_start_time, last_update_time
    try:
        # Get now playing from history
        history = yt.get_history()
        if history and len(history) > 0:
            track = history[0]
            title = track.get('title', 'Unknown')
            artist = ''
            vid = track.get('videoId') or track.get('video_id')
            image_url = track.get('thumbnails', [{}])[-1].get('url', 'ytmusic_logo')

            # Check if song changed
            if vid != last_track_id:
                last_track_id = vid
                song_start_time = int(time())
            
            # Get duration (convert from MM:SS if needed)
            duration_sec = 0
            if 'duration' in track and track['duration']:
                try:
                    if isinstance(track['duration'], int):
                        duration_sec = track['duration']
                    elif isinstance(track['duration'], str):
                        parts = track['duration'].split(':')
                        if len(parts) == 2:
                            duration_sec = int(parts[0]) * 60 + int(parts[1])
                except:
                    duration_sec = 0
            
            # Cap duration for podcasts (max 3 hours = 10800 seconds)
            if duration_sec > 10800:
                duration_sec = 10800
            
            if 'artists' in track and track['artists']:
                artists_list = []
                for artist_info in track['artists']:
                    if isinstance(artist_info, dict) and 'name' in artist_info:
                        name = artist_info['name']
                    elif isinstance(artist_info, str):
                        name = artist_info
                    else:
                        continue
                    
                    # Filter out date-like strings (MM/DD/YYYY or similar patterns)
                    import re
                    if not re.match(r'^\d{1,2}/\d{1,2}/\d{4}', name) and not re.match(r'^\d{4}', name):
                        artists_list.append(name)
                
                artist = ', '.join(artists_list) if artists_list else track.get('artists', [{}])[0].get('name', 'Unknown') if isinstance(track.get('artists', [{}])[0], dict) else str(track.get('artists', ['Unknown'])[0])

            
            # Shorten title if artist is a podcast
            display_title = title
            if is_podcast_artist(artist):
                # Shorten to first 50 chars
                display_title = title[:50] + "..." if len(title) > 50 else title
            
            # Build button with YouTube Music link
            buttons = []
            if vid:
                yt_music_url = f"https://music.youtube.com/watch?v={vid}"
                buttons.append({"label": "Listen on YouTube Music", "url": yt_music_url})
            
            # Calculate timestamps in milliseconds for Discord time bar
            kwargs = {
                'status_display_type': StatusDisplayType.DETAILS,
                'activity_type': ActivityType.LISTENING,
                'details': f"Listening to {display_title[:127]}",
                "state": f"by {artist[:127]}",
                'large_image': "embedded_cover",
                'small_image': image_url,
                'buttons': buttons if buttons else None
            }
            
            # Add time bar if duration is available (without resetting)
            if duration_sec > 0 and song_start_time:
                end_time = song_start_time + duration_sec
                kwargs['start'] = song_start_time
                kwargs['end'] = end_time
                elapsed = int(time()) - song_start_time
                print(f"Duration: {duration_sec}s | Elapsed: {elapsed}s | Time bar: {song_start_time} → {end_time}")
            
            RPC.update(**kwargs)
            print(f"Updated Discord: {title} - {artist}")
            last_update_time = int(time())
    except Exception as e:
        print(f"Error updating Discord: {e}")

# Initial update
update_discord()

# Keep updating - check every 2 seconds for song changes, update Discord when needed
try:
    while True:
        sleep(2)
        
        # Check if song changed
        if check_song_changed():
            os.system('cls' if os.name == 'nt' else 'clear')
            print("🎵 Song changed detected!")
            update_discord()
        # Also do a full update every 15 seconds as fallback
        elif int(time()) - last_update_time >= 15:
            last_update_time = int(time())
            os.system('cls' if os.name == 'nt' else 'clear')
            update_discord()
except KeyboardInterrupt:
    print("\n✓ Stopping Discord RPC...")
    RPC.close()
    print("✓ RPC closed")
except Exception as e:
    print(f"Error: {e}")
    RPC.close()