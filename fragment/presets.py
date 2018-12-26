from fragment import controller
import os

def preset_directory_exists():
    return os.path.isdir("presets")

def init_preset_directory():
        if not preset_directory_exists():
            os.makedirs("presets")

def get_preset(name):
    if not preset_exists(name):
        return []

    filename = get_preset_filename(name)
    lines = [line.rstrip("\n") for line in open(filename)]
    playlist_settings = []

    for line in lines:
        values = line.split(",")
        name = values[0]
        freq = int(values[1])
        setting = controller.PlaylistSetting(name, freq)
        playlist_settings.append(setting)

    return playlist_settings

def save_preset(name, playlist_settings):
    init_preset_directory()
    filename = get_preset_filename(name)
    preset_file = open(filename, "w")

    for setting in playlist_settings:
        preset_file.write(setting.name + "," + str(setting.frequency))
        preset_file.write("\n")

    preset_file.close()

def preset_exists(name):
    if not preset_directory_exists():
        return False
    return os.path.isfile(get_preset_filename(name))

def get_preset_filename(name):
    return "presets/{}.preset".format(name)