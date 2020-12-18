import requests
import json
from Track import Track

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