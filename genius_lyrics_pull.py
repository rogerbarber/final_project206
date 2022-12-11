import lyricsgenius as lg
import json
import re
import sqlite3

API_KEY = "CUAq9PoXth-VccgEW1vqALmmefhkarPZI3DgyYPJLOfsKVrPvaN3YLJz4wmFdmSQ"

def pull_songdata(cur, con, length = 0):
    song_info = cur.execute("SELECT Top100.rank, Top100.TrackName, ArtistIndex.artist \
        From Top100 JOIN ArtistIndex ON Top100.ArtistIndex = ArtistIndex.artist_index")
    song_dict = {}

    song = song_info.fetchall()
    #print(song)

    check = cur.execute("SELECT max(Rank) FROM Top100").fetchone()
    #print(type(check[0]))
    if check[0] == 0:
        for i in range(1, check[0] + 26):
            song = song_info.fetchone()
            #print(song)

            if song[2] not in song_dict:
                song_dict[song[2]] = [(song[0], song[1])]
            else:
                song_dict[song[2]] += [(song[0], song[1])]
        return song_dict
    else:
        for i in range(check[0] - 25, check[0]): #Change back to check[0] - 25, check[0]
            dict_song = song[i]
            #print(dict_song)

            if song[i][2] not in song_dict:
                #print(song[i][2])
                song_dict[song[i][2]] = [(song[i][0], song[i][1])]
            else:
                song_dict[song[i][2]] += [(song[i][0], song[i][1])]
        #print(song_dict)
        return song_dict

def lyric_search(genius, song_dict):
    lyrics_dict = {}
    pattern = r" +[-(].{5,}"

    for artist, songs in song_dict.items():
        lyrics_dict[artist] = {}
        for songname in songs:
            lyrics_dict[artist][songname[1]] = {}
            try:
                song = genius.search_song(songname[1], artist)
            except:
                print("Search failed, skip ",songname[1])
            lyrics_dict[artist][songname[1]] = song.lyrics
    #print(lyrics_dict)       
    return lyrics_dict

def clean_and_count_lyrics(data_packet):
    word_counts = {}
    ignore_lst = ['the', 'and', 'be', 'for', 'to', '', 'am', 'a', 'how', 'in', 'of', \
                  'this', 'that', 'there', 'is', 'isn\'t', 'was', 'wasn\'t', \
                  'it', 'oh', 'mm', 'on', 'it\'s', 'at', 'ah', 'i', 'me', 'we', 'you', \
                  'i\'m', 'you\'re',]
    lyric_lead_pattern = r".*[lL]yrics+"
    section_header_pattern = r"\[.*?\]"
    embed_msg_pattern = r"You might also like*[\d]*|Embed|\dEmbed"

    #print(data_packet)

    for artist, song in data_packet.items():
        for songname, lyrics in song.items():
            #print(str(lyrics))
            word_counts[songname] = {}
            string_clean_one = str(lyrics).replace("\n", " ")
            string_clean_two = re.sub(section_header_pattern, " ", string_clean_one)
            string_clean_three = re.sub(lyric_lead_pattern, " ", string_clean_two)
            string_clean_four = re.sub(embed_msg_pattern, " ", string_clean_three)
            string_clean_five = string_clean_four.replace("  ", " ")
            string_clean_six = string_clean_five.replace("(", " ")
            string_clean_seven = string_clean_six.replace(")", " ")
            string_clean_eight = string_clean_seven.replace('" ', ' ')
            string_clean_nine = string_clean_eight.replace(' "', ' ')
            string_clean_ten = string_clean_nine.replace(',', '')
            string_clean_eleven = string_clean_ten.replace('?', '')

            cleaned_lyrics_lst = string_clean_eleven.split(" ")
                
            for word in cleaned_lyrics_lst:
                if word.lower() in ignore_lst:
                    continue
                else:
                    if word.lower() not in word_counts[songname]:
                        word_counts[songname][word.lower()] = 1
                    else:
                        word_counts[songname][word.lower()] += 1

    #print(word_counts)
    return word_counts

