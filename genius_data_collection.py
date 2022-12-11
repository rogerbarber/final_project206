import re
import sqlite3
import json
import matplotlib.pyplot as plt

def get_top_ten_of_each(cur, conn):
    song_word_dict = {}
    song_word_data = cur.execute("SELECT Top100.TrackName, Top100.ArtistIndex, songWordRelation.word_id, songWordRelation.count \
         FROM Top100 JOIN songWordRelation ON Top100.Rank = songWordRelation.song_rank").fetchall()

    #print(song_word_data)

    for i in range(len(song_word_data)):
        artist = cur.execute("SELECT artist FROM ArtistIndex Where artist_index = ?", (song_word_data[i][1],)).fetchone()[0]
        word = cur.execute("SELECT word FROM wordIndex Where id = ?", (song_word_data[i][2],)).fetchone()[0]
        song = song_word_data[i][0]
        count = song_word_data[i][3]

        if artist not in song_word_dict:
            song_word_dict[artist] = {}
        
        if song not in song_word_dict[artist].keys():
            song_word_dict[artist][song] = []
            song_word_dict[artist][song].append((word, count))
        else:
            song_word_dict[artist][song].append((word,count))

    #print(song_word_dict)
    return(song_word_dict)

def get_top_ten_of_all(song_word_dict):
    word_dict = {}
    for artist, song in song_word_dict.items():
        for songname, wordlist in song.items():
            for i in range(len(wordlist)):
                if wordlist[i][0] not in word_dict:
                    word_dict[wordlist[i][0]] = wordlist[i][1]
                else:
                    word_dict[wordlist[i][0]] += wordlist[i][1]
    
    sorted_top_words = sorted(word_dict.items(), key = lambda x: x[1], reverse = True)
    dataset_top_ten = sorted_top_words[:10]

    #print(dataset_top_ten)
    return(dataset_top_ten)

def write_to_json(dataset_top_ten):
    
    with open("top_ten.json", "w") as data:
        j_string = json.dumps(dataset_top_ten)
        data.write(j_string)

def plot_data():
    with open("top_ten.json", 'r') as data:
        j_string = data.read()
        top_ten = json.loads(j_string)

        #print(top_ten)
        x = []
        y = []

        for i in range(len(top_ten)):
            x.append(top_ten[i][0])
            y.append(top_ten[i][1])
        fig = plt.figure(figsize=(8,8))
        plt.subplot(111)
        plt.title("Top Ten Words of All Top Ten Across Dataset")
        plt.xlabel("Top Ten Words")
        plt.ylabel("Word Count Across Top Ten for Top100 songs")
        plt.bar(x,y, color = ['seagreen', 'lightseagreen', 'steelblue', 'slateblue', 'mediumpurple', 'mediumorchid', 'orchid', 'palevioletred', 'lightcoral','gold'])
        plt.show()
        fig.savefig("top_ten_of_top_ten.png")

def main():
    #Establish connection to the database
    conn = sqlite3.connect("spotipyTop100.db")
    cur = conn.cursor()

    #Collect data from database and find the top 10 words of all songs
    top_ten_dict = get_top_ten_of_each(cur, conn)

    #Get top ten across total 
    dataset_top_ten = get_top_ten_of_all(top_ten_dict)

    #Write data to json
    write_to_json(dataset_top_ten)

    #plot data
    plot_data()

main()