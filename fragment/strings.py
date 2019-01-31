# Symbols
COMMAND_SYMBOL = ">>> "
YES_SYMBOL = "y"

# Prompt messages.
USERNAME_PROMPT = "Spotify username: "
AUTHORIZATION_CODE_PROMPT = "Please enter the code from the url you were redirected to: "
PRESET_PROMPT = "Preset name: "
OVERRIDE_PROMPT = "A preset of this name already exists, do you wish to override (y/n)? "
USE_PRESET_PROMPT = "Would you like to load settings from a preset (y/n)? "
PLAYLISTS_PROMPT = "Please enter the playlists you wish to be a part of this session.\nTo finish entering playlists, press Enter."
ASSIGN_FREQUENCY_PROMPT = "Assign a frequency to each playlist (1-10)."

# Success messages.
PRESET_SAVED = "Preset successfully saved!\n"
PRESET_LOADED = "Preset successfully loaded!\n"
SETTINGS_CHANGED = "Session settings successfully changed!\n"

# Error messages.
ERROR_INVALID_COMMAND = "Error: invalid command. For a list of commands, use 'help'.\n"
ERROR_NO_SETTINGS = "Error: No playlist settings!\n"
ERROR_PRESET_NOT_FOUND = "Error: preset not found!\n"
ERROR_NO_PLAYLISTS_ENTERED = "Error: you must enter at least one playlist!\n"
ERROR_INVALID_FREQUENCY_SUM = "Error: the sum of the frequencies you entered does not add up to 10!\n"
ERROR_GUI_NOT_IMPLEMENTED = "Error: GUI not yet implemented!"

# Labels.
SETTINGS_LABEL = "Playlist Settings"
PRESETS_LABEL = "Existing Presets"

# Miscellaneous strings.
HELP_STRING = "Available commands\n set - Allows you to change your current session settings.\n viewset - Prints your current session settings.\n saveset - Saves the current session settings as a preset.\n presets - Lists all existing presets.\n exit - Exits the application.\n"

# Formatted string functions.
def playlist_display(name, frequency):
    return "* {} ({})".format(name, frequency)

def preset_display(name):
    return "* {}".format(name)

def invalid_argument(option):
    return "Error: invalid argument for {}!\n".format(option)
