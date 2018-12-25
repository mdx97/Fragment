from fragment import wrapper
import sys
import os
import threading
import random
import time

class Session:
    def __init__(self):
        self.spotify_wrapper = wrapper.SpotifyWrapper()
        self.session_playlists = []
        self.init_preset_directory()
        self.running = True
        main_th = threading.Thread(target=self.session_loop)
        main_th.start()
    
    def session_loop(self):
        segment_last_track = ""
        cached_playlists = []
        playlist_track_uri_cache = []

        while True:
            if not self.running:
                sys.exit(0)

            update_queue = False

            # Playlist settings have been updated and the session loop needs to update the URI cache.
            if self.session_playlists != cached_playlists:
                update_queue = True
                cached_playlists = list(self.session_playlists)
                playlist_track_uri_cache = [[] for x in range(len(cached_playlists))]
                for idx, session_playlist in enumerate(cached_playlists):
                    playlist_id = self.spotify_wrapper.get_playlist_id_by_name(session_playlist.name)
                    playlist_track_uri_cache[idx] = self.spotify_wrapper.get_playlist_track_uris(playlist_id)

            # If the song queue is on the last track, the song queue should be updated.
            if segment_last_track == self.spotify_wrapper.get_current_track_uri():
                update_queue = True

            if update_queue:
                tracks = []
                for idx, sp in enumerate(cached_playlists):
                    for j in range(sp.frequency):
                        random_idx = random.randint(0, len(playlist_track_uri_cache[idx]) - 1)
                        random_track = playlist_track_uri_cache[idx][random_idx]
                        tracks.append(random_track)
                        del playlist_track_uri_cache[idx][random_idx]
                
                if tracks:
                    random.shuffle(tracks)
                    segment_last_track = tracks[-1]
                    self.spotify_wrapper.play_tracks(tracks)

            time.sleep(1)

    def init_preset_directory(self):
        if not os.path.isdir("presets"):
            os.makedirs("presets")

    def load_preset(self, name):
        if not self.preset_exists(name):
            return 1

        filename = self.get_preset_filename(name)
        lines = [line.rstrip("\n") for line in open(filename)]
        
        for line in lines:
            values = line.split(",")
            name = values[0]
            freq = int(values[1])
            session_playlist = SessionPlaylist(name, freq)
            self.session_playlists.append(session_playlist)

        return 0
    
    def save_preset(self, name):
        filename = self.get_preset_filename(name)
        preset_file = open(filename, "w")

        for playlist in self.session_playlists:
            preset_file.write(playlist.name + "," + str(playlist.frequency))
            preset_file.write("\n")

        preset_file.close()
    
    def preset_exists(self, name):
        return os.path.isfile(self.get_preset_filename(name))

    def get_preset_filename(self, name):
        return "presets/{}.preset".format(name)

class SessionPlaylist:
    def __init__(self, name, frequency):
        self.name = name
        self.frequency = frequency
