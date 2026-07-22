#!/usr/bin/env python3
#
# Usage:
#   export SPOTIFY_CLIENT_ID=<your_client_id>
#   export SPOTIFY_CLIENT_SECRET=<your_client_secret>
#   python3 fetch_artist_genre.py <spotify_artist_url>
#
# Example:
#   python3 fetch_artist_genre.py "https://open.spotify.com/artist/0YSaA3PB82JjyHSPq30lO3?si=abc123"

import os
import sys
import subprocess
from pathlib import Path

VENV_DIR = Path.home() / ".venvs" / "scripts"
VENV_PYTHON = VENV_DIR / "bin" / "python3"

# If not running inside the venv, set it up and re-launch
if Path(sys.executable).resolve() != VENV_PYTHON.resolve():
    if not VENV_PYTHON.exists():
        print("Setting up virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", str(VENV_DIR)], check=True)
        subprocess.run([str(VENV_PYTHON), "-m", "pip", "install", "spotipy"], check=True)
    os.execv(str(VENV_PYTHON), [str(VENV_PYTHON)] + sys.argv)

from urllib.parse import urlparse
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

if len(sys.argv) != 2:
    print("Usage: python3 fetch_artist_genre.py <spotify_artist_url>")
    sys.exit(1)

url = sys.argv[1]
path = urlparse(url).path  # /artist/0YSaA3PB82JjyHSPq30lO3
parts = path.strip("/").split("/")
if len(parts) != 2 or parts[0] != "artist":
    print("Error: URL must be a Spotify artist URL, e.g. https://open.spotify.com/artist/<id>")
    sys.exit(1)
artist_id = parts[1]

client_id = os.environ.get('SPOTIFY_CLIENT_ID')
client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')
if not client_id or not client_secret:
    raise ValueError("SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET environment variables must be set")

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
))

artist = sp.artist(f'spotify:artist:{artist_id}')
print(artist['name'], artist['genres'])
