import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sqlite3
import json
import re
import matplotlib
import matplotlib.pyplot as plt

# Client ID: 670aabd450884ac4b78a2cdfcc6efb9e
# Client Secret: 3c6bfedf6ddd4a579cd735ad2bd8b6d6

# Billboard Top 100 Playlist ID: 6UeSakyzhiEt4NB3UAd6NQ

# Write function to create artist ID list using id numbers and artist names
# Inputs: track_list generated from spotipy object for billboard top 100
# Outputs: dictionary with index, artist name as key, value.
def artistIndex(track_list):
    id_dict = {}
    start = 0
    for a in track_list['items']:
        artist_name = a['track']['artists'][0]['name']
        if artist_name not in id_dict.values():
            id_dict[start] = id_dict.get(start, artist_name)
            start += 1
    return id_dict

# write function to generate genre index
# Inputs: dictionary of song features, spotipy object.
# Outputs: A dictionary with index, genre as key, value.
def genreIndex(track_list, sp):
    genre_dict = {}
    genre_id = 1
    genre_dict[0] = "none"
    for a in track_list['items']:
        artist_id = a['track']['album']['artists'][0]['id']
        artist_info = sp.artist(artist_id)
        if len(artist_info['genres']) > 0:
            if artist_info["genres"][0] not in genre_dict.values():
                genre_dict[genre_id] = genre_dict.get(genre_id, artist_info["genres"][0])
                genre_id += 1
    return genre_dict


#Write function to consolidate artist info and track features
#Inputs: Dictionary of song features, indexed dictionary of artists, indexed dictionary of genres, Spotipy object.
#Outputs: a complete dictionary of audio features, with genre-index and artist-index.
def spotipyScouring(track_list, artist_index, genre_index, sp):
    song_dict = {}
    rank = 1
    for a in track_list['items']:
        re_track = re.split(" +[(-].{5,}", a['track']['name'])
        track = re_track[0]
        if track in song_dict.keys():
            track_name = track + "(Duplicate)"
        else:
            track_name = track
        for c in artist_index.items():
            if c[1] == a['track']['artists'][0]['name']:
                 artist_int = c[0]
        track_uri = a['track']['uri']
        song_dict[track_name] = {'Track URI': track_uri,'Artist Index': artist_int}
        artist_id = a['track']['album']['artists'][0]['id']
        artist_info = sp.artist(artist_id)
        for item in genre_index.items():
            if len(artist_info['genres']) > 0:
                if artist_info['genres'][0] == item[1]:
                    genre_id = item[0]
            else:
                genre_id = 0
        song_dict[track_name].update({"Genre Index":genre_id})
        song_dict[track_name].update({"Rank": rank})
        rank += 1
        audio_features = sp.audio_features(track_uri)[0].items()
        for a,b in audio_features:
            if a == 'type':
                break
            song_dict[track_name].update({a:b})
    return song_dict

