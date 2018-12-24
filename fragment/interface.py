from fragment import wrapper, util, session
import sys
import math
import random

class FragmentCLI:
    def __init__(self):
        self.spotify_wrapper = wrapper.SpotifyWrapper()
        self.session = session.Session()
        self.cli_loop()
    
    def cli_loop(self):
        while 1:
            cmd = input("> ")
            print()

            if cmd == "set":
                self.settings()
            elif cmd == "viewset":
                self.print_settings()
            elif cmd == "saveset":
                self.save_settings()
            elif cmd == "exit":
                self.session.running = False
                sys.exit(0)
            else:
                print("Error: invalid command '{}'.\n".format(cmd))
    
    def print_settings(self):
        if len(self.session.session_playlists) > 0:
            print("Playlist Settings")
            for playlist in self.session.session_playlists:
                print("* {} ({})".format(playlist.name, playlist.frequency))
        else:
            print("No playlist settings!")

        print()
    
    def save_settings(self):
        preset_name = input("Please enter a name for this preset: ")
        if self.session.preset_exists(preset_name):
            override = input("A playlist of this name already exists, do you wish to override (y/n)? ")
            if override != "y":
                print()
                return
        
        self.session.save_preset(preset_name)
        print("Preset '{}' successfully saved!\n".format(preset_name))

    def settings(self):
        # First check if user wants to use a preset.
        do_preset = input("Would you like to load settings from a preset (y/n)? ")
        if do_preset == "y":
            preset_name = input("Preset name: ")
            result = self.session.load_preset(preset_name)
            if result == 1:
                print("Error: preset named '{}' not found!\n".format(preset_name))
                return
            
            print("Successfully loaded preset '{}'!\n".format(preset_name))
            return
        
        # Get the playlist names that will be a part of the session.
        print("Please enter the playlists you wish to be a part of this session.\nTo finish entering playlists, press Enter.")
        playlists = []

        while (1):
            playlist_name = input("> ")
            if playlist_name == "":
                break
            playlists.append(session.SessionPlaylist(playlist_name, 0))

        print()
        playlist_count = len(playlists)

        if playlist_count == 0:
            print("You must enter at least one playlist!\n")
            return

        # Get the percentage each playlist will represent.
        print("Assign a frequency to each playlist (1-10).")
        freq_sum = 0

        for i in range(playlist_count):
            freq = int(input("{}: ".format(playlists[i].name)))
            playlists[i].frequency = freq
            freq_sum += freq

        print()

        if (freq_sum != 10):
            print("Error: your sum of frequencies does not add up to 10.\n")
            return

        self.session.session_playlists = playlists
        print("Session settings successfully changed!\n")
