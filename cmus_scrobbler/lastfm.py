"""Last.fm scrobble API wrapper"""

import os
import json
import config
import requests
import webbrowser
from hashlib import md5
from datetime import datetime
from dataclasses import dataclass
from urllib.parse import urlencode

PBCK_STATUS_INDEX = 1  # Index of 'playing' in the status list (also can be exiting, stopped, etc.)
LASTFM_API_BASEURL = "http://ws.audioscrobbler.com/2.0/"

def generate_playback_timestamp() -> datetime:
    """Generates the current time and converts to seconds since epoch"""
    return datetime.today().timestamp

@dataclass
class Track:
    # TODO consider removing a lot of these since they don't matter to the API
    filepath: str
    artist: str
    album_artist: str
    album: str
    tracknumber: str
    title: str
    date: str
    duration: str

def TrackFactory(raw_status: list) -> Track:
    """
    Constructs a Track given the raw output of cmus.
    If the given status does not include a 'playing' message, None is returned.
    """

    if raw_status[PBCK_STATUS_INDEX] != "playing":
        return None

    return Track(*raw_status[3::2])

class Lastfm():
    """Last.fm API Class"""
    
    def __init__(self):
        """Creates a Lastfm object"""
        self.config_json = config.read_config()
        self.api_key = self.config_json["api_key"]
        self.secret_key = self.config_json["secret_key"]
        self.session_key = self.config_json["session_key"]
        self.api_token = self.config_json["api_token"]

        if not self.api_token:
            self._generate_api_token()
        elif not self._validate_token():
            self._refresh_token


    # TODO Write out the process for authenticating through the web, user needs to accept their token and then every 60 minutes it needs to refresh

    def _validate_token(self):
        """Checks to see if the api_token is still valid"""
        pass

    def _refresh_token(self):
        """Refreshes a user's API token"""
        pass

    def _generate_api_token(self):
        """
        Authenticates the user within the LastFM API. This will setup the session_key and api_token for the config.
        If an api_token already exists, 
        """
        pass

    def _generate_api_sig(self, params: dict) -> str:
        """Generates the API signature expected by LastFM using the given params"""
        
        api_signature = ""
        for params_key, params_value in sorted(params.items(), key=lambda pkv: (pkv[1], pkv[0])):
            api_signature += f"{params_key}{params_value}"
        
        api_signature += self.secret_key
        api_signature = api_signature.encode("utf-8")

        return md5(api_signature).hexdigest()

    def scrobble(self, track: Track) -> bool:
        """Sends a POST request to Last.fm to log a scrobble, returning the success status"""
        
        params = {
            "method": "track.scrobble",
            "artist": track.artist,
            "track": track.title,
            "timestamp": generate_playback_timestamp(),
            "album": track.album,
            "api_key": self.api_key,
            "sk": self.session_key
        }
        api_signature = self._generate_api_sig(params)
        params["api_sig"] = api_signature

