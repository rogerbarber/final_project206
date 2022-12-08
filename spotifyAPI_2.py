import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sqlite3
import json
import re
import matplotlib
import matplotlib.pyplot as plt



# Input: A filename to be written to.
# Output: A text file that has the average scores for the four music metrics provided by the Spotify track information. No output returned to the program space.
def scoreAverage(output):
    conn = sqlite3.connect('spotipyTop100.db')
    cur = conn.cursor()
    average = cur.execute("SELECT Danceability, Energy, Speechiness, Valence FROM Top100")
    average_dict = {}
    for item in average:
        average_dict['Danceability'] = average_dict.get('Danceability', 0) + float(item[0])
        average_dict['Energy'] = average_dict.get('Energy', 0) + float(item[1])
        average_dict['Speechiness'] = average_dict.get('Speechiness', 0) + float(item[2])
        average_dict['Valence'] = average_dict.get('Valence', 0) + float(item[3])
    for key in average_dict:
        average_dict[key] = round((average_dict.get(key)/100), 3)
    with open(output, 'w') as handle:
        j_string = json.dumps(average_dict)
        handle.write(j_string)

# Input: A filename to be written to.
# Output: A text file that contains a count of the different genres present in the top 100. The groupings are 'pop', 'rock', 'country', 'hip hop', 'rap', 'indie' - there will also be individual entries if the genre does not exist in these larger sub-groupings.
def genreCount(output):
    conn = sqlite3.connect('spotipyTop100.db')
    cur = conn.cursor()
    genre_count = cur.execute("SELECT Top100.TrackName, GenreIndex.genre FROM Top100 JOIN GenreIndex ON Top100.GenreIndex = GenreIndex.genre_index")
    genre_dict = {}
    for item in genre_count:
        if "indie" in item[1]:
            genre_dict['indie'] = genre_dict.get('indie', 0) + 1
        elif "pop" in item[1]:
            genre_dict['pop'] = genre_dict.get('pop', 0) + 1
        elif "rock" in item[1]:
            genre_dict['rock'] = genre_dict.get('rock', 0) + 1
        elif 'country' in item[1]:
            genre_dict['country'] = genre_dict.get('country', 0) + 1
        elif 'hip hop' in item[1]:
            genre_dict['hip hop'] = genre_dict.get('hip hop', 0) + 1
        elif 'rap' in item[1]:
            genre_dict['rap'] = genre_dict.get('rap', 0) + 1
        else:
            genre_dict[item[1]] = genre_dict.get(item[1], 0) + 1
    with open(output, 'w') as handle:
        j_string = json.dumps(genre_dict)
        handle.write(j_string)

# Input: A filename to write to.
# Output: a text file that has a count of how many songs in the top 100 belong to a certain artist. Nothing is returned to the program space.
def artistCount(output):
    conn = sqlite3.connect('spotipyTop100.db')
    cur = conn.cursor()
    artist_count = cur.execute("SELECT Top100.TrackName, ArtistIndex.artist FROM Top100 JOIN ArtistIndex ON Top100.ArtistIndex = ArtistIndex.artist_index")
    artist_dict = {}
    for item in artist_count:
        artist_dict[item[1]] = artist_dict.get(item[1], 0) + 1
    with open(output, 'w') as handle:
        j_string = json.dumps(artist_dict)
        handle.write(j_string)

# Input: a filename to pull information from in order to create a bar graph. Designed for scoreAverage function.
# Output: Shows a plot of the bar graph. Saves a picture of the plot as an image file in the file directory. Nothing returned to program space.
def bar_graph(filename):
    with open(filename, "r") as handle:
        string = handle.read()
        j_dict = json.loads(string)
        x = []
        y = []
        for a,b in j_dict.items():
            x.append(a)
            y.append(b)
        fig = plt.figure(figsize=(8, 8))
        plt.subplot(111)
        plt.title("Top 100 Songs - Average Audio Scores")
        plt.xlabel("Song Metric Categories")
        plt.ylabel("Counts (0.0 to 1.0)")
        plt.bar(x,y, color=['lightcoral', 'blue', 'green', 'aquamarine'])
        plt.show()
        fig.savefig("scoreAverageGraph.png")

# Input: a filename to pull information from in order to create a pie chart. Designed for artistCount function.
# Output: Shows a plot of the pie chart. Saves a picture of the pie chart as an image file in the file directory. Nothing returned to program space.
def pie_chart(filename):
    with open(filename, 'r') as handle:
        string = handle.read()
        j_dict = json.loads(string)
        new_dict = {}
        for a,b in j_dict.items():
            if b < 2:
                new_dict['Single Song'] = new_dict.get("Single Song", 0) + 1
            else:
                new_dict[a] = b
        artists = []
        counts = []
        for a, b in new_dict.items():
            artists.append(a)
            counts.append(b)
        fig, ax = plt.subplots()
        ax.pie(counts, labels=artists, shadow=True)
        ax.axis('equal')
        plt.show()
        fig.savefig("artistCountPieChart.png")

#Input: a filename to pull data from for making a horizontal bar chart. Designed for genre count.
#Output: shows a plot within the program space, and saves an image to the directory.
def barh_chart(filename):
    with open(filename, "r") as handle:
        string = handle.read()
        j_dict = json.loads(string)
        genres = []
        counts = []
        for a,b in j_dict.items():
            genres.append(a)
            counts.append(b)
        fig = plt.figure(figsize=(10,10))
        plt.subplot(111)
        plt.title("Top 100 - Genre Composition")
        plt.barh(genres,counts)
        plt.show()
        fig.savefig("genreCountBarH.png")
        



def main2():
# Selecting data from tables (3 tables to pull from)
# Expecting multiple functions for multiple files, calculating a few things.
# Calculating average of music category scores and writing to file.
    scoreAverage("scoreAverage.json")
# Calculating count of genres, sorted by main genre (when possible).
    genreCount("genreCount.json")
# Calculating count of songs by certain artists on the top 100.
    artistCount("artistCount.json")
# Plotting information from written files.
    bar_graph("scoreAverage.json")
    pie_chart("artistCount.json")
    barh_chart("genreCount.json")



main2()