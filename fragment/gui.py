import tkinter as tk
from fragment.globals import g_controller, g_Tkroot

def gui_main():
    g_Tkroot = tk.Tk()
   
    # Dropdown menu label.
    tk.Label(g_Tkroot, text="Playlists").pack()

    # Playlist selection dropdown menu.
    var = tk.StringVar(g_Tkroot)
    choices = g_controller.spotify_wrapper.get_playlist_names() 
    var.set(choices[0])
    playlist_options = tk.OptionMenu(g_Tkroot, var, *choices)
    playlist_options.pack()
    
    # Add playlist button.
    tk.Button(g_Tkroot, text="Add Playlist").pack()

    g_Tkroot.mainloop()
