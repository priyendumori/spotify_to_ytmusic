import spotipy
import spotipy.util as util
import json

clientId = "<client-id-of-registered-app>"
clientSecret = "<client-secret-of-registered-app>"
redirectUri = "<redirectUri-of-registered-app>"

def writeLikedSongsToFile():
    scope = 'user-library-read'
    username = 'set your name' 

    token = util.prompt_for_user_token(username,
                                    scope,
                                    client_id=clientId,
                                    client_secret=clientSecret,
                                    redirect_uri=redirectUri)

    liked_songs = []
    i=0
    while True:
        sp = spotipy.Spotify(auth=token)
        results = sp.current_user_saved_tracks(offset=i, limit=50)
        print(len(results['items']))
        if (len(results['items']) > 0):
            for idx, item in enumerate(results['items']):
                track = item['track']
                print(idx, track['album']['name'], " - ", track['artists'][0]['name'], " – ", track['name'], " - ", track['duration_ms'])
                trackArtists = []
                
                for artist in track['artists']:
                    trackArtists.append(artist['name'])
                trackArtists.sort()

                song = {
                    "name": track['name'],
                    "duration": track['duration_ms'],
                    "album": track['album']['name'],
                    "artists": trackArtists
                }

                liked_songs.append(song)
            
            i+=50
        else:
            print("No more songs to fetch")
            break

    # Writing to sample.json
    with open("spotify_liked.json", "w") as outfile:
        outfile.write(json.dumps(liked_songs, indent=4))

def writeLikedAlbumsToFile():
    scope = 'user-library-read'
    username = 'set your name' 

    token = util.prompt_for_user_token(username,
                                    scope,
                                    client_id=clientId,
                                    client_secret=clientSecret,
                                    redirect_uri=redirectUri)
    liked_albums = []
    i=0
    while True:
        sp = spotipy.Spotify(auth=token)
        results = sp.current_user_saved_albums(offset=i, limit=50)
        print(len(results['items']))
        if (len(results['items']) > 0):
            for idx, item in enumerate(results['items']):
                album = item['album']
                print(idx, album['name'], " - ", album['total_tracks'])
                albumArtists = []
                
                for artist in album['artists']:
                    albumArtists.append(artist['name'])
                albumArtists.sort()

                album = {
                    "name": album['name'],
                    "total_tracks": album['total_tracks'],
                    "artists": albumArtists
                }

                liked_albums.append(album)
            
            i+=50
        else:
            print("No more songs to fetch")
            break

    # Writing to sample.json
    with open("spotify_liked_albums.json", "w") as outfile:
        outfile.write(json.dumps(liked_albums, indent=4))

def writeLikedArtistsToFile():
    scope = 'user-follow-read'
    username = 'set your name' 

    token = util.prompt_for_user_token(username,
                                    scope,
                                    client_id=clientId,
                                    client_secret=clientSecret,
                                    redirect_uri=redirectUri)

    liked_artists = []
    after = None
    while True:
        sp = spotipy.Spotify(auth=token)
        results = sp.current_user_followed_artists(after=after)
        #print(results)
        print(len(results['artists']['items']))
        if (len(results['artists']['items']) > 0):
            for idx, item in enumerate(results['artists']['items']):
                artist = item['name']
                print(idx, artist)
                artist_json = {
                    "name": artist
                }

                liked_artists.append(artist_json)
            print(results['artists']['cursors']['after'])
            after = results['artists']['cursors']['after']
            if (after == None):
                break
            
        else:
            print("No more artists to fetch")
            break

    # Writing to sample.json
    with open("spotify_liked_artists.json", "w") as outfile:
        outfile.write(json.dumps(liked_artists, indent=4))

def writeUserPlaylistsToFile():
    scope = 'playlist-read-collaborative'
    username = 'set your name' 

    token = util.prompt_for_user_token(username,
                                    scope,
                                    client_id=clientId,
                                    client_secret=clientSecret,
                                    redirect_uri=redirectUri)

    liked_playlists = []
    i=0
    while True:
        sp = spotipy.Spotify(auth=token)
        results = sp.current_user_playlists(limit=50, offset=i)
        print(len(results['items']))
        if (len(results['items']) > 0):
            for idx, item in enumerate(results['items']):
                print(idx, item['name'], " - ", item['id'], " - ", item['owner']['display_name'], " - ", item['description'])
                add_to_list = input("Would you like to add this playlist to the list? (yes/no): ")
                if add_to_list.lower() == "y":
                    playlist = {
                        "name": item['name'],
                        "id": item['id'],
                        "owner": item['owner']['display_name'],
                        "description": item['description']
                    }
                    liked_playlists.append(playlist)
            i += 50
        else:
            break

    with open("spotify_playlists.json", "w") as outfile:
        outfile.write(json.dumps(liked_playlists, indent=4))

def writeUserPlayListsWithTrackInfoToFile():
    scope = 'playlist-read-collaborative'
    username = 'set your name' 

    token = util.prompt_for_user_token(username,
                                    scope,
                                    client_id=clientId,
                                    client_secret=clientSecret,
                                    redirect_uri=redirectUri)

    playlistsWithTracks = []
    with open('spotify_playlists.json', 'r') as openfile:
        # Reading from json file
        json_object = json.load(openfile)
        
        for playlist in json_object:
            i=0
            tracks = []
            while True:
                sp = spotipy.Spotify(auth=token)
                results = sp.playlist_tracks(playlist['id'],limit=50, offset=i)

                if (len(results['items']) <= 0):
                    break
    
                for idx, item in enumerate(results['items']):
                    print(item['track']['name'])
                    print(item['track']['artists'][0]['name'])

                    trackArtists = []
                        
                    for artist in item['track']['artists']:
                        trackArtists.append(artist['name'])
                    trackArtists.sort()
                    print(trackArtists)
                    track = {
                        "name": item['track']['name'],
                        "album": item['track']['album']['name'],
                        "artists": trackArtists
                    }
                    tracks.append(track)
                i += 50
            
            playlistWithTracks = {
                "name": playlist['name'],
                "id": playlist['id'],
                "owner": playlist['owner'],
                "description": playlist['description'],
                "tracks": tracks 
            }
            playlistsWithTracks.append(playlistWithTracks)

    with open("spotify_playlistsWithTracks.json", "w") as outfile:
        outfile.write(json.dumps(playlistsWithTracks, indent=4))

writeLikedSongsToFile()
