class Song():
    def __init__(self, json, lyrics):
        self.json = json
        self.lyrics = []
        self.lyrics.append(lyrics.split('\n'))
        self.fulltitle = json['response']['song']['full_title']
        self.songurl = json['response']['song']['url']
        self.description = json['response']['song']['description']['dom']['children']
    def __str__(self):
        return self.lyrics