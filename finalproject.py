from flask import Flask, render_template,request
from bs4 import BeautifulSoup
import json, requests
# urllib.request, urllib.error, urllib.parse,

# credits to https://bigishdata.com/2016/09/27/getting-song-lyrics-from-geniuss-api-scraping/
app = Flask(__name__)
def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

#client credentials
base_url = "http://api.genius.com"
redirect_url = 'https://moosical'
client_id = 'J_taqYmJtBqKO4IIB7FYNwvXqxKFbVm4nkMednmcsSpGSaju5Jow89A9Vgixa2qj'
client_secret = '9LHiCzhnZ26ObPlLIKih2M1R7_Nwq5dPjdLu7BgqSLW2W6QprFkkQnhPBE4IHjF86sAEm0b_M3p6bJ_6LPzEyQ'
access_token = '24owyf8KJ8CV54BW4QJJMjtEG9-Mz7KKhdxr_0_OGybjtm883Mz04bjWxk2zqGSH'


# recieves the song and artist name extracted from the Spotify session and sends a request to the Genius API

base_url = "https://api.genius.com"
headers = {'Authorization': 'Bearer 24owyf8KJ8CV54BW4QJJMjtEG9-Mz7KKhdxr_0_OGybjtm883Mz04bjWxk2zqGSH'}

song_title = 'Lake Song'
artist_name = 'The Decemberists'

def lyrics_from_song_api_path(song_api_path):
    song_url = base_url + song_api_path
    response = requests.get(song_url, headers = headers)
    json = response.json()
    path = json['response']['song']['path']
    #html scraping
    page_url = 'http://genius.com' + path
    page = requests.get(page_url)
    html = BeautifulSoup(page.text, 'html.parser')
    #remove script tags in middle of lyrics
    [h.extract() for h in html('script')]
    lyrics = html.find('div', class_ = 'lyrics').get_text()

if __name__ == '__main__':
    search_url = base_url + '/search'
    data = {'q': song_title + ' ' + artist_name}
    response = requests.get(search_url, data=data, headers=headers)
    json = response.json()
    song_info = None
    for hit in json['response']['hits']:
        if hit['results']['primary_artist']['name'] == artist_name:
            song_info = hit
        break
    if song_info:
        song_api_path = song_info['result']['api_path']
        print (lyrics_from_song_api_path(song_api_path))







