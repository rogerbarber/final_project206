import lyricsgenius as lg
import json
import re
import sqlite3

API_KEY = "CUAq9PoXth-VccgEW1vqALmmefhkarPZI3DgyYPJLOfsKVrPvaN3YLJz4wmFdmSQ"

def pull_songdata(cur, con, length = 0):
    """song_info = cur.execute("SELECT Top100.rank, Top100.TrackName, ArtistIndex.artist \
        From Top100 Join ArtistIndex ON Top100.ArtistIndex = ArtistIndex.artist_index")
    song_dict = {}"""

    song_info = cur.execute("SELECT Top100.rank, Top100.TrackName, ArtistIndex.artist \
        From Top100 Join ArtistIndex ON Top100.ArtistIndex = ArtistIndex.artist_index").fetchall()
    song_dict = {}
    for song in song_info:
        if song[2] not in song_dict:
            song_dict[song[2]] = [(song[0], song[1])]
        else:
            song_dict[song[2]] += [(song[0], song[1])]
    return song_dict

    """if length == 0:
        for i in range(1, length + 26):  
            song = song_info.fetchone()
            #print(song)

            if song[2] not in song_dict:
                song_dict[song[2]] = [(song[0], song[1])]
            else:
                song_dict[song[2]] += [(song[0], song[1])]
        return song_dict
    else:
        
        for i in range(length, length + 25):
            song = cur.execute("SELECT Top100.rank, Top100.TrackName, ArtistIndex.artist \
                From Top100 Join ArtistIndex ON Top100.ArtistIndex = ArtistIndex.artist_index \
                     Join WordCounts ON Top100.rank = WordCounts.id WHERE Top100.rank = (Select MAX(id) FROM WordCounts)")
            song = song_info.fetchone()
            #print(song)

            if song[2] not in song_dict:
                song_dict[song[2]] = [(song[0], song[1])]
            else:
                song_dict[song[2]] += [(song[0], song[1])]
        return song_dict"""

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
    return lyrics_dict

def clean_and_count_lyrics(data_packet):
    word_counts = {}
    ignore_lst = ['the', 'and', 'be', 'for', 'to', '', 'am', 'a', 'how', 'in', 'of', \
                  'this', 'that', 'there', 'is', 'isn\'t', 'was', 'wasn\'t', \
                  'it', 'oh', 'mm', 'on', 'it\'s', 'at', 'ah']
    lyric_lead_pattern = r".*[lL]yrics+"
    section_header_pattern = r"\[.*?\]"
    embed_msg_pattern = r"You might also like*[\d]*|Embed|\dEmbed"

    for artist, song in data_packet.items():
        for songname, lyrics in song.items():
            word_counts[songname] = {}
            
            string_clean_one = lyrics.replace("\n", " ")
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

def dataset_word_counts(top_ten_all_songs):
    total_word_counts = {}
    for rank, song_data in top_ten_all_songs.items():
        for song, words in song_data.items():
            for i in range(len(words)):
                if words[i][0] not in total_word_counts:
                    total_word_counts[words[i][0]] = words[i][1]
                else:
                    total_word_counts[words[i][0]] += words[i][1]

    sorted_total = sorted(total_word_counts.items(), key = lambda word: word[1], reverse = True)
    #print(sorted_total)
    return(sorted_total)

def groom_data_for_database(top_ten_words, total_word_counts):
    data_dict = {}
    data_set_10 = total_word_counts[0:10]

    print(data_set_10)
        
    for rank, song_info in top_ten_words.items():
        data_dict[rank] = {}
        for song, words in song_info.items():
            #print(words)
            data_dict[rank][song] = {}
            for i in range(len(data_set_10)):
                if data_set_10[i][0] not in data_dict and data_set_10[i][0] == words[i][0]:
                    data_dict[rank][song][words[i][0]] = words[i][1]
                elif data_set_10[i][0] != words[i][0]:
                    continue
                else:
                    data_dict[rank][song][words[i][0]] = 0

    print(data_dict)
    return data_dict

def build_word_database(cur, conn):
    pass

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

    #Total word counts across entire dataset
    total_words = dataset_word_counts(top_ten_all_songs)

    #Groom data for database insert
    data = groom_data_for_database(top_ten_all_songs, total_words)

main()