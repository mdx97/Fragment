from wrapper import SpotifyWrapper
import math
import random

w = SpotifyWrapper()
w.authorize()
w.create_playlist()

# Get the playlist names that will be a part of the session.
print("-----------------------------------------")
print("* Please enter the playlists you wish to be a part of this session.")
print("* To complete entering playlists, type 'done'.")

playlists = []

while (1):
    playlist = input()
    if playlist == "done":
        break
    playlists.append(playlist)

playlist_count = len(playlists)

# Get the total number of songs for this session.
print("-----------------------------------------")
print("* Please enter the number of songs for this session.")

song_count = input()

# Get the percentage each playlist will represent.
print("-----------------------------------------")
print("* For each playlist, please assign a percentage to each.")

percentages = [0 for x in range(playlist_count)]
for i in range(playlist_count):
    percentages[i] = int(input("{}: ".format(playlists[i])))

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
    if id != "0":
        tracks = w.get_playlist_tracks(id)
        for j in range(songs_per[i]):
            random_index = random.randint(0, len(tracks) - 1)
            session_track_uris.append(tracks[random_index]["track"]["uri"])
            del tracks[random_index]

for track_uri in session_track_uris:
    w.add_track(track_uri)

