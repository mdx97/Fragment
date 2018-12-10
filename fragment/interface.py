from fragment import wrapper, util
import sys
import math
import random

def run_cli():
    w = wrapper.SpotifyWrapper()
    w.create_playlist()

    # Get the playlist names that will be a part of the session.
    util.wrap_with_seperators(" Please enter the playlists you wish to be a part of this session.\n to finish entering playlists, press Enter.")
    playlists = []

    while (1):
        playlist = input(" ")
        if playlist == "":
            break
        playlists.append(playlist)

    playlist_count = len(playlists)

    # Get the total number of songs for this session.
    util.print_seperator()
    song_count = input(" Number of songs for this session: ")

    # Get the percentage each playlist will represent.
    util.wrap_with_seperators(" Assign a percentage to each playlist.")
    percentages = [0 for x in range(playlist_count)]

    for i in range(playlist_count):
        percentages[i] = int(input(" {}: ".format(playlists[i])))

    if (sum(percentages) != 100):
        util.print_seperator()
        print(" Error: your sum of percentages does not add up to 100.")
        sys.exit(1)
        
    # Calculate the number of songs per playlist.
    songs_per = [0 for x in range(playlist_count)]
    for i in range(playlist_count):
        songs_per[i] = math.floor(float(song_count) * (percentages[i] / 100))

    # Get the Spotify playlist ids of the chosen playlists.
    spotify_playlists = w.get_playlists()
    playlist_ids = ["0" for x in range(playlist_count)]

    for i in range(playlist_count):
        for j in range(len(spotify_playlists)):
            if playlists[i].lower() == spotify_playlists[j]["name"].lower():
                playlist_ids[i] = spotify_playlists[j]["id"]

    # Add random songs from each playlist into fragment-auto.
    session_track_uris = []

    for i in range(playlist_count):
        id = playlist_ids[i]
        if id == "0":
            print("No playlist id found for '{}'!".format(playlists[i]))
            continue
        tracks = w.get_playlist_tracks(id)
        for j in range(songs_per[i]):
            if len(tracks) > 1:
                random_index = random.randint(0, len(tracks) - 1)
                session_track_uris.append(tracks[random_index]["track"]["uri"])
                del tracks[random_index]

    for track_uri in session_track_uris:
        w.add_track(track_uri)

    w.play_playlist()