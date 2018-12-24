import sys
import os
from fragment import util

class Session:
    def __init__(self):
        self.session_playlists = []
        self.init_preset_directory()

    def init_preset_directory(self):
        if not os.path.isdir("presets"):
            os.makedirs("presets")

    def load_preset(self, name):
        if not self.preset_exists(name):
            return 1

        filename = self.get_preset_filename(name)
        lines = [line.rstrip("\n") for line in open(filename, "r")]
        
        for line in lines:
            values = line.split()
            name = values[0]
            freq = int(values[1])
            session_playlist = SessionPlaylist(name, freq)
            
        return 0
    
    def save_preset(self, name):
        filename = self.get_preset_filename(name)
        preset_file = open(filename, "w")

        for playlist in self.session_playlists:
            preset_file.write(playlist.name + " " + str(playlist.frequency))
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