def find_top_ten(word_counts):
    top_ten_words = {}
    rank = 1

    for songname, words in word_counts.items():
        top_ten_words[rank]={}
        top_ten_words[rank][songname] = []
        sorted_words = sorted(words.items(), key = lambda word: word[1], reverse = True)

        top_ten_words[rank][songname] = sorted_words[:10]

        rank += 1
    #print(top_ten_words)
    return top_ten_words

def store_top_words(cur, conn, top_ten_words):
    cur.execute("CREATE TABLE IF NOT EXISTS wordIndex (id INTEGER PRIMARY KEY, word TEXT)")
    check = cur.execute("SELECT max(id) FROM wordIndex").fetchone()
    print(check)
    if check[0] == None:
        print("Word Index table is empty, establishing data for first 25 songs")
        accumulate = {}
        count = 0
        for rank, songname in top_ten_words.items():
            for song, wordlist in songname.items():
                for i in range(len(wordlist)):
                    if wordlist[i][0] not in accumulate.values():
                        accumulate[count] = wordlist[i][0]
                        count += 1
                    else:
                        continue
        
        for index, word in accumulate.items(): 
            print (index, word)
            cur.execute("INSERT OR IGNORE INTO wordIndex (id, word) VALUES (?, ?)", (index, word))
        conn.commit()
    else:
        wordtuples = cur.execute("SELECT id, word FROM wordIndex").fetchall()
        count = len(wordtuples) - 1
        print(count)
        word_dict = {}
        for word in wordtuples:
            word_dict[word[0]] = word[1]
        print(word_dict)
        print("Word Index table is already established, storing data starting at ID " + str(count +1))
        for rank, songname in top_ten_words.items():
            for song, wordlist in songname.items():
                    for i in range(len(wordlist)):
                        if wordlist[i][0] not in word_dict.copy().values():
                            count += 1
                            word_dict[count] = wordlist[i][0]
                            print(count, wordlist[i][0])
                            cur.execute("INSERT OR IGNORE INTO wordIndex (id, word) VALUES (?, ?)", (count, wordlist[i][0]))
                            print("Inserted " + wordlist[i][0] + " into id position " + str(count) + " in table wordIndex")
                        else:
                            continue
    conn.commit()            
    top_ten = top_ten_words
    return top_ten

def make_songwordrelation_table(cur, conn, top_ten):
    cur.execute("CREATE TABLE IF NOT EXISTS songWordRelation (song_rank INTEGER, word_id INTEGER, count INTEGER)")
    for rank, songname in top_ten.items():
        for song, wordlist in songname.items():
            for i in range(len(wordlist)):
                word_id = cur.execute("SELECT id from wordIndex Where word = ?", (wordlist[i][0],)).fetchone()
                song_rank = cur.execute("SELECT Rank from Top100 Where TrackName = ?", (song,)).fetchone()
                #print(word_id)
                #print(song_rank)
                if word_id != None:
                    print("This is the word id", word_id[0])
                    print("This is the rank", song_rank[0])
                    print("This is the count", wordlist[i][1])
                    cur.execute("INSERT INTO songWordRelation (song_rank, word_id, count) VALUES (?, ?, ?)", (song_rank[0], word_id[0], wordlist[i][1]))
                
    conn.commit()

def main():
    #Genius api session
    genius = lg.Genius(API_KEY)

    #Database connection and cursor
    conn = sqlite3.connect("spotipyTop100.db")
    cur = conn.cursor()

    #Pull song info from spotipy database
    song_dict = pull_songdata(cur, conn)

    #Lyric Search
    lyrics = lyric_search(genius, song_dict)

    #Clean and count lyrics
    word_counts = clean_and_count_lyrics(lyrics)

    #Find the top ten across all songs
    top_ten_all_songs = find_top_ten(word_counts)

    #Stores Top Words in Table
    top_ten = store_top_words(cur, conn, top_ten_all_songs)

    #Create Song to Words table
    make_songwordrelation_table(cur, conn, top_ten)

main()