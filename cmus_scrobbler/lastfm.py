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
import xml.etree.ElementTree as ET

PBCK_STATUS_INDEX = 1  # Index of 'playing' in the status list (also can be exiting, stopped, etc.)
LASTFM_API_BASEURL = "http://ws.audioscrobbler.com/2.0/"
LASTFM_AUTH_BASEURL = "http://www.last.fm/api/auth/?"

def generate_playback_timestamp() -> datetime:
    """Generates the current time and converts to seconds since epoch"""
    return str(int(datetime.today().timestamp()))

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

        if not self.session_key:
            self._generate_api_token()
            self._authorize_token()
            self._generate_session_key()

    def _generate_api_token(self):
        """
        Authenticates the user within the LastFM API. This will be used by _authorize_token to create a user-authenticated token and then
        session key.
        """

        params = {
            "api_key": self.api_key,
            "format": "json",
            "method": "auth.getToken"
        }
        params["api_sig"] = self._generate_api_sig(params)

        response = requests.get(LASTFM_API_BASEURL, params=params)
        # TODO better error handling here
        if not (response.status_code % 200) <= 99:
            return ""
        
        self.api_token = response.json()["token"]

    def _authorize_token(self):
        """
        Opens a web browser for the user to authorize the generated API token. This authorized token will be used to generate a
        session key.
        """

        params = {
            "api_key": self.api_key,
            "token": self.api_token
        }
        auth_api_url = LASTFM_AUTH_BASEURL + urlencode(params)
        webbrowser.open_new_tab(auth_api_url)
        input("A web browser has been opened in order to authenticate the generated API token. Hit enter once cmus-scrobbler has been authorized!")

    def _generate_session_key(self):
        """
        Authenticates the user's session within the LastFM API. This will generate session_key for the config.
        This API call consumes the API token, however the session key is infinitely used unless the user unauthroizes the app.
        For some reason, 'format' doesn't work here so parse the output as an XML.
        """

        params = {
            "api_key": self.api_key,
            "method": "auth.getSession",
            "token": self.api_token
        }
        params["api_sig"] = self._generate_api_sig(params)
        response = requests.get(LASTFM_API_BASEURL, params=params)
        if not (response.status_code % 200) <= 99:
            return ""

        root = ET.fromstring(response.content)
        key_xml = root.find("session/key")
        self.session_key = key_xml.text
        config.update_config(session_key=self.session_key)

    def _generate_api_sig(self, params: dict) -> str:
        """Generates the API signature expected by LastFM using the given params"""
        
        api_signature = ""
        for params_key, params_value in sorted(params.items(), key=lambda pkv: pkv[0]):
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
        params["api_sig"] = self._generate_api_sig(params)
        
        response = requests.post(LASTFM_API_BASEURL, params=params)
        #if not (response.status_code % 200) <= 99:

        return response.content