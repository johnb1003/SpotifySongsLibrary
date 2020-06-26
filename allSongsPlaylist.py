import sys
import spotipy
from spotipy import SpotifyOAuth
import spotipy.util as util
import os
import time

# HIGH LEVEL DESIGN
# Loop through all playlists and add all songs from every playlist to allSongsDict

# Sort allSongsDict by song title
# sortedSongs = sorted(allSongsDict, key=allSongsDict.get)

# If "All" playlist doesn't exist create it
# ** user_playlist_create(user, name, public=True, description='') **

# Replace whole playlist with new (alphabetically) sorted allSongsDict
# ** sp.user_playlist_replace_tracks(user, playlist_id, tracks) ** (100 song limit) 

# Add all remaining songs from allSongsDict
# ** user_playlist_add_tracks(user, playlist_id, tracks, position=None) ** (100 song limit)

def main():

    # Dictionary of all songs from all playlists {song['id']: song['name']}
    allSongsDict = {}

    trackList = []

    USERNAME = os.environ.get('SPOTIFY_USER_JOHN')
    CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
    CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
    REDIRECT_URI = 'https://localhost:8080/'
    SCOPE = 'user-library-read,playlist-modify-private,user-read-private,playlist-modify-public,user-read-currently-playing'

    playlistID = None


    # Connect to Spotify API with credentials declared above
    auth = SpotifyOAuth(username=USERNAME, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=SCOPE)
    sp = spotipy.Spotify(auth_manager=auth)

    while(True):
        print("Booting up to refresh 'All' playlist")

        # Get all playlists info and insert into playlists
        playlistResults = sp.user_playlists(USERNAME, limit=50)
        playlists = playlistResults['items']
        while playlistResults['next']:
            playlistResults = sp.next(playlistResults)
            playlists.extend(playlistResults['items'])
        
        print("Retrieving songs from all user playlists")
        for playlist in playlists:
            if(playlist['name'] == 'All'): 
                playlistID = playlist['id']
            
            # Get all songs info from each playlist and insert into trackList
            trackResults = sp.user_playlist_tracks(USERNAME, playlist['id'])
            trackList.extend(trackResults['items'])
            for track in trackResults['items']:
                if(track['track']['id'] is not None and track['track']['name'] is not None):
                    allSongsDict[track['track']['id'].replace("'", '') ] = track['track']['name'].lower().replace("'", '')

            while trackResults['next']:
                trackResults = sp.next(trackResults)
                trackList.extend(trackResults['items'])
                for track in trackResults['items']:
                    if(track['track']['id'] is not None and track['track']['name'] is not None):  
                        allSongsDict[track['track']['id'].replace("'", '')] = track['track']['name'].lower().replace("'", '')

        # Check if 'All' playlist is currently in use so that refresh does not disturb user
        result = sp.current_user_playing_track()
        if(result is not None and (('context' in result) and ('href' in result['context']) and (type(result['context']['href']) == str) and (playlistID is not None) and (playlistID in result['context']['href']))):
            print("Cannot refresh, \'All\' playlist is currently in use. Sleeping for 1 hour...")
            print()
            time.sleep(3600)
            continue

        # Sort songs alphabetically
        sortedSongs = sorted(allSongsDict, key=allSongsDict.get)

        # Create 'All' playlist if it doesn't exist
        if(playlistID == None):
            playlistID = sp.user_playlist_create(user=USERNAME, name='All', public=True)['id']

        # Replace all songs from 'All' playlist with an empty list (Clear the playlist)
        sp.user_playlist_replace_tracks(USERNAME, playlistID, [])

        
        print("Adding songs to 'All' playist ...")

        # Add all songs from allSongsDict to 'All' playlist
        # allSongs = list(sortedSongs.keys())
        allSongs = sortedSongs
        tracks = []
        i = 100
        while(i < len(allSongs)):
            tracks = allSongs[i-100:i]
            sp.user_playlist_add_tracks(USERNAME, playlistID, tracks)
            i += 100
            # print("100 songs added")
            time.sleep(1)

        if(len(allSongs) % i != 0):
            tracks = allSongs[(i-100):]
            sp.user_playlist_add_tracks(USERNAME, playlistID, tracks)
            # print("%d songs added" % (len(allSongs) % 100))

        print("Finished sorting and adding songs. Sleeping for 1 hour...")
        print()
        time.sleep(3600)            # Wait for 1 hour before running again

main()



