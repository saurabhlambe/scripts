#!/usr/bin/env python3
#
# Usage:
#   python3 fetch_artist_genre.py <spotify_or_bandcamp_url>
#
# Spotify requires credentials:
#   export SPOTIFY_CLIENT_ID=<your_client_id>
#   export SPOTIFY_CLIENT_SECRET=<your_client_secret>
#
# Examples:
#   python3 fetch_artist_genre.py "https://open.spotify.com/artist/0YSaA3PB82JjyHSPq30lO3?si=abc123"
#   python3 fetch_artist_genre.py "https://pipebombpa.bandcamp.com/album/hell-hole"

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

import urllib.request
from html.parser import HTMLParser
from urllib.parse import urlparse
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

if len(sys.argv) != 2:
    print("Usage: python3 fetch_artist_genre.py <spotify_or_bandcamp_url>")
    sys.exit(1)

url = sys.argv[1]
hostname = urlparse(url).hostname or ""


def fetch_spotify_genres(url):
    parts = urlparse(url).path.strip("/").split("/")
    if len(parts) != 2 or parts[0] != "artist":
        print("Error: Spotify URL must be an artist URL, e.g. https://open.spotify.com/artist/<id>")
        sys.exit(1)
    artist_id = parts[1]

    client_id = os.environ.get('SPOTIFY_CLIENT_ID')
    client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')
    if not client_id or not client_secret:
        print("Error: SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET environment variables must be set")
        sys.exit(1)

    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    ))
    artist = sp.artist(f'spotify:artist:{artist_id}')
    print(artist['name'], artist['genres'])


class BandcampTagParser(HTMLParser):
    LOCATION_TAGS = {
        "afghanistan", "albania", "algeria", "andorra", "angola", "argentina", "armenia", "australia",
        "austria", "azerbaijan", "bahrain", "bangladesh", "belarus", "belgium", "belize", "benin",
        "bhutan", "bolivia", "bosnia", "botswana", "brazil", "brunei", "bulgaria", "burkina faso",
        "burundi", "cambodia", "cameroon", "canada", "chad", "chile", "china", "colombia", "congo",
        "croatia", "cuba", "cyprus", "czechia", "denmark", "ecuador", "egypt", "estonia", "ethiopia",
        "finland", "france", "georgia", "germany", "ghana", "greece", "guatemala", "haiti", "honduras",
        "hungary", "iceland", "india", "indonesia", "iran", "iraq", "ireland", "israel", "italy",
        "jamaica", "japan", "jordan", "kazakhstan", "kenya", "kosovo", "kuwait", "kyrgyzstan", "laos",
        "latvia", "lebanon", "libya", "liechtenstein", "lithuania", "luxembourg", "madagascar", "malawi",
        "malaysia", "maldives", "mali", "malta", "mauritania", "mexico", "moldova", "monaco", "mongolia",
        "montenegro", "morocco", "mozambique", "myanmar", "namibia", "nepal", "netherlands",
        "new zealand", "nicaragua", "niger", "nigeria", "north korea", "norway", "oman", "pakistan",
        "panama", "paraguay", "peru", "philippines", "poland", "portugal", "qatar", "romania", "russia",
        "rwanda", "saudi arabia", "senegal", "serbia", "singapore", "slovakia", "slovenia", "somalia",
        "south africa", "south korea", "spain", "sri lanka", "sudan", "sweden", "switzerland", "syria",
        "taiwan", "tajikistan", "tanzania", "thailand", "togo", "tunisia", "turkey", "turkmenistan",
        "uganda", "ukraine", "united arab emirates", "united kingdom", "united states", "uruguay",
        "uzbekistan", "venezuela", "vietnam", "yemen", "zambia", "zimbabwe",
        # US states
        "alabama", "alaska", "arizona", "arkansas", "california", "colorado", "connecticut", "delaware",
        "florida", "georgia", "hawaii", "idaho", "illinois", "indiana", "iowa", "kansas", "kentucky",
        "louisiana", "maine", "maryland", "massachusetts", "michigan", "minnesota", "mississippi",
        "missouri", "montana", "nebraska", "nevada", "new hampshire", "new jersey", "new mexico",
        "new york", "north carolina", "north dakota", "ohio", "oklahoma", "oregon", "pennsylvania",
        "rhode island", "south carolina", "south dakota", "tennessee", "texas", "utah", "vermont",
        "virginia", "washington", "west virginia", "wisconsin", "wyoming",
        # Common cities
        "london", "new york", "los angeles", "chicago", "houston", "toronto", "montreal", "berlin",
        "paris", "tokyo", "sydney", "melbourne", "amsterdam", "barcelona", "madrid", "rome", "athens",
        "stockholm", "oslo", "copenhagen", "helsinki", "vienna", "zurich", "brussels", "dublin",
        "lisbon", "warsaw", "prague", "budapest", "bucharest", "sofia", "belgrade", "zagreb",
        "philadelphia", "boston", "seattle", "portland", "denver", "austin", "nashville", "atlanta",
        "miami", "minneapolis", "detroit", "cleveland", "pittsburgh", "baltimore", "phoenix",
        "san francisco", "san diego", "las vegas", "new orleans", "memphis", "richmond", "brooklyn",
        "queens", "manhattan", "bronx", "vancouver", "calgary", "edmonton", "ottawa", "winnipeg",
    }

    def __init__(self):
        super().__init__()
        self.in_tag = False
        self.genres = []
        self.all_tags = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a' and 'tag' in dict(attrs).get('class', ''):
            self.in_tag = True

    def handle_data(self, data):
        if self.in_tag:
            self.all_tags.append(data.strip())

    def handle_endtag(self, tag):
        if tag == 'a':
            self.in_tag = False

    def get_genres(self):
        return [t for t in self.all_tags if t.lower() not in self.LOCATION_TAGS]


def fetch_bandcamp_genres(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        html = urllib.request.urlopen(req).read().decode()
    except Exception as e:
        print(f"Error fetching Bandcamp page: {e}")
        sys.exit(1)

    parser = BandcampTagParser()
    parser.feed(html)
    genres = parser.get_genres()

    artist = urlparse(url).hostname.replace(".bandcamp.com", "")
    if not genres:
        print(f"{artist}: no genres found")
    else:
        print(f"{artist}", genres)


if hostname == "open.spotify.com":
    fetch_spotify_genres(url)
elif hostname.endswith(".bandcamp.com"):
    fetch_bandcamp_genres(url)
else:
    print("Error: URL must be a Spotify (open.spotify.com) or Bandcamp (*.bandcamp.com) URL")
    sys.exit(1)
