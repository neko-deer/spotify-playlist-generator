import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

# Load configuration and song titles from JSON file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

client_id = config['client_id']
client_secret = config['client_secret']
redirect_uri = config['redirect_uri']
username = config['username']
song_titles = config['song_titles']

# Authenticate with Spotify
sp_oauth = SpotifyOAuth(client_id=client_id,
                        client_secret=client_secret,
                        redirect_uri=redirect_uri,
                        scope='playlist-modify-public')

def get_spotify_client():
    token_info = sp_oauth.get_cached_token()
    if not token_info:
        token_info = sp_oauth.get_access_token()
    if token_info:
        token = token_info['access_token']
        return spotipy.Spotify(auth=token)
    else:
        print("No valid token available. Please check your authentication setup.")
        return None

sp = get_spotify_client()

if sp:
    try:
        # Fetch the current user’s ID
        current_user = sp.current_user()
        user_id = current_user['id']

        # Playlist name and description
        playlist_name = 'Anime OPs Collection'
        playlist_description = 'A collection of anime opening themes.'

        # Create a new playlist for the current user
        playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True, description=playlist_description)
        playlist_id = playlist['id']

        # Search for each song and add it to the playlist
        for title in song_titles:
            try:
                results = sp.search(q=title, limit=1, type='track')
                if results['tracks']['items']:
                    track = results['tracks']['items'][0]
                    sp.playlist_add_items(playlist_id, [track['id']])
                    print(f"Added: {track['name']} by {track['artists'][0]['name']}")
                else:
                    print(f"Track not found: {title}")
            except spotipy.SpotifyException as e:
                print(f"Error searching for track '{title}': {e}")
                continue

        print(f"Playlist '{playlist_name}' created successfully!")

    except spotipy.SpotifyException as e:
        print(f"Spotify API error: {e}")
