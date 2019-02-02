import fragment.controller as controller
import fragment.globals as gvars
import fragment.presets as presets
import fragment.strings as strings
import fragment.wrapper as wrapper
import sys

def cli_main():
    gvars.g_controller = controller.Controller() 
    authorize()
    while True:
        cmd = input(strings.COMMAND_SYMBOL)
        print()

        if cmd == "set":
            settings()
        elif cmd == "viewset":
            print_settings()
        elif cmd == "saveset":
            save_settings()
        elif cmd == "presets":
            print_presets()
        elif cmd == "help":
            print(strings.HELP_STRING) 
        elif cmd == "exit":
            gvars.g_controller.running = False
            sys.exit(0)
        else:
            print(strings.ERROR_INVALID_COMMAND)

def authorize():
    if wrapper.is_authorized():
        return
    user = input(strings.USERNAME_PROMPT)
    wrapper.set_user(user)
    wrapper.get_authorization_code()
    authorization_code = input(strings.AUTHORIZATION_CODE_PROMPT)
    wrapper.authorize(authorization_code)

def print_settings():
    if len(gvars.g_controller.playlist_settings) > 0:
        print(strings.SETTINGS_LABEL)
        for playlist in gvars.g_controller.playlist_settings:
            print(strings.playlist_display(playlist.name, playlist.frequency))
    else:
        print(strings.ERROR_NO_SETTINGS)
    print()

def save_settings():
    preset_name = input(strings.PRESET_PROMPT)
    if presets.preset_exists(preset_name):
        override = input(strings.OVERRIDE_PROMPT).lower()
        if override != strings.YES_SYMBOL:
            print()
            return
    
    presets.save_preset(preset_name, gvars.g_controller.playlist_settings)
    print(strings.PRESET_SAVED)

def settings():
    # First check if user wants to use a preset.
    do_preset = input(strings.USE_PRESET_PROMPT)
    if do_preset == strings.YES_SYMBOL:
        preset_name = input(strings.PRESET_PROMPT)
        result = presets.get_preset(preset_name)
        if not result:
            print(strings.ERROR_PRESET_NOT_FOUND)
            return
        
        gvars.g_controller.playlist_settings = result
        print(strings.PRESET_LOADED)
        return
    
    # Get the playlist names that will be a part of the session.
    print(strings.PLAYLISTS_PROMPT)
    playlists = []

    while (1):
        playlist_name = input(strings.COMMAND_SYMBOL)
        if not playlist_name:
            break
        playlists.append(PlaylistSetting(playlist_name, 0))

    print()
    playlist_count = len(playlists)

    if playlist_count == 0:
        print(strings.ERROR_NO_PLAYLISTS_ENTERED)
        return

    # Get the percentage each playlist will represent.
    print(strings.ASSIGN_FREQUENCY_PROMPT)
    freq_sum = 0

    for i in range(playlist_count):
        freq = int(input("{}: ".format(playlists[i].name)))
        playlists[i].frequency = freq
        freq_sum += freq

    print()

    if (freq_sum != 10):
        print(strings.ERROR_INVALID_FREQUENCY_SUM)
        return

    gvars.g_controller.playlist_settings = playlists
    print(strings.SETTINGS_CHANGED)

def print_presets():
    print(strings.PRESETS_LABEL)
    presets = presets.get_presets()
    for preset in presets:
        print(strings.preset_display(preset))
    print()
