import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sqlite3
import json
import re
import matplotlib
import matplotlib.pyplot as plt
import spotifyAPI_2
import genius_data_collection

def main4():
    spotifyAPI_2.main2()
    genius_data_collection.main()

main4()
