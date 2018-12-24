A user can define which playlists the current session will draw tracks from and at what frequency.

For example, the user selects playlist A and playlist B and sets the frequency of playlist A to be 8 and the frequency of playlist B to be 2. This means that 8/10 tracks will be from playlist A and 2/10 tracks will be from playlist B.

Fragment will pull tracks from the specified playlists at their defined frequencies and add them to the song queue. Once the song queue passes below QUEUE_MIN number of tracks, Fragment will refill the queue with tracks up to QUEUE_MAX number of tracks with the present settings (meaning the user can *dynamically* change the session settings).

Presets
----------
Presets can be used to save a session's settings for later use. Presets are saved in a plain text file with the following data:
- Preset name.
- Playlist names and their frequencies (1-10).


