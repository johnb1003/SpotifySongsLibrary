import sys
import spotipy
from spotipy import SpotifyOAuth
import spotipy.util as util
import xlrd
import os
import re
import time

SCOPE = 'user-library-read,playlist-modify-private,user-read-private,playlist-modify-public'
REDIRECT_URI = 'http://localhost/'


class Song:
    def __init__(self, title='', time=0, artist=[], album='', genre='', songID='', matchScore=0, playlists=[]):
        self.title = title
        self.time = time
        self.artist = artist
        self.album = album
        self.genre = genre
        self.songID = songID
        self.matchScore = matchScore
        self.returnedResults = 0
        self.playlists = playlists

# List of playlist IDs
playlistList = []

# Dictionary of all songs from all playlists {song['id']: song['name']}
allSongsDict = {}
# sortedSongs = sorted(allSongsDict, key=allSongsDict.get)

def main():
    USERNAME = os.environ.get('SPOTIFY_USER')
    CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
    CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')

    # Connect to Spotify API with credentials declared earlier
    #token = util.prompt_for_user_token(USERNAME, SCOPE,  client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI)

    auth = SpotifyOAuth(username=USERNAME, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=SCOPE)

    sp = spotipy.Spotify(auth_manager=auth)
    print(sp.me())
    print("Connected!") 

main()

words = ["John", "Jacob", "Carl", "90210"]

sortedWords = sorted(words, key=str.lower)

print (sortedWords)
print(sortedWords.index("John"))

