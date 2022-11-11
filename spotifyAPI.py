# Client ID: 670aabd450884ac4b78a2cdfcc6efb9e
# Client Secret: 3c6bfedf6ddd4a579cd735ad2bd8b6d6

# Billboard Top 100 Playlist ID: 6UeSakyzhiEt4NB3UAd6NQ

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Creating spotipy object with credentials
client_credentials_manager = SpotifyClientCredentials(client_id="670aabd450884ac4b78a2cdfcc6efb9e", client_secret="3c6bfedf6ddd4a579cd735ad2bd8b6d6")
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

print(sp)




