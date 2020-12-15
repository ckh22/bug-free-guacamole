from flask import Flask, render_template, request

requesturl = 'https://accounts.spotify.com/en/authorize?client_id=c3489fd7fba04530a443381d740d1dc2&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A8080%2Fcallback%2F&scope=playlist-read-private'
print(requesturl)
r = urllib.request.urlopen(requesturl).read()
with open('templates/auth.html', 'w') as f:
    f.write(r.decode('utf-8'))

app = Flask(__name__)
@app.route("/", methods=['GET', 'POST'])
def index():
    print(request.method)
    if request.method == 'POST':
        if request.form.get('Connect Spotify') == 'Connect Spotify':
            webbrowser.open(url=requesturl)
        else:
            return render_template("landing.html")
    elif request.method == 'GET':
        print("No Post Back Call")
    return render_template("landing.html")

@app.route('/callback/')
def auth():
    return render_template('auth.html')
if __name__=="__main__":
        app.run(host="localhost", port=8080, debug=True)
