from flask.helpers import url_for
import json
from flask import Flask, request, redirect, render_template
import requests
from urllib.parse import quote
from GeniusAPI import GeniusAPI

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

CLIENT_ID = "c3489fd7fba04530a443381d740d1dc2"
CLIENT_SECRET = "2a8ad0b1aa4c4a9ba40c673397e9b7d5"

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)


CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 8080
REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
SCOPE = "playlist-modify-public playlist-modify-private"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

authorization_header = None
playlists = {}

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "client_id": CLIENT_ID
}


class Track():
    def __init__(self, track):
        self.name = track['track']['name']
        self.track = track
        artistList = []
        for artist in track['track']['album']['artists']:
            artistList.append(artist['name'])
        self.artists = artistList
        self.id = track['track']['id']
        self.image = track['track']['album']['images'][0]['url']
    def __str__(self):
        return self.lyrics


class Playlist():
    def __init__(self, playlist, authorization):
        self.playlist = playlist
        self.name = playlist['name']
        self.id = playlist['id']
        self.image = playlist['images'][0]['url']
        self.owner = playlist['owner']['display_name']
        tracks = requests.get(playlist['tracks']['href'], headers=authorization)
        track_data = json.loads(tracks.text)
        trackList = {}
        for track in track_data['items']:
            single = Track(track)
            trackList[single.id] = single
        self.tracks = trackList

    def __str__(self):
        return json.dumps(self.tracks, indent=4)


@app.route("/")
def index():
    url_args = "&".join(["{}={}".format(key, quote(val)) for key, val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)


@app.route("/callback/q")
def callback():
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload)
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]
    authorization_header = {"Authorization": "Bearer {}".format(access_token)}
    user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
    profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
    profile_data = json.loads(profile_response.text)
    playlist_api_endpoint = "{}/playlists".format(profile_data["href"])
    playlists_response = requests.get(playlist_api_endpoint, headers=authorization_header)
    playlist_data = json.loads(playlists_response.text)
    for playlist in playlist_data['items']:
        playlist_id = playlist['id']
        playlists[playlist_id] = Playlist(playlist=playlist, authorization=authorization_header)
    return redirect(url_for('user'))

@app.route('/user')
def user():
    return render_template('landing.html', playlists=playlists.values())

@app.route('/playlist/<playlist_id>')
def playlist(playlist_id):
    if playlist_id in playlists:
        return render_template("playlist.html", playlist=playlists[playlist_id])

@app.route('/playlist/<playlist_id>/<track_id>')
def track(playlist_id, track_id):
    if playlist_id in playlists:
        if track_id in playlists[playlist_id].tracks:
            track_name = playlists[playlist_id].tracks[track_id].name
            track_artists = playlists[playlist_id].tracks[track_id].artists[0]
            info = GeniusAPI(track_name, track_artists)
            return render_template("track.html", track=playlists[playlist_id].tracks[track_id], genius=info, lyrics=info.return_song()[0])

if __name__ == "__main__":
    app.run(debug=True, port=PORT)