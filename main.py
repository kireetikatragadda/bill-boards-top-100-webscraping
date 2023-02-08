import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = input("enter the date in YYY-MM-DD")

url = (f"https://www.billboard.com/charts/hot-100/{date}/")

response = requests.get(url)
page = response.text

soup = BeautifulSoup(page,"html.parser")
ml = soup.find_all(name = "h3", class_ =  "c-title  a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-245 u-max-width-230@tablet-only u-letter-spacing-0028@tablet" )
songs_names_h3 = soup.select(".o-chart-results-list__item h3.c-title")
songs = [song.getText().strip( ) for song in songs_names_h3]
print(songs)

Client_ID = "164c70cb4753416c85992cd4f1a3c9f0"
Client_Secret = "8492b67fb5014ea9bc71d6fe66e5d811"
SPOTIPY_REDIRECT_URI = "http://example.com"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=Client_ID,
        client_secret=Client_Secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

#Searching Spotify for songs by title
song_uris = []
year = date.split("-")[0];
for song in songs:
    result = sp.search(q = f"track:{song} year:{year}",type="track")

    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} not on spotify")
print(song_uris)

#create playlist

playlist = sp.user_playlist_create(user= user_id, name=f"{year}'s top 100", public=False)

#add songs to the playlist
sp.playlist_add_items( playlist_id= playlist["id"], items =song_uris, position=None)