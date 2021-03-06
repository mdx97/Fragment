import fragment.wrapper as wrapper
import sys
import os
import threading
import random
import time

class Controller:
    def __init__(self):
        self.playlist_settings = []
        self.running = True
        main_th = threading.Thread(target=self.main_loop)
        main_th.daemon = True
        main_th.start()
    
    def main_loop(self):
        segment_last_track = ""
        cached_playlists = []
        playlist_track_uri_cache = []

        while True:
            if not self.running:
                sys.exit(0)

            if wrapper.is_authorized():
                update_queue = False

                # Playlist settings have been updated and the loop needs to update the URI cache.
                if self.playlist_settings != cached_playlists:
                    update_queue = True
                    cached_playlists = list(self.playlist_settings)
                    playlist_track_uri_cache = [[] for x in range(len(cached_playlists))]
                    for idx, setting in enumerate(cached_playlists):
                        playlist_id = wrapper.get_playlist_id_by_name(setting.name)
                        playlist_track_uri_cache[idx] = wrapper.get_playlist_track_uris(playlist_id)

                # Force shuffle to always be disabled.
                wrapper.toggle_shuffle_off()
                
                # If the song queue is on the last track, the song queue should be updated.
                if segment_last_track == wrapper.get_current_track_uri():
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
                        wrapper.toggle_shuffle_off()
                        wrapper.play_tracks(tracks)

            time.sleep(5)

class PlaylistSetting:
    def __init__(self, name, frequency):
        self.name = name
        self.frequency = frequency
