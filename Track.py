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