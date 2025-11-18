#!/usr/bin/env python3

import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Set environment variables SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET before running the script
client_id = os.environ.get('SPOTIFY_CLIENT_ID')
client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')

if not client_id or not client_secret:
    raise ValueError("SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET environment variables must be set")

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
))

# Set environment variable ARTIST_ID to the artist ID from Spotify (e.g., '06HL4z0CvFAxyc27GXpf02' for Taylor Swift)
artist_id = os.environ.get('ARTIST_ID')
if not artist_id:
    raise ValueError("ARTIST_ID environment variable must be set")
artist = sp.artist(f'spotify:artist:{artist_id}')
