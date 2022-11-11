# Client ID: 670aabd450884ac4b78a2cdfcc6efb9e
# Client Secret: 3c6bfedf6ddd4a579cd735ad2bd8b6d6

# Billboard Top 100 Playlist ID: 6UeSakyzhiEt4NB3UAd6NQ

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Creating spotipy object with credentials
client_credentials_manager = SpotifyClientCredentials(client_id="670aabd450884ac4b78a2cdfcc6efb9e", client_secret="3c6bfedf6ddd4a579cd735ad2bd8b6d6")
# THIS IS YOUR OBJECT BELOW
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# Grabbing track info from playlist stored above (grabbed from Spotify app)
tracklist = sp.playlist_tracks("6UeSakyzhiEt4NB3UAd6NQ")
#Structure is dict -> list -> dict -> list -> dict -> list for track URI

#below grabs track name
print(tracklist['items'][0]['track']['name'])
#Below grabs artist name from track
print(tracklist['items'][0]['track']['artists'][0]['name'])
#Below finds track URI successsfully
sample_uri = tracklist['items'][0]['track']['uri']

#writing function to grab info and generate dictionary from above information

def spotipyScouring(sp_object):
    pass




# Example of inserting many items in a list into table at once:
# data = [
#     ("Monty Python Live at the Hollywood Bowl", 1982, 7.9),
#    ("Monty Python's The Meaning of Life", 1983, 7.5),
#     ("Monty Python's Life of Brian", 1979, 8.0),
# ]
# cur.executemany("INSERT INTO movie VALUES(?, ?, ?)", data)
# con.commit()  # Remember to commit the transaction after executing INSERT.
