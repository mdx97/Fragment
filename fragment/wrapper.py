import fragment.config as config
from datetime import datetime as DateTime
from datetime import timedelta as TimeDelta
import datetime
import webbrowser
import requests
import json
import base64
import os.path

DATETIME_FORMAT = "%d-%m-%y %H:%M:%S"
user = ""
access_token = ""
refresh_token = ""
credential_expiration = DateTime.utcnow()
encoded_id_secret = base64.b64encode(bytes(config.SPOTIFY_CLIENT_ID + ":" + config.SPOTIFY_CLIENT_SECRET, "utf-8")).decode("ascii")

# API Functions
def get_current_track_uri():
    _handle_credentials()
    url = "https://api.spotify.com/v1/me/player/currently-playing"
    headers = _get_standard_headers()
    response = requests.get(url, headers=headers)
    return json.loads(response.text)["item"]["uri"]

def get_playlists():
    _handle_credentials()
    url = "https://api.spotify.com/v1/users/{}/playlists".format(user)
    headers = _get_standard_headers()
    response = requests.get(url, headers=headers)
    return json.loads(response.text)["items"]

def get_playlist_names():
    playlists = get_playlists()
    return [playlist["name"] for playlist in playlists]

def get_playlist_tracks(id):
    _handle_credentials()
    url = "https://api.spotify.com/v1/playlists/{}".format(id)
    headers = _get_standard_headers()
    response = requests.get(url, headers=headers)
    return json.loads(response.text)["tracks"]["items"]
    
def play_tracks(track_uris):
    _handle_credentials()
    url = "https://api.spotify.com/v1/me/player/play"
    headers = _get_standard_headers()
    headers["Content-Type"] = "application/json"
    body = {"uris": track_uris}
    requests.put(url, data=json.dumps(body), headers=headers)

def toggle_shuffle_off():
    _handle_credentials()
    url = "https://api.spotify.com/v1/me/player/shuffle?state=false"
    headers = _get_standard_headers()
    requests.put(url, headers=headers)

# API Wrapper Functions.
def get_playlist_id_by_name(playlist_name):
    playlists = get_playlists()
    for playlist in playlists:
        if playlist["name"] == playlist_name:
            return playlist["id"]

def get_playlist_track_uris(id):
    data = get_playlist_tracks(id)
    uris = []
    for track in data:
        uris.append(track["track"]["uri"])
    return uris

def _get_standard_headers():
    return {"Authorization": "Bearer {}".format(access_token)}

def _handle_credentials():
    if credentials_expired():
        refresh_credentials()

# Credential Management
def get_authorization_code():
    authorization_token_request_url = "https://accounts.spotify.com/authorize?response_type=code&client_id=" + config.SPOTIFY_CLIENT_ID + "&scope=" + config.SPOTIFY_SCOPES + "&redirect_uri=" + config.SPOTIFY_REDIRECT_URI
    webbrowser.open(authorization_token_request_url)

def authorize(authorization_code):
    _get_tokens("authorization_code", authorization_code)

def refresh_credentials():
    _get_tokens("refresh_token", refresh_token)

def _get_tokens(grant_type, auth_token):
    global access_token
    global refresh_token
    global credential_expiration
    request_headers = {"Authorization": "Basic {}".format(encoded_id_secret), "Content-Type": "application/x-www-form-urlencoded"}
    request_body = {"grant_type": grant_type}
    
    if grant_type == "authorization_code":
        request_body["code"] = auth_token
        request_body["redirect_uri"] = config.SPOTIFY_REDIRECT_URI
        request_body["client_id"] = config.SPOTIFY_CLIENT_ID
    elif grant_type == "refresh_token":
        request_body["refresh_token"] = auth_token

    response = requests.post("https://accounts.spotify.com/api/token", data=request_body, headers=request_headers)
    response_data = json.loads(response.text)
    access_token = response_data["access_token"]

    if "refresh_token" in response_data.keys():
        refresh_token = response_data["refresh_token"]
        
    credential_expiration = DateTime.utcnow() + TimeDelta(seconds=response_data["expires_in"])
    sync_authfile()

def is_authorized():
    return user and access_token

def credentials_expired():
    return DateTime.utcnow() > credential_expiration

def set_user(new_user):
    global user
    user = new_user
    sync_authfile()

def sync_authfile():
    authfile = open(".authfile", "w")
    authfile.write(user)
    authfile.write("\n")
    authfile.write(access_token)
    authfile.write("\n")
    authfile.write(refresh_token)
    authfile.write("\n")
    authfile.write(credential_expiration.strftime(DATETIME_FORMAT))
    authfile.close()

def load_authfile():
    global user
    global access_token
    global refresh_token
    global credential_expiration
    if os.path.isfile(".authfile"):
        authfile = open(".authfile", "r")
        user = authfile.readline().rstrip()
        access_token = authfile.readline().rstrip()
        refresh_token = authfile.readline().rstrip()
        credential_expiration = DateTime.strptime(authfile.readline().rstrip(), DATETIME_FORMAT)
        authfile.close()

load_authfile()

