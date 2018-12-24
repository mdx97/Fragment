from fragment import wrapper, util, session
import sys
import math
import random
from tkinter import *

class FragmentCLI:
    def __init__(self):
        self.spotify_wrapper = wrapper.SpotifyWrapper()
        self.session = session.Session()
        self.settings()

    def settings(self):
        # First check if user wants to use a preset.
        do_preset = input("Would you like to load settings from a preset (y/n)? ")
        if do_preset == "y":
            preset_name = input("Preset name: ")
            self.session.load_preset(preset_name)
            return
        
        # Get the playlist names that will be a part of the session.
        util.wrap_with_seperators("Please enter the playlists you wish to be a part of this session.\n to finish entering playlists, press Enter.")
        playlists = []

        while (1):
            playlist_name = input(" ")
            if playlist_name == "":
                break
            playlists.append(session.SessionPlaylist(playlist_name, 0))

        playlist_count = len(playlists)

        if playlist_count == 0:
            print("You must enter at least one playlist!")
            return

        # Get the percentage each playlist will represent.
        util.wrap_with_seperators("Assign a frequency to each playlist (1-10).")
        freq_sum = 0

        for i in range(playlist_count):
            freq = int(input(" {}: ".format(playlists[i].name)))
            playlists[i].frequency = freq
            freq_sum += freq

        if (freq_sum != 10):
            util.print_seperator()
            print("Error: your sum of frequencies does not add up to 10.")
            return

        self.session.session_playlists = playlists
        util.wrap_with_seperators("Session settings successfully changed!")
