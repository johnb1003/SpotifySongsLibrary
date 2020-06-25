import sys
import spotipy
from spotipy import SpotifyOAuth
import spotipy.util as util
import os
import time


def main():

    # Dictionary of all songs from all playlists {song['id']: song['name']}
    allSongsDict = {}

    trackList = []

    USERNAME = os.environ.get('SPOTIFY_USER')
    CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
    CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
    REDIRECT_URI = 'http://localhost/'
    SCOPE = 'user-library-read,playlist-modify-private,user-read-private,playlist-modify-public,user-read-currently-playing'

    playlistID = '72L1ruRcxPEBWBbkC3pN17'


    # Connect to Spotify API with credentials declared above
    auth = SpotifyOAuth(username=USERNAME, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=SCOPE)
    sp = spotipy.Spotify(auth_manager=auth)

    result = sp.current_user_playing_track()
    if(result == None or (('context' in result) and ('href' in result['context']) and (type(result['context']['href']) == str) and (playlistID not in result['context']['href']))):
        print('You are on my playlist!')
    


main()