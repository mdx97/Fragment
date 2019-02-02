import fragment.globals as gvars
import fragment.wrapper as wrapper
import tkinter as tk

def gui_main():
    gvars.g_Tkroot = tk.Tk()
   
    # Dropdown menu label.
    tk.Label(gvars.g_Tkroot, text="Playlists").pack()

    # Playlist selection dropdown menu.
    var = tk.StringVar(gvars.g_Tkroot)
    choices = wrapper.get_playlist_names() 
    var.set(choices[0])
    playlist_options = tk.OptionMenu(gvars.g_Tkroot, var, *choices)
    playlist_options.pack()
    
    # Add playlist button.
    tk.Button(gvars.g_Tkroot, text="Add Playlist").pack()

    gvars.g_Tkroot.mainloop()
