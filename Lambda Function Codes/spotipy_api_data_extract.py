import json
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import boto3
from datetime import datetime

def lambda_handler(event, context):
    client_id = os.environ.get('client_id')
    client_secret = os.environ.get('client_secret')

    # This is used for authentication purposes
    client_credetials_manager = SpotifyClientCredentials(client_id = client_id, client_secret= client_secret)
    # This is used for the authorization purpose
    sp = spotipy.Spotify(client_credentials_manager = client_credetials_manager)

    playlist_link = 'https://open.spotify.com/playlist/1bvcVgSFFKobfJOWgsUrEe'
    playlist_URI = playlist_link.split("/")[-1]

    # Fetch data from the spotipy
    data = sp.playlist_tracks(playlist_URI)

    print(data)

    cilent = boto3.client('s3')
    filename = "spotipy_raw_"+str(datetime.now())+".json"

    cilent.put_object(
        Bucket = "spotipy-etl-project-anamika",
        Key = "raw_data/to_processed/"+filename,
        Body = json.dumps(data)
    )
    
