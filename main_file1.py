import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sqlite3
import json
import re
import matplotlib
import matplotlib.pyplot as plt

import spotifyAPI_1
import genius_lyrics_pull

def main3():
    spotifyAPI_1.main1()
    genius_lyrics_pull.main()


main3()