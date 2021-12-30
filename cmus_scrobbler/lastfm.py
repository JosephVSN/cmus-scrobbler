"""Last.fm scrobble API wrapper"""

import os
import json
import config
import requests
import webbrowser
from urllib.parse import urlencode

class Lastfm():
    """Last.fm API Class"""
    def __init__(self):
        """Creates a Lastfm object"""
        self._api_session = None
        self._api_session_key = None
        self._config = config.read_config()
        self._authenticate()

    # TODO Write out the process for authenticating through the web, user needs to accept their token and then every 60 minutes it needs to refresh
    # Maybe re-think how this class works, or what its for

    def _authenticate(self):
        """Authenticates against the Last.fm API and sets the self._api_session to an authenticated Requests session if successful"""


    def scrobble(self, track) -> bool:
        """Sends a POST request to Last.fm to log a scrobble, returning the success status"""
        pass
