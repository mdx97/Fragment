from fragment import wrapper
import sys
import os
import threading

class Session:
    def __init__(self):
        self.spotify_wrapper = wrapper.SpotifyWrapper()
        self.session_playlists = []
        self.init_preset_directory()
        self.running = True
        main_th = threading.Thread(target=self.session_loop)
        main_th.start()
        
    def session_loop(self):
        # TODO: Where the controlling of the song queue happens.
        while True:
            if not self.running:
                sys.exit(0)
            continue
    
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
