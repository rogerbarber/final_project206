import re
import sqlite3

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

    print(song_word_dict)
    return(song_word_dict)

def get_top_of_each(song_word_dict):
    word_dict = {}
    for artist, song in song_word_dict.items():
        for songname, wordlist in song.items():
            for i in range(len(wordlist)):
                if wordlist[i][0] not in word_dict:
                    


def main():
    #Establish connection to the database
    conn = sqlite3.connect("spotipyTop100.db")
    cur = conn.cursor()

    #Collect data from database and find the top 10 words of all songs
    top_words = get_top_ten_of_all(cur, conn)

main()