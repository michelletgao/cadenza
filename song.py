import json
import os
from db import User, Song, Request, Recommendation
import requests

def song_search(search):
    # go to the right url, get search results
    url = "https://itunes.apple.com/search?" + "term=" + search + "&entity=song&limit=5"
    response = requests.get(url)
    json_response = response.json()
    song_info = json_response.get("results")

    # get song titles, artists, and album names and add to list
    search_results = []
    for i in song_info:
        song_dict = {}
        track_title = i.get("trackName")
        artist_name = i.get("artistName")
        album = i.get("collectionName")
        song_dict["title"] = track_title
        song_dict["artist"] = artist_name
        song_dict["album"] = album
        search_results.append(song_dict)
    
    return search_results

