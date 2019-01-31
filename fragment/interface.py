from fragment.presets import *
from fragment.controller import Controller, PlaylistSetting
from fragment.strings import * 
import sys

class FragmentCLI:
    def __init__(self):
        self.controller = Controller()
    
    def main(self):
        self.authorize()
        while True:
            cmd = input(COMMAND_SYMBOL)
            print()

            if cmd == "set":
                self.settings()
            elif cmd == "viewset":
                self.print_settings()
            elif cmd == "saveset":
                self.save_settings()
            elif cmd == "help":
                print(HELP_STRING) 
            elif cmd == "exit":
                self.controller.running = False
                sys.exit(0)
            else:
                print(ERROR_INVALID_COMMAND)
    
    def authorize(self):
        credential_manager = self.controller.spotify_wrapper.credential_manager
        if credential_manager.is_authorized():
            return
        user = input(USERNAME_PROMPT)
        credential_manager.set_user(user)
        credential_manager.get_authorization_code()

        authorization_code = input(AUTHORIZATION_CODE_PROMPT)
        credential_manager.authorize(authorization_code)

    def print_settings(self):
        if len(self.controller.playlist_settings) > 0:
            print(SETTINGS_LABEL)
            for playlist in self.controller.playlist_settings:
                print(playlist_display(playlist.name, playlist.frequency))
        else:
            print(ERROR_NO_SETTINGS)

        print()
    
    def save_settings(self):
        preset_name = input(PRESET_PROMPT)
        if preset_exists(preset_name):
            override = input(OVERRIDE_PROMPT).lower()
            if override != YES_SYMBOL:
                print()
                return
        
        save_preset(preset_name, self.controller.playlist_settings)
        print(PRESET_SAVED)

    def settings(self):
        # First check if user wants to use a preset.
        do_preset = input(USE_PRESET_PROMPT)
        if do_preset == YES_SYMBOL:
            preset_name = input(PRESET_PROMPT)
            result = get_preset(preset_name)
            if not result:
                print(ERROR_PRESET_NOT_FOUND)
                return
            
            self.controller.playlist_settings = result
            print(PRESET_LOADED)
            return
        
        # Get the playlist names that will be a part of the session.
        print(PLAYLISTS_PROMPT)
        playlists = []

        while (1):
            playlist_name = input(COMMAND_SYMBOL)
            if not playlist_name:
                break
            playlists.append(PlaylistSetting(playlist_name, 0))

        print()
        playlist_count = len(playlists)

        if playlist_count == 0:
            print(ERROR_NO_PLAYLISTS_ENTERED)
            return

        # Get the percentage each playlist will represent.
        print(ASSIGN_FREQUENCY_PROMPT)
        freq_sum = 0

        for i in range(playlist_count):
            freq = int(input("{}: ".format(playlists[i].name)))
            playlists[i].frequency = freq
            freq_sum += freq

        print()

        if (freq_sum != 10):
            print(ERROR_INVALID_FREQUENCY_SUM)
            return

        self.controller.playlist_settings = playlists
        print(SETTINGS_CHANGED)
