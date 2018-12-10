from config import Config
import webbrowser
import requests
import json
import base64

class SpotifyWrapper:
    def __init__(self):
        self.config = Config()
        self.access_token = ""
        self.user = ""

    def authorize(self):
        # Request Spotify username.
        self.user = input("What is your spotify username?: ")
        
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

    def create_playlist(self):
        # Check if fragment-auto playlist exists.
        playlists = self.get_playlists()
        playlist_exists = False

        for pl in playlists:
            if pl["name"] == "fragment-auto":
                playlist_exists = True
                break
        
        # Create fragment-auto playlists if it does not exist.
        if not playlist_exists:
            url = "https://api.spotify.com/v1/users/{}/playlists".format(self.user)
            data = {"name": "fragment-auto", "description": "Automatically generated playlist for Fragment."}
            headers = self._get_standard_headers()
            headers["Content-Type"] = "application/json"
            requests.post(url, data=json.dumps(data), headers=headers)

    def get_playlists(self):
        url = "https://api.spotify.com/v1/users/{}/playlists".format(self.user)
        headers = self._get_standard_headers()
        response = requests.get(url, headers=headers)
        return json.loads(response.text)["items"]

    def _get_standard_headers(self):
        return {"Authorization": "Bearer {}".format(self.access_token)}