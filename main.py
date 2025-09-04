import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
# from pprint import PrettyPrinter

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        client_id="fe5b91bc5e9c4b519a9cc1703a0e9413",
        client_secret="d2a94c51533b4aefb09fc3fdc07ced00",
        redirect_uri="http://example.com",
        show_dialog=True,
        cache_path="token.txt",
        username="ce5525wv95lj48s6dusfhahh6",
    )
)

user_id = sp.current_user()["id"]


date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")

soup = BeautifulSoup(response.text, "html.parser")

songs_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in songs_names_spans]

song_uris = []
year = date.split("-")[0]

for song in song_names:
    result = sp.search(q=f"song:{song}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"The song '{song}' doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False, description=f"{date} Billboard 100")

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
