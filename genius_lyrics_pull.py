import lyricsgenius as lg
import json
import re
import sqlite3
import os


API_KEY = "CUAq9PoXth-VccgEW1vqALmmefhkarPZI3DgyYPJLOfsKVrPvaN3YLJz4wmFdmSQ"

def read_json(cache_filename):
    #attempts to open json cache else initiates empty dictionary. 

    try:
        with open(cache_filename, 'r') as data_r:
            j_dict = json.loads(data_r.read())
            return j_dict
    except:
        j_dict = {}
        return j_dict

def write_json(cache_filename, dict):
    #write json data to file using json indent 4 structure

    with open(cache_filename, 'w') as data_w:
        data_w.write(json.dumps(dict, indent = 4))

def pull_songdata():
    # Pulls song data from spotipyTop100.db
    # Joins Top100 to ArtistIndex and pairs the song data with the artist who produced it. 
    # Returns a dictionary of artist names with a list of their respective songs.
    conn = sqlite3.connect("spotipyTop100.db")
    cur = conn.cursor()
    track_object = cur.execute("SELECT ArtistIndex, TrackName FROM Top100")
    tracks = track_object.fetchall()
    artist_object = cur.execute("SELECT Artist_Index, Artist From ArtistIndex")
    artists = artist_object.fetchall()

    track_dict = {}
    artist_dict = {}

    for i in tracks:
        if i[0] not in track_dict:
            track_dict[i[0]] = [i[1]]
        else:
            track_dict[i[0]].append(i[1])

    for k, v in track_dict.items():
        for i in artists:
            if int(k) == i[0]:
                artist_dict[i[1]] = v
    
    conn.close()
    print("pull_songdata working")
    return artist_dict

def lyric_search(genius, artist_dict, cache):
    lyrics_dict = {}
    pattern = r" +[-(].{5,}"


    if len(cache) > 1:
        print("Lyrics cache already established.")
        return None
    else:
        try:
            print("Establishing lyrics cache.")
            for k, v in artist_dict.items():
                lyrics_dict[k] = {}
                for i in range(len(v)):
                    lyrics_dict[k][v[i]] = {}
                    cleaned_song_name = re.split(pattern, v[i])
                    song = genius.search_song(cleaned_song_name[0], k)
                    lyrics_dict[k][v[i]] = song.lyrics 

            return lyrics_dict
        except:
            print("Exception!")
            return None

def clean_and_count_lyrics(cache):

    word_counts = {}
    ignore_lst = ['the', 'and', 'be', 'for', 'to', '', 'am', 'a', 'how', 'in', 'of', 'who', 'what', \
                  'where', 'why', 'when', 'this', 'that', 'there', 'is', 'isn\'t', 'was', 'wasn\'t', \
                  'it', 'oh', 'mm', 'on', 'it\'s', 'at', 'ah', 'yeah',   ]
    lyric_lead_pattern = r".*[lL]yrics+"
    section_header_pattern = r"\[.*?\]"
    embed_msg_pattern = r"You might also like*[\d]*|Embed|\dEmbed"

    for artist, song in cache.items():
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

            #print(word_counts)


            cleaned_lyrics_lst = string_clean_eleven.split(" ")
            #print(cleaned_lyrics_lst)
            
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

    for songname, words in word_counts.items():
        top_ten_words[songname] = []
        sorted_words = sorted(words.items(), key = lambda word: word[1], reverse = True)

        top_ten_words[songname] = sorted_words[:10]

    print(top_ten_words)
    return top_ten_words
    
def main():
    # Genius_api session
    genius = lg.Genius(API_KEY)

    # Substantiates path for cache
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cache_filename = dir_path + '/' + "cache_lyrics.json"

    # Reads cache via read_json
    cache = read_json(cache_filename)

    # Pull Track dictionary that includes {'Artist': ['Songs", '...'], ...}
    tracks = pull_songdata()

    # Perform API call and lyrics search on tracks from pull_songdata()
    lyrics = lyric_search(genius, tracks, cache)
    print(lyrics)

    # Write newly created dictionary to the json cache
    if lyrics == None:
        print("cache already established")
    else:
        write_json(cache_filename, lyrics)

    # Clean_lyric information for processing, convert to lists of words
    cleaned = clean_and_count_lyrics(cache)

    # Sort word counts by value
    sorted_words = find_top_ten(cleaned)

main()

"""if __name__ == "__main__":
    main()
    unittest.main(verbosity=2) """   