import json
from ytmusicapi import YTMusic
ytmusic = YTMusic("oauth.json")

def searchAndLikeSongsOnYTMusic():
    with open('spotify_liked.json', 'r') as openfile:
        # Reading from json file
        json_object = json.load(openfile)
        
        for song in json_object:
            query = song['name']+" "+song['album']+" "
            for artist in song['artists']:
                query += artist
                query += " "
            print("query: " + query)

            if len(query)>0:
                ytSearch = ytmusic.search(query, filter="songs", limit=1)
                
                for song in ytSearch:
                    try:
                        print("title :" + song['title'])
                        print("album :" + song['album']['name'])
                        artists = ""
                        for artist in song['artists']:
                            artists += artist['name']
                            artists += ", "

                        print("artists :" + artists)
                    except Exception:
                        print("can't print")

                    print("videoId : " + song['videoId'])
                    # for key, value in song.items():
                    #     print(f'{key}: {value}')
                    ytmusic.rate_song(videoId=song['videoId'], rating='LIKE')
                    print("Liked this song")
                    print("------------------")
                    break
                    #print(song['title'] + " - " + song['views'])


def searchAndLikeAlbumsOnYTMusic():
    with open('spotify_liked_albums.json', 'r') as openfile:
        # Reading from json file
        json_object = json.load(openfile)
        
        for album in json_object:
            query = album['name']+" "
            #for artist in album['artists']:
            #    query += artist
            #    query += " "
            print("query: " + query)

            if len(query)>0:
                ytSearch = ytmusic.search(query, filter="albums", limit=1)
                
                for album in ytSearch:
                    #print(album)
                #if len(song['artists'])>0 and song['artists'][0]['name'] == "Linkin Park":
                    try:
                        print("title :" + album['title'])
                        artists = ""
                        for artist in album['artists']:
                            artists += artist['name']
                            artists += ", "

                        print("artists :" + artists)
                    except Exception:
                        print("can't print")

                    print("type : " + album['type'])
                    print("browseId : " + album['browseId'])
                    albumFromBrowseId = ytmusic.get_album(browseId=album['browseId'])
                    print(albumFromBrowseId['audioPlaylistId'])
                    #print("playlistId : " + album['playlistId'])
                    # for key, value in song.items():
                    #     print(f'{key}: {value}')
                    if album['type'].lower() == "single":
                        print("This is a single, not an album, so not liking")
                    else:
                        result = ytmusic.rate_playlist(playlistId=albumFromBrowseId['audioPlaylistId'], rating='LIKE')
                        #print(result)
                        print("Liked this album")
                    
                    print("------------------")
                    break
                    #print(song['title'] + " - " + song['views'])

def searchAndLikeArtistsOnYTMusic():
    with open('spotify_liked_artists.json', 'r') as openfile:
        # Reading from json file
        json_object = json.load(openfile)
        
        for artist in json_object:
            query = artist['name']+" "
            print("query: " + query)

            if len(query)>0:
                ytSearch = ytmusic.search(query, filter="artists", limit=1)
                
                for artist in ytSearch:
                    #print(artist)
                    print(artist['artist'])
                    print("browseId : " + artist['browseId'])
                    artistFromBrowseId = ytmusic.get_artist(artist['browseId'])
                    #print(artistFromBrowseId)
                    print(artistFromBrowseId['channelId'])
                    
                    result = ytmusic.subscribe_artists([artistFromBrowseId['channelId']])
                    #print(result)
                    print("Subscribed this artist")
                
                    print("------------------")
                    break
                    #print(song['title'] + " - " + song['views'])

def copyPlayliststoYTMusic():
    with open('spotify_playlistsWithTracks.json', 'r') as openfile:
        # Reading from json file
        json_object = json.load(openfile)
        
        for playlist in json_object:
            playlistName = playlist['name']
            ytPlaylistId = ytmusic.create_playlist(playlistName, "This playlist was copied from Spotify")
            print("Created playlist: " + playlistName + " with id: " + ytPlaylistId)
            tracks = playlist['tracks']
            videoIdsToAdd = []
            for track in tracks:
                query = track['name']+" "+track['album']+" "
                for artist in track['artists']:
                    query += artist
                    query += " "
                print("query: " + query)

                if len(query)>0:
                    ytSearch = ytmusic.search(query, filter="songs", limit=1)
                    
                    for song in ytSearch:
                        print("adding videoId: " + song['videoId'] + " " + song['title'])
                        videoIdsToAdd.append(song['videoId'])
                        break

            res = ytmusic.add_playlist_items(playlistId=ytPlaylistId, videoIds=videoIdsToAdd, duplicates=True)
            print(res)
            print("-----------------------------------------------------")


print("Calling searchAndLikeSongsOnYTMusic()")
searchAndLikeSongsOnYTMusic()
print("Finished searchAndLikeSongsOnYTMusic()")
print("------------------")

print("Calling searchAndLikeAlbumsOnYTMusic()")
searchAndLikeAlbumsOnYTMusic()
print("Finished searchAndLikeAlbumsOnYTMusic()")
print("------------------")

print("Calling searchAndLikeArtistsOnYTMusic()")
searchAndLikeArtistsOnYTMusic()
print("Finished searchAndLikeArtistsOnYTMusic()")
print("------------------")

print("Calling copyPlayliststoYTMusic()")
copyPlayliststoYTMusic()
print("Finished copyPlayliststoYTMusic()")
print("------------------")