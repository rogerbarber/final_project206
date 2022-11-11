import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sqlite3

# Client ID: 670aabd450884ac4b78a2cdfcc6efb9e
# Client Secret: 3c6bfedf6ddd4a579cd735ad2bd8b6d6

# Billboard Top 100 Playlist ID: 6UeSakyzhiEt4NB3UAd6NQ


# Creating spotipy object with credentials
client_credentials_manager = SpotifyClientCredentials(client_id="670aabd450884ac4b78a2cdfcc6efb9e", client_secret="3c6bfedf6ddd4a579cd735ad2bd8b6d6")
# THIS IS YOUR OBJECT BELOW
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# Grabbing track info from playlist stored above (grabbed from Spotify app)
tracklist = sp.playlist_tracks("6UeSakyzhiEt4NB3UAd6NQ")

#writing function to grab info and generate dictionary from above information

def spotipyScouring(track_list):
    song_dict = {}
    for a in track_list['items']:
        track_name = a['track']['name']
        artist_name = a['track']['artists'][0]['name']
        track_uri = a['track']['uri']
        song_dict[track_name] = {'Track URI': track_uri,'Artist Name': artist_name}
        audio_features = sp.audio_features(track_uri)[0].items()
        for a,b in audio_features:
            if a == 'type':
                break
            song_dict[track_name].update({a:b})


    return song_dict


item = spotipyScouring(tracklist)
print(item.items())




# Example of inserting many items in a list into table at once:
# data = [
#     ("Monty Python Live at the Hollywood Bowl", 1982, 7.9),
#    ("Monty Python's The Meaning of Life", 1983, 7.5),
#     ("Monty Python's Life of Brian", 1979, 8.0),
# ]
# cur.executemany("INSERT INTO movie VALUES(?, ?, ?)", data)
# con.commit()  # Remember to commit the transaction after executing INSERT.
