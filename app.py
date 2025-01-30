from flask import Flask, render_template, redirect, url_for, request, session
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

SPOTIFY_CLIENT_ID = "af4cae999c184ad7b760fb8c51b60d60"
SPOTIFY_CLIENT_SECRET = "9d1c008a6aaa4a969b178224406d5a73"
SPOTIFY_REDIRECT_URI = "https://5001-santianaalex-spotifyapi-76oqy36jqks.ws-eu117.gitpod.io/callback"

app = Flask(__name__)
app.secret_key = 'chiave_per_session' 

sp_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-read-private" ,
    show_dialog=True 
)

@app.route('/home')
def home():
    token_info = session.get('token_info', None)
    if not token_info:
        return redirect(url_for('login'))
    sp = spotipy.Spotify(auth=token_info['access_token']) 
    user_info = sp.current_user()
    print(user_info)
    playlists = sp.current_user_playlists() 
    playlists_info = playlists['items'] 
    return render_template('home.html', user_info=user_info, playlists=playlists_info)

@app.route('/')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code) 
    session['token_info'] = token_info
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)