class Song():
    def __init__(self, json, lyrics):
        self.json = json
        self.lyrics = lyrics
        self.url = json['response']['song']['album']['artist']['url']
        self.coverart = json['response']['song']['album']['cover_art_url']
        self.fulltitle = json['response']['song']['full_title']
        self.songurl = json['response']['song']['url']
        self.desciption = json['response']['song']['description']['dom']['children']
    def __str__(self):
        return self.lyrics