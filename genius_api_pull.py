import json
import requests
import sqllite3
import lyricsgenius as lg

client_id = "TmD7GV5BRXgFuQV9909xljkicmNgYSD3ccE-ysqcGqcsIEKJrKfpoQ6h9RT3nNMq"
client_secret = "TmD7GV5BRXgFuQV9909xljkicmNgYSD3ccE-ysqcGqcsIEKJrKfpoQ6h9RT3nNMq"
access_token = "CUAq9PoXth-VccgEW1vqALmmefhkarPZI3DgyYPJLOfsKVrPvaN3YLJz4wmFdmSQ"

genius = lg.Genius(access_token)



#artist = genius.search_artist("James Blake", max_songs = 5, sort = 'title')
#artist = genius.search_artist("Beyonce", max_songs = 5, sort = "title")
#print(artist)

#song = genius.search_song("Lemonade", "Beyonce")

#lemonade_lyrics = song.lyrics

#print(lemonade_lyrics)

#song = genius.search_song("Unholy", "Sam Smith")

#unholy_lyrics = song.lyrics

#print(unholy_lyrics)

#song = genius.search_song("Shirt", "SZA")

#print(song.lyrics)

songs = {"Taylor Swift": ["Anti-Hero", "Lavender Haze", "Midnight Rain",
                          "Bejeweled", "Maroon", "Karma", "Snow On The Beach",
                          "You're On Your Own, Kid"],
         "Drake": ["Rich Flex", "Major Distribution", "On BS",
                   "Spin Bout U", "Pussy & Millions", "Privileged Rappers",
                   "Circo Loco", "BackOutsideBoyz", "Hours In Silence", "Broke Boys",
                   "Treacherous Twins", "Middle of the Ocean", "Jumbotron Shit Poppin",
                   "More M's", "I Guess It's Fuck Me", "3AM on Glenwood", "Jimmy Cooks"],
         "Sam Smith":["Unholy"],
         "Steve Lacy": ["Bad Habit"],
         "Harry Styles": ["As it Was"],
         "David Guetta": ["I'm Good (Blue)"],
         "Nicki Minaj": ["Super Freaky Girl"],
         "Rihanna": ["Lift Me Up"],
         "Post Malone": ["I Like You"],
         "Moran Wallen": ["You Proof"],
         "Zach Bryan": ["Something in the Orange"],
         "One Republic": ["I Ain't Worried"],
         "Doja Cat": ["Vegas"],
         "Chris Brown": ["Under The Influence"],
         "The Weeknd": ["Die For You"],
         "Nicky Youre": ["Sunroof"],
         "Morgan Wallen": ["Wasted On You"],
         "Beyonce": ["CUFF IT"],
         "Future": ["WAIT FOR U"],
         "Bad Bunny": ["Titi me Pregunto"],
         "Lil Uzi Vert": ["Just Wanna Rock"],
         "Luke Combs": ["The Kind of Love We Make"],
         "SZA": ["Shirt"],
         "Cole Swindell": ["She Had Me At Heads Carolina"],
         "Lizzo": ["About Damn Time"],
         "GloRilla": ["Tomorrow 2"],
         "Sia": ["Unstoppable"]
         }
