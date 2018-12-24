from fragment import config
import webbrowser
import requests
import json
import base64
import os.path

class SpotifyWrapper:
    def __init__(self):
        self.credential_manager = CredentialManager()
        self.playlist_id = ""

    def create_playlist(self):
        # Check if fragment-auto playlist exists.
        playlists = self.get_playlists()
        playlist_exists = False

        for pl in playlists:
            if pl["name"] == "fragment-auto":
                self.playlist_id = pl["id"]
                playlist_exists = True
                break
        
        # Create fragment-auto playlists if it does not exist.
        if not playlist_exists:
            url = "https://api.spotify.com/v1/users/{}/playlists".format(self.credential_manager.user)
            data = {"name": "fragment-auto", "description": "Automatically generated playlist for Fragment."}
            headers = self._get_standard_headers()
            headers["Content-Type"] = "application/json"
            response = requests.post(url, data=json.dumps(data), headers=headers)
            self.playlist_id = json.loads(response.text)["id"]

    def get_playlists(self):
        url = "https://api.spotify.com/v1/users/{}/playlists".format(self.credential_manager.user)
        headers = self._get_standard_headers()
        response = requests.get(url, headers=headers)
        return json.loads(response.text)["items"]

    def get_playlist_tracks(self, id):
        url = "https://api.spotify.com/v1/playlists/{}".format(id)
        headers = self._get_standard_headers()
        response = requests.get(url, headers=headers)
        return json.loads(response.text)["tracks"]["items"]
    
    def add_track(self, uri):
        url = "https://api.spotify.com/v1/playlists/{}/tracks".format(self.playlist_id)
        headers = self._get_standard_headers()
        headers["Content-Type"] = "application/json"
        data = {"uris": [uri]}
        requests.post(url, data=json.dumps(data), headers=headers)

    def play_playlist(self):
        url = "https://api.spotify.com/v1/me/player/play"
        headers = self._get_standard_headers()
        data = {"context_uri": "spotify:playlist:{}".format(self.playlist_id)}
        requests.put(url, data=json.dumps(data), headers=headers)

    def _get_standard_headers(self):
        return {"Authorization": "Bearer {}".format(self.credential_manager.access_token)}

class CredentialManager:
    def __init__(self):
        self.config = config.CredentialConfiguration
        self.access_token = ""
        self.user = ""
        self.load_authfile()
        self.authorize()

    def sync_authfile(self):
        authfile = open(".authfile", "w")
        authfile.write(self.user)
        authfile.write("\n")
        authfile.write(self.access_token)
        authfile.close()
    
    def load_authfile(self):
        if os.path.isfile(".authfile"):
            authfile = open(".authfile", "r")
            self.user = authfile.readline().rstrip()
            self.access_token = authfile.readline().rstrip()
            authfile.close()
    
    def authorize(self):
        # Request Spotify username.
        if not self.user:
            self.user = input("What is your spotify username?: ")
            self.sync_authfile()
        
        if not self.access_token:
            # Retrieve authorization token from API.
            authorization_token_request_url = "https://accounts.spotify.com/authorize?response_type=code&client_id=" + self.config.SPOTIFY_CLIENT_ID + "&scope=" + self.config.SPOTIFY_SCOPES + "&redirect_uri=" + self.config.SPOTIFY_REDIRECT_URI
            webbrowser.open(authorization_token_request_url)
            authorization_code = input("Please enter the code from the redirect uri: ")
            
            # Use the authorization token to receive an access token from the API.
            encoded_id_secret = base64.b64encode(bytes(self.config.SPOTIFY_CLIENT_ID + ":" + self.config.SPOTIFY_CLIENT_SECRET, "utf-8")).decode("ascii")
            request_body = {"grant_type": "authorization_code", "code": authorization_code, "redirect_uri": self.config.SPOTIFY_REDIRECT_URI, "client_id": self.config.SPOTIFY_CLIENT_ID}
            request_headers = {"Authorization": "Basic {}".format(encoded_id_secret), "Content-Type": "application/x-www-form-urlencoded"}
            response = requests.post("https://accounts.spotify.com/api/token", data=request_body, headers=request_headers)
            response_data = json.loads(response.text)
            self.access_token = response_data["access_token"]
            self.sync_authfile()