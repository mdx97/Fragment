from wrapper import SpotifyWrapper
import math

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

# Get all playlists from Spotify.
spotify_playlists = w.get_playlists()
playlist_ids = ["0" for x in range(playlist_count)]

for i in range(playlist_count):
    for j in range(len(spotify_playlists)):
        if playlists[i].lower() == spotify_playlists[j]["name"].lower():
            playlist_ids[i] = spotify_playlists[j]["id"]

print(str(playlist_ids))
