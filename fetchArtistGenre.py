import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Set environment variables SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET before running the script
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.environ.get('SPOTIFY_CLIENT_ID'),
    client_secret=os.environ.get('SPOTIFY_CLIENT_SECRET')
))

# Set environment variable ARTIST_ID to the artist ID from Spotify
artist = sp.artist('spotify:artist:ARTIST_ID')
print(artist['name'], artist['genres'])
