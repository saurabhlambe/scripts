import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id='088effd1d43c44c1b859616babe82da6', client_secret='dab4db21446140489cbc75ab7ec7ed58'))
artist = sp.artist('spotify:artist:0ug84nvWi4PxvGIL52EZWr')
print(artist['name'], artist['genres'])