# Runs up to max_rank, 25 in this case, per run.
# Current input: Complete dictionary for main table (output of spotipyScouring).
# Output: create table with 25 items, update table with 25 items per run.
def createSongTable25(song_dict):
    conn = sqlite3.connect('spotipyTop100.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Top100 (Rank INTEGER PRIMARY KEY, TrackName TEXT, TrackURI BLOB, ArtistIndex TEXT, GenreIndex INTEGER, Danceability FLOAT, Energy FLOAT, Speechiness FLOAT, Valence FLOAT)")
    conn.commit()
    check = cur.execute("SELECT Rank FROM Top100").fetchall()
    if len(check) == len(song_dict.items()):
        print("The song table is fully created. Terminating function.")
        return True
    if len(check) < 24:
        print("Initiating song table with first 25 items.")
        for i in range(1,26):
            for a,b in song_dict.items():
                if b['Rank'] == i:
                    track_name = a
                    uri = b['Track URI']
                    artist_index = b['Artist Index']
                    genre_index = b['Genre Index']
                    dance = b['danceability']
                    energy = b['energy']
                    speech = b['speechiness']
                    valence = b['valence']
                    song_tup = (b['Rank'], track_name, uri, artist_index, genre_index, dance, energy, speech, valence)
                    cur.execute("INSERT INTO Top100 (Rank, TrackName, TrackURI, ArtistIndex, GenreIndex, Danceability, Energy, Speechiness, Valence) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", song_tup)
        conn.commit()
        conn.close()
    else:
        print("Song Table has existing items. Beginning from last known index.")
        try:
            for i in range(len(check)+1, len(check)+26):
                for a,b in song_dict.items():
                    if b['Rank'] == i:
                        track_name = a
                        uri = b['Track URI']
                        artist_index = b['Artist Index']
                        genre_index = b['Genre Index']
                        dance = b['danceability']
                        energy = b['energy']
                        speech = b['speechiness']
                        valence = b['valence']
                        song_tup = (b['Rank'], track_name, uri, artist_index, genre_index, dance, energy, speech, valence)
                        cur.execute("INSERT INTO Top100 (Rank, TrackName, TrackURI, ArtistIndex, GenreIndex, Danceability, Energy, Speechiness, Valence) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", song_tup)
            conn.commit()
        except:
            print("Exceeded index range of available items (Genre Table). Committing current progress and ending function.")
            conn.commit()
        conn.close()

#Creating function to run genre, artist, and song table in order. 25 items max.
#Input: genre_index, artist_index, track_features dictionaries.
#Output: three tables. nothing returned to program space.
def tableWriter25(artist_index, genre_index, track_features):
    createGenreTable25(genre_index)
    createArtistTable25(artist_index)
    createSongTable25(track_features)
    return print("----------------------")
    


# Write function to create table for genre id's.
# Inputs: genre_index dictionary.
# Outputs: a table for genre_index, with integer and genre string. A print statement if table or row already exists.
def createGenreTable25(genre_dict):
    conn = sqlite3.connect("spotipyTop100.db")
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS GenreIndex (genre_index INTEGER PRIMARY KEY, genre TEXT)')
    conn.commit()
    check = cur.execute("SELECT genre_index, genre FROM GenreIndex").fetchall()
    if len(check) == len(genre_dict.items()):
        print("The genre table is fully created. Terminating function.")
        return True
    if len(check) < 24:
        print("Initiating genre table with first 25 items.")
        for i in range(25):
            cur.execute("INSERT INTO GenreIndex (genre_index, genre) VALUES (?, ?)",
            (i,genre_dict[i]))
        conn.commit()
        conn.close()
    else:
        print("Genre Table has existing items. Beginning from last known index.")
        try:
            for i in range(len(check), len(check)+25):
                cur.execute("INSERT INTO GenreIndex (genre_index, genre) VALUES (?, ?)", (i, genre_dict[i]))
                conn.commit()
        except:
            print("Exceeded index range of available items (Genre Table). Committing current progress and ending function.")
            conn.commit()
        conn.close()


# Write function to create table for artist id's.
# Inputs: artist_index dictionary.
# Outputs: a table for artist_index, with integer and name string.
def createArtistTable25(artist_dict):
    conn = sqlite3.connect("spotipyTop100.db")
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS ArtistIndex (artist_index INTEGER PRIMARY KEY, artist TEXT)')
    conn.commit()
    check = cur.execute("SELECT artist_index, artist FROM ArtistIndex").fetchall()
    if len(check) == len(artist_dict.items()):
        print("The artist table is fully created. Terminating function.")
        return True
    if len(check) < 24:
        print("Initiating artist table with first 25 items.")
        for i in range(25):
            cur.execute("INSERT INTO ArtistIndex (artist_index, artist) VALUES (?, ?)",
            (i,artist_dict[i]))
        conn.commit()
        conn.close()
    else:
        print("Artist Table has existing items. Beginning from last known index.")
        try:
            for i in range(len(check), len(check)+25):
                cur.execute("INSERT INTO ArtistIndex (artist_index, artist) VALUES (?, ?)", (i, artist_dict[i]))
                conn.commit()
        except:
            print("Exceeded index range of available items (Artist Table). Committing current progress and ending function.")
            conn.commit()
            conn.close()


def main1():
# Creating DB file
    try:
        with open("spotipyTop100.db", "r") as handle:
# Creating spotipy object with credentials
            client_credentials_manager = SpotifyClientCredentials(client_id="670aabd450884ac4b78a2cdfcc6efb9e", client_secret="3c6bfedf6ddd4a579cd735ad2bd8b6d6")
# THIS IS YOUR OBJECT BELOW
            sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
# Grabbing track info from playlist stored above (grabbed from Spotify app)
            tracklist = sp.playlist_tracks("6UeSakyzhiEt4NB3UAd6NQ")
# Creating a genre index file
            genre_index = genreIndex(tracklist, sp)
# Creating artist index file
            artist_index = artistIndex(tracklist)
# Creating track information file (track features)
            track_features = spotipyScouring(tracklist, artist_index, genre_index, sp)
# Writing 25 items to each table, beginning with genre_index.
            tableWriter25(artist_index, genre_index, track_features)
            
    except:
        with open("spotipyTop100.db", "w") as handle:
# Creating spotipy object with credentials
            client_credentials_manager = SpotifyClientCredentials(client_id="670aabd450884ac4b78a2cdfcc6efb9e", client_secret="3c6bfedf6ddd4a579cd735ad2bd8b6d6")
# THIS IS YOUR OBJECT BELOW
            sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
# Grabbing track info from playlist stored above (grabbed from Spotify app)
            tracklist = sp.playlist_tracks("6UeSakyzhiEt4NB3UAd6NQ")
# Creating a genre index file
            genre_index = genreIndex(tracklist, sp)
# Creating artist index file
            artist_index = artistIndex(tracklist)
# Creating track information file (track features)
            track_features = spotipyScouring(tracklist, artist_index, genre_index, sp)
# Writing 25 items to each table, beginning with genre_index.
            tableWriter25(artist_index, genre_index, track_features)
            
