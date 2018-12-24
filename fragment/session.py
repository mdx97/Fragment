import sys
from fragment import util

class Session:
    def __init__(self):
        self.session_playlists = []
    
    def load_preset(self, name):
        return
    
    def save_preset(self, name):
        return


class SessionPlaylist:
    def __init__(self, name, frequency):
        self.name = name
        self.frequency = frequency
