from fragment import config
from datetime import datetime as DateTime
from datetime import timedelta as TimeDelta
import datetime
import webbrowser
import requests
import json
import base64
import os.path

DATETIME_FORMAT = "%d-%m-%y %H:%M:%S"

class SpotifyWrapper:
    def __init__(self):
        self.credential_manager = CredentialManager()

    # Direct API Functions.
    def play_tracks(self, track_uris):
        self._handle_credentials()
        url = "https://api.spotify.com/v1/me/player/play"
        headers = self._get_standard_headers()
        headers["Content-Type"] = "application/json"
        body = {"uris": track_uris}
        response = requests.put(url, data=json.dumps(body), headers=headers)
    
    def get_current_track_uri(self):
        self._handle_credentials()
        url = "https://api.spotify.com/v1/me/player/currently-playing"
        headers = self._get_standard_headers()
        response = requests.get(url, headers=headers)
        return json.loads(response.text)["item"]["uri"]

    def get_playlists(self):
        self._handle_credentials()
        url = "https://api.spotify.com/v1/users/{}/playlists".format(self.credential_manager.user)
        headers = self._get_standard_headers()
        response = requests.get(url, headers=headers)
        return json.loads(response.text)["items"]
    
    def get_playlist_tracks(self, id):
        self._handle_credentials()
        url = "https://api.spotify.com/v1/playlists/{}".format(id)
        headers = self._get_standard_headers()
        response = requests.get(url, headers=headers)
        return json.loads(response.text)["tracks"]["items"]

    # API Wrapper Functions.
    def get_playlist_id_by_name(self, playlist_name):
        playlists = self.get_playlists()
        for playlist in playlists:
            if playlist["name"] == playlist_name:
                return playlist["id"]

    def get_playlist_track_uris(self, id):
        data = self.get_playlist_tracks(id)
        uris = []
        for track in data:
            uris.append(track["track"]["uri"])
        return uris

    def _get_standard_headers(self):
        return {"Authorization": "Bearer {}".format(self.credential_manager.access_token)}

    def _handle_credentials(self):
        if self.credential_manager.credentials_expired():
            self.credential_manager.refresh_credentials()

class CredentialManager:
    def __init__(self):
        self.config = config.CredentialConfiguration
        self.access_token = ""
        self.refresh_token = ""
        self.credential_expiration = DateTime.utcnow()
        self.user = ""
        self.load_authfile()
        self.authorize()

    def sync_authfile(self):
        authfile = open(".authfile", "w")
        authfile.write(self.user)
        authfile.write("\n")
        authfile.write(self.access_token)
        authfile.write("\n")
        authfile.write(self.refresh_token)
        authfile.write("\n")
        authfile.write(self.credential_expiration.strftime(DATETIME_FORMAT))
        authfile.close()
    
    def load_authfile(self):
        if os.path.isfile(".authfile"):
            authfile = open(".authfile", "r")
            self.user = authfile.readline().rstrip()
            self.access_token = authfile.readline().rstrip()
            self.refresh_token = authfile.readline().rstrip()
            self.credential_expiration = DateTime.strptime(authfile.readline().rstrip(), DATETIME_FORMAT)
            authfile.close()

    def refresh_credentials(self):
        encoded_id_secret = self.generate_secret()
        request_body = {"grant_type": "refresh_token", "refresh_token": self.refresh_token}
        request_headers = {"Authorization": "Basic {}".format(encoded_id_secret), "Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post("https://accounts.spotify.com/api/token", data=request_body, headers=request_headers)
        response_data = json.loads(response.text)
        self.access_token = response_data["access_token"]
        if "refresh_token" in response_data.keys():
            self.refresh_token = response_data["refresh_token"]
        self.credential_expiration = DateTime.utcnow() + TimeDelta(seconds=response_data["expires_in"])
        self.sync_authfile()

    def credentials_expired(self):
        return DateTime.utcnow() > self.credential_expiration

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
            encoded_id_secret = self.generate_secret()
            request_body = {"grant_type": "authorization_code", "code": authorization_code, "redirect_uri": self.config.SPOTIFY_REDIRECT_URI, "client_id": self.config.SPOTIFY_CLIENT_ID}
            request_headers = {"Authorization": "Basic {}".format(encoded_id_secret), "Content-Type": "application/x-www-form-urlencoded"}
            response = requests.post("https://accounts.spotify.com/api/token", data=request_body, headers=request_headers)
            response_data = json.loads(response.text)
            self.access_token = response_data["access_token"]
            self.refresh_token = response_data["refresh_token"]
            self.credential_expiration = DateTime.utcnow() + TimeDelta(seconds=response_data["expires_in"])
            self.sync_authfile()
    
    def generate_secret(self):
        return base64.b64encode(bytes(self.config.SPOTIFY_CLIENT_ID + ":" + self.config.SPOTIFY_CLIENT_SECRET, "utf-8")).decode("ascii")