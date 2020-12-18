from bs4 import BeautifulSoup
import json, requests
from Song import Song

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

class GeniusAPI():
    def __init__(self, name, artist):
        self.base_url = "http://api.genius.com"
        self.redirect_url = 'https://moosical'
        self.client_id = 'J_taqYmJtBqKO4IIB7FYNwvXqxKFbVm4nkMednmcsSpGSaju5Jow89A9Vgixa2qj'
        self.client_secret = '9LHiCzhnZ26ObPlLIKih2M1R7_Nwq5dPjdLu7BgqSLW2W6QprFkkQnhPBE4IHjF86sAEm0b_M3p6bJ_6LPzEyQ'
        self.access_token = '24owyf8KJ8CV54BW4QJJMjtEG9-Mz7KKhdxr_0_OGybjtm883Mz04bjWxk2zqGSH'
        self.base_url = "https://api.genius.com"
        self.headers = {'Authorization': 'Bearer 24owyf8KJ8CV54BW4QJJMjtEG9-Mz7KKhdxr_0_OGybjtm883Mz04bjWxk2zqGSH'}
        self.song_title = name
        self.artist_name = artist
        self.song = None
        search_url = self.base_url + '/search'
        data = {'q': self.song_title + ' ' + self.artist_name}
        response = requests.get(search_url, data=data, headers=self.headers)
        self.jsondata = response.json()
        song_info = None
        for hit in self.jsondata['response']['hits']:
            if hit['result']['primary_artist']['name'] == self.artist_name:
                song_info = hit
            break
        if song_info != None:
            song_api_path = song_info['result']['api_path']
            song_url = self.base_url + song_api_path
            response = requests.get(song_url, headers = self.headers)
            jsondata = response.json()
            path = jsondata['response']['song']['path']
            page_url = 'http://genius.com' + path
            page = requests.get(page_url)
            html = BeautifulSoup(page.text, 'html.parser')
            [h.extract() for h in html('script')]
            lyrics = html.find('div', class_ = 'lyrics').get_text()
            self.song = Song(jsondata, lyrics)